#!/usr/bin/env python3
"""Collect public repository statistics and render the committed SVG snapshots."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = Path(__file__).resolve().parents[1]
UTC = timezone.utc


class CollectionError(RuntimeError):
    """A failed collection must leave the published snapshot untouched."""


@dataclass(frozen=True)
class ActivityWindow:
    start: datetime
    end: datetime
    months: tuple[str, ...]
    timezone_name: str


def aware_datetime(value: str) -> datetime:
    """Parse an ISO timestamp, refusing ambiguous timestamps without an offset."""
    if not isinstance(value, str):
        raise CollectionError("Expected an ISO timestamp with a timezone offset.")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError) as error:
        raise CollectionError("Expected an ISO timestamp with a timezone offset.") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CollectionError("Expected an ISO timestamp with a timezone offset.")
    return parsed


def activity_window(as_of: datetime, timezone_name: str, months: int) -> ActivityWindow:
    if as_of.tzinfo is None or as_of.utcoffset() is None:
        raise CollectionError("The collection timestamp must include a timezone offset.")
    if not isinstance(months, int) or isinstance(months, bool) or months < 1:
        raise CollectionError("activity_months must be a positive integer.")
    try:
        local_end = as_of.astimezone(ZoneInfo(timezone_name))
    except (ZoneInfoNotFoundError, TypeError) as error:
        raise CollectionError("The configured timezone is not available.") from error
    final_month = local_end.year * 12 + local_end.month - 1
    month_numbers = range(final_month - months + 1, final_month + 1)
    labels = tuple(f"{number // 12:04d}-{number % 12 + 1:02d}" for number in month_numbers)
    first_year, first_month = map(int, labels[0].split("-"))
    start = datetime(first_year, first_month, 1, tzinfo=local_end.tzinfo)
    return ActivityWindow(start, local_end, labels, timezone_name)


def bucket_commits(timestamps: list[int], window: ActivityWindow) -> dict[str, int]:
    """Count only timestamps inside the window, using local calendar months."""
    counts = dict.fromkeys(window.months, 0)
    first_timestamp = window.start.timestamp()
    final_timestamp = window.end.timestamp()
    for timestamp in timestamps:
        if first_timestamp <= timestamp <= final_timestamp:
            committed_at = datetime.fromtimestamp(timestamp, UTC).astimezone(window.end.tzinfo)
            counts[committed_at.strftime("%Y-%m")] += 1
    return counts


def nonnegative_integer(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise CollectionError(f"Missing or invalid {label}.")
    return value


def validate_config(config: dict) -> dict:
    owner = config.get("owner")
    if not isinstance(owner, str) or not re.fullmatch(r"[A-Za-z0-9-]+", owner):
        raise CollectionError("The configuration must contain a valid GitHub owner.")
    names = config.get("repositories")
    if not isinstance(names, list) or not names:
        raise CollectionError("The configuration must list the featured repositories.")
    for name in names:
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            raise CollectionError("The configuration contains an invalid repository name.")
        if name in {".", ".."}:
            raise CollectionError("The configuration contains an invalid repository name.")
    if len({name.casefold() for name in names}) != len(names):
        raise CollectionError("The configuration contains duplicate repositories.")
    if not isinstance(config.get("timezone"), str):
        raise CollectionError("The configuration must specify a timezone.")
    activity_window(datetime.now(UTC), config["timezone"], config.get("activity_months"))
    return config


class GitHubClient:
    def __init__(self, token: str | None = None):
        self.token = token

    def get(self, endpoint: str) -> object:
        url = f"https://api.github.com{endpoint}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "project-statistics-snapshot",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            with urlopen(Request(url, headers=headers), timeout=60) as response:
                return json.load(response)
        except HTTPError as error:
            # Do not echo request headers, response bodies, or credentials.
            raise CollectionError(f"GitHub request failed ({error.code}): {endpoint}") from None
        except (URLError, TimeoutError, OSError, json.JSONDecodeError):
            raise CollectionError(f"GitHub request failed: {endpoint}") from None

    def repositories(self, owner: str) -> list[dict]:
        repositories = []
        page = 1
        while True:
            result = self.get(f"/users/{owner}/repos?per_page=100&page={page}")
            if not isinstance(result, list):
                raise CollectionError("GitHub returned invalid repository metadata.")
            repositories.extend(result)
            if len(result) < 100:
                return repositories
            page += 1

    def languages(self, owner: str, name: str) -> dict[str, int]:
        result = self.get(f"/repos/{owner}/{name}/languages")
        if not isinstance(result, dict):
            raise CollectionError(f"GitHub returned invalid language data for {name}.")
        for language, amount in result.items():
            if not isinstance(language, str) or not language:
                raise CollectionError(f"GitHub returned invalid language data for {name}.")
            nonnegative_integer(amount, f"language byte count for {name}")
        return result


def run_git(arguments: list[str], *, cwd: Path | None = None) -> str:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["GCM_INTERACTIVE"] = "Never"
    try:
        result = subprocess.run(
            ["git", *arguments], cwd=cwd, env=environment, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise CollectionError("Git could not complete a repository operation.") from None
    if result.returncode:
        # Git's stderr can include credential-helper output, so do not publish it.
        raise CollectionError(f"Git repository operation failed (exit {result.returncode}).")
    return result.stdout


def cached_repository(owner: str, name: str, branch: str, cache_dir: Path) -> Path:
    repository = cache_dir / owner / f"{name}.git"
    ref = f"refs/heads/{branch}"
    run_git(["check-ref-format", ref])
    url = f"https://github.com/{owner}/{name}.git"
    if repository.exists():
        if run_git(["rev-parse", "--is-bare-repository"], cwd=repository).strip() != "true":
            raise CollectionError(f"The repository cache is not bare: {name}.")
        # Fetch the expected public URL directly; never trust a cached remote URL.
        run_git(["fetch", "--filter=blob:none", "--no-tags", url, f"+{ref}:{ref}"], cwd=repository)
    else:
        repository.parent.mkdir(parents=True, exist_ok=True)
        run_git([
            "clone", "--bare", "--filter=blob:none", "--single-branch", "--no-tags",
            "--branch", branch, "--", url, str(repository),
        ])
    return repository


def git_activity(repository: Path, branch: str, window: ActivityWindow) -> dict:
    ref = f"refs/heads/{branch}"
    # No --since traversal filter: dates need not be monotonic along Git history.
    output = run_git(["log", "--no-merges", "--format=%ct", ref], cwd=repository)
    try:
        timestamps = [int(value) for value in output.splitlines()]
    except ValueError:
        raise CollectionError("Git returned invalid commit timestamps.") from None
    last_commit = aware_datetime(run_git(["show", "-s", "--format=%cI", ref], cwd=repository).strip())
    tree = run_git([
        "ls-tree", "-r", "--name-only", "-z", ref, "--", ".github/workflows",
    ], cwd=repository)
    workflow_files = sorted(
        name for name in tree.split("\0") if name
        and PurePosixPath(name).parent == PurePosixPath(".github/workflows")
        and PurePosixPath(name).suffix in {".yml", ".yaml"}
    )
    return {
        "commits_by_month": bucket_commits(timestamps, window),
        "last_commit_at": last_commit.astimezone(UTC).isoformat(),
        "workflow_files": workflow_files,
    }


def build_snapshot(repositories: list[dict], window: ActivityWindow) -> dict:
    sources = [repository for repository in repositories if not repository["fork"]]
    language_bytes = Counter()
    language_repositories = Counter()
    total_activity = dict.fromkeys(window.months, 0)
    active_since = window.end.astimezone(UTC) - timedelta(days=90)
    active_repositories = 0
    for repository in sources:
        for language, amount in repository["languages"].items():
            language_bytes[language] += amount
            if amount:
                language_repositories[language] += 1
        for month in window.months:
            total_activity[month] += repository["commits_by_month"][month]
        last_commit = aware_datetime(repository["last_commit_at"])
        if active_since <= last_commit <= window.end:
            active_repositories += 1
    languages = [
        {"name": name, "bytes": amount, "repositories": language_repositories[name]}
        for name, amount in sorted(language_bytes.items(), key=lambda item: (-item[1], item[0]))
        if amount
    ]
    return {
        "generated_at": window.end.astimezone(UTC).isoformat(),
        "timezone": window.timezone_name,
        "period": {"start": window.start.isoformat(), "end": window.end.isoformat()},
        "repositories": repositories,
        "summary": {
            "featured_repositories": len(repositories),
            "source_repositories": len(sources),
            "support_forks": len(repositories) - len(sources),
            "language_count": len(languages),
            "repositories_with_workflows": sum(bool(repository["workflow_files"]) for repository in sources),
            "commits_in_period": sum(total_activity.values()),
            "active_repositories_90_days": active_repositories,
        },
        "languages": languages,
        "activity": [
            {"month": month, "commits": commits, "partial": month == window.months[-1]}
            for month, commits in total_activity.items()
        ],
    }


def collect(config: dict, client: GitHubClient, cache_dir: Path, as_of: datetime,
            metadata: list[dict] | None = None) -> dict:
    config = validate_config(config)
    window = activity_window(as_of, config["timezone"], config["activity_months"])
    owner = config["owner"]
    metadata = client.repositories(owner) if metadata is None else metadata
    if not isinstance(metadata, list) or any(not isinstance(item, dict) for item in metadata):
        raise CollectionError("Repository metadata must be a list of GitHub repository objects.")
    by_name = {}
    for item in metadata:
        full_name = item.get("full_name", "")
        if isinstance(full_name, str) and full_name.casefold().startswith(f"{owner}/".casefold()):
            by_name[full_name.split("/", 1)[1].casefold()] = item
    selected_metadata = []
    for name in config["repositories"]:
        item = by_name.get(name.casefold())
        if item is None or item.get("private") is not False:
            raise CollectionError(f"Public repository metadata is unavailable for {name}.")
        if not isinstance(item.get("fork"), bool):
            raise CollectionError(f"Fork metadata is unavailable for {name}.")
        branch = item.get("default_branch")
        if not isinstance(branch, str) or not branch:
            raise CollectionError(f"Default branch metadata is unavailable for {name}.")
        selected_metadata.append((name, item))
    repositories = []
    for name, item in selected_metadata:
        repository = {
            "name": name,
            "url": f"https://github.com/{owner}/{name}",
            "default_branch": item["default_branch"],
            "fork": item["fork"],
            "languages": {},
            "commits_by_month": {},
            "last_commit_at": None,
            "workflow_files": [],
            "stars": nonnegative_integer(item.get("stargazers_count"), f"star count for {name}"),
            "forks": nonnegative_integer(item.get("forks_count"), f"fork count for {name}"),
        }
        if not repository["fork"]:
            try:
                repository["languages"] = client.languages(owner, name)
                cached = cached_repository(owner, name, repository["default_branch"], cache_dir)
                repository.update(git_activity(cached, repository["default_branch"], window))
            except CollectionError as error:
                raise CollectionError(f"{name}: {error}") from error
        repositories.append(repository)
    return build_snapshot(repositories, window)


def publish(snapshot: dict, root: Path = ROOT) -> None:
    # Render all outputs before touching the published snapshot.
    try:
        from render_project_statistics import render
    except ImportError as error:
        raise CollectionError("The project statistics renderer is unavailable.") from error
    rendered = render(snapshot)
    required = {"overview.svg", "languages.svg", "activity.svg"}
    if not isinstance(rendered, dict) or set(rendered) != required:
        raise CollectionError("The renderer did not return the three expected SVG files.")
    outputs = {root / "stats/data.json": json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"}
    for filename, content in rendered.items():
        if not isinstance(content, str) or not content.lstrip().startswith("<svg"):
            raise CollectionError(f"The renderer returned invalid SVG content for {filename}.")
        outputs[root / "assets/project-statistics" / filename] = content
    staged = []
    try:
        for destination, content in outputs.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=destination.parent, delete=False,
                prefix=f".{destination.name}.",
            ) as temporary:
                temporary.write(content)
                staged.append((Path(temporary.name), destination))
        for temporary, destination in staged:
            os.replace(temporary, destination)
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)


def read_json(path: Path) -> object:
    try:
        with path.open(encoding="utf-8") as source:
            return json.load(source)
    except (OSError, json.JSONDecodeError):
        raise CollectionError(f"Could not read JSON from {path}.") from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "stats/projects.json")
    parser.add_argument("--metadata", type=Path, help="Use a saved /users/{owner}/repos response.")
    parser.add_argument("--cache-dir", type=Path, default=Path(tempfile.gettempdir()) / "project-statistics")
    parser.add_argument("--input", type=Path, help="Render an existing snapshot without network access.")
    parser.add_argument("--as-of", help="Use an explicit ISO timestamp with a timezone offset.")
    arguments = parser.parse_args(argv)
    try:
        if arguments.input:
            snapshot = read_json(arguments.input)
        else:
            config = read_json(arguments.config)
            if not isinstance(config, dict):
                raise CollectionError("The statistics configuration must be a JSON object.")
            as_of = aware_datetime(arguments.as_of) if arguments.as_of else datetime.now(UTC)
            metadata = read_json(arguments.metadata) if arguments.metadata else None
            snapshot = collect(
                config, GitHubClient(os.environ.get("GITHUB_TOKEN")), arguments.cache_dir,
                as_of, metadata,
            )
        publish(snapshot)
    except (CollectionError, KeyError, TypeError, ValueError, OverflowError, OSError) as error:
        print(f"Project statistics were not updated: {error}", file=sys.stderr)
        return 1
    print("Updated project statistics and three SVG views.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
