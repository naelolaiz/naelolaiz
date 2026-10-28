"""Checks for statistical boundaries, source scope, failed-refresh preservation,
rendered output, and README/configuration consistency."""

from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ElementTree


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import update_project_statistics as statistics

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class CalendarTests(unittest.TestCase):
    def test_local_month_and_year_boundaries(self):
        window = statistics.activity_window(
            statistics.aware_datetime("2026-09-30T22:30:00Z"), "Europe/Madrid", 12,
        )
        self.assertEqual(window.months[0], "2025-11")
        self.assertEqual(window.months[-1], "2026-10")
        self.assertEqual(window.start.isoformat(), "2025-11-01T00:00:00+01:00")
        self.assertEqual(window.end.isoformat(), "2026-10-01T00:30:00+02:00")
        commits = [
            int(statistics.aware_datetime(value).timestamp()) for value in [
                "2025-10-31T22:59:59Z",  # Before the first local calendar month.
                "2025-10-31T23:00:00Z",  # First included instant.
                "2026-09-30T21:59:59Z",  # September locally.
                "2026-09-30T22:00:00Z",  # October locally.
                "2026-09-30T22:30:00Z",  # Collection boundary is inclusive.
                "2026-09-30T22:30:01Z",  # Future commit must be excluded.
            ]
        ]
        buckets = statistics.bucket_commits(commits, window)
        self.assertEqual(buckets["2025-11"], 1)
        self.assertEqual(buckets["2026-09"], 1)
        self.assertEqual(buckets["2026-10"], 2)
        self.assertEqual(sum(buckets.values()), 4)

    def test_dst_repeated_hour_does_not_include_future_commits(self):
        window = statistics.activity_window(
            statistics.aware_datetime("2026-10-25T00:30:00Z"), "Europe/Madrid", 12,
        )
        # Both commits show 02:15 locally, on opposite sides of the clock change.
        timestamps = [
            int(statistics.aware_datetime(value).timestamp())
            for value in ["2026-10-25T00:15:00Z", "2026-10-25T01:15:00Z"]
        ]
        self.assertEqual(statistics.bucket_commits(timestamps, window)["2026-10"], 1)

    def test_naive_collection_time_is_refused(self):
        with self.assertRaises(statistics.CollectionError):
            statistics.aware_datetime("2026-10-08T22:00:00")
        with self.assertRaises(statistics.CollectionError):
            statistics.activity_window(datetime(2026, 10, 8), "Europe/Madrid", 12)


class SourceScopeTests(unittest.TestCase):
    def setUp(self):
        self.window = statistics.activity_window(
            statistics.aware_datetime("2026-10-08T20:00:00Z"), "Europe/Madrid", 12,
        )

    def repository(self, name, *, fork=False, languages=None, commits=0,
                   last_commit="2026-10-01T00:00:00+00:00", workflows=None):
        return {
            "name": name, "fork": fork, "languages": languages or {},
            "commits_by_month": {month: commits for month in self.window.months},
            "last_commit_at": last_commit, "workflow_files": workflows or [],
        }

    def test_forks_cannot_inflate_language_activity_or_workflow_totals(self):
        source = self.repository("source", languages={"C": 100, "Python": 25}, commits=2,
                                 workflows=[".github/workflows/build.yml"])
        second = self.repository("other", languages={"C": 40}, commits=1)
        fork = self.repository("support", fork=True, languages={"Rust": 100000}, commits=1000,
                               workflows=[".github/workflows/upstream.yml"])
        result = statistics.build_snapshot([source, second, fork], self.window)
        self.assertEqual(result["summary"], {
            "featured_repositories": 3, "source_repositories": 2, "support_forks": 1,
            "language_count": 2, "repositories_with_workflows": 1,
            "commits_in_period": 36, "active_repositories_90_days": 2,
        })
        self.assertEqual(result["languages"], [
            {"name": "C", "bytes": 140, "repositories": 2},
            {"name": "Python", "bytes": 25, "repositories": 1},
        ])
        self.assertEqual([item["commits"] for item in result["activity"]], [3] * 12)
        self.assertEqual([item["partial"] for item in result["activity"]], [False] * 11 + [True])

    def test_recent_repository_count_uses_exact_90_days_and_excludes_future_head(self):
        rows = [
            self.repository("at-boundary", last_commit="2026-07-10T20:00:00Z"),
            self.repository("too-old", last_commit="2026-07-10T19:59:59Z"),
            self.repository("future", last_commit="2026-10-08T20:00:01Z"),
        ]
        result = statistics.build_snapshot(rows, self.window)
        self.assertEqual(result["summary"]["active_repositories_90_days"], 1)

    def test_fork_is_metadata_only_and_missing_languages_abort(self):
        config = {
            "owner": "example", "timezone": "Europe/Madrid", "activity_months": 12,
            "repositories": ["support", "source"],
        }
        metadata = [
            {"full_name": f"example/{name}", "private": False, "fork": fork,
             "default_branch": "main", "stargazers_count": 0, "forks_count": 0}
            for name, fork in [("support", True), ("source", False)]
        ]
        client = Mock()
        client.languages.side_effect = statistics.CollectionError("Language fetch failed.")
        with patch.object(statistics, "cached_repository") as cache:
            with self.assertRaisesRegex(statistics.CollectionError, "Language fetch failed"):
                statistics.collect(config, client, Path("/tmp/unused-test-cache"),
                                   self.window.end, metadata)
        client.repositories.assert_not_called()
        client.languages.assert_called_once_with("example", "source")
        cache.assert_not_called()


class GitHistoryTests(unittest.TestCase):
    def test_only_direct_yaml_workflow_files_count_as_workflow_presence(self):
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)

            def git(*arguments):
                return subprocess.run(["git", *arguments], cwd=repository, text=True,
                                      capture_output=True, check=True).stdout.strip()

            git("init", "--initial-branch=main")
            for name in [
                ".github/workflows/build.yml", ".github/workflows/test.yaml",
                ".github/workflows/README.md", ".github/workflows/nested/ignored.yml",
                ".github/elsewhere/ignored.yml",
            ]:
                path = repository / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture\n")
            git("add", ".github")
            with patch.dict(statistics.os.environ, {
                "GIT_AUTHOR_DATE": "2026-10-01T12:00:00+00:00",
                "GIT_COMMITTER_DATE": "2026-10-01T12:00:00+00:00",
            }):
                git("-c", "user.name=test", "-c", "user.email=test@example.invalid",
                    "commit", "-m", "fixture")
            window = statistics.activity_window(
                statistics.aware_datetime("2026-10-08T20:00:00Z"), "Europe/Madrid", 12,
            )
            result = statistics.git_activity(repository, "main", window)
            self.assertEqual(result["workflow_files"], [
                ".github/workflows/build.yml", ".github/workflows/test.yaml",
            ])

    def test_merges_are_excluded_but_nonmonotonic_ancestors_are_counted(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(statistics.os.environ, {
            "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "safe.bareRepository",
            "GIT_CONFIG_VALUE_0": "explicit",
        }):
            repository = Path(temporary)

            def git(*arguments, input=None):
                return subprocess.run(
                    ["git", "--git-dir", str(repository), *arguments],
                    cwd=repository, input=input, text=True,
                    capture_output=True, check=True,
                ).stdout.strip()

            git("init", "--bare", "--initial-branch=main")
            tree = git("mktree", input="")

            def commit(date, *parents):
                environment = {
                    "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
                    "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
                    "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date,
                }
                arguments = ["git", "--git-dir", str(repository), "commit-tree", tree]
                for parent in parents:
                    arguments.extend(["-p", parent])
                with patch.dict(statistics.os.environ, environment):
                    return subprocess.run(arguments, cwd=repository, input="test\n", text=True,
                                          capture_output=True, check=True).stdout.strip()

            current = commit("2026-10-01T12:00:00+00:00")
            older_parent = commit("2025-01-01T12:00:00+00:00", current)
            other = commit("2026-10-02T12:00:00+00:00", current)
            merge = commit("2026-10-03T12:00:00+00:00", older_parent, other)
            future = commit("2026-10-09T12:00:00+00:00", merge)
            git("update-ref", "refs/heads/main", future)
            window = statistics.activity_window(
                statistics.aware_datetime("2026-10-08T20:00:00Z"), "Europe/Madrid", 12,
            )
            result = statistics.git_activity(repository, "main", window, bare=True)
            self.assertEqual(result["commits_by_month"]["2026-10"], 2)
            self.assertEqual(sum(result["commits_by_month"].values()), 2)
            self.assertEqual(result["last_commit_at"], "2026-10-09T12:00:00+00:00")
            self.assertEqual(result["workflow_files"], [])

    def test_cached_repository_can_be_refreshed_with_explicit_bare_repository_safety(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "sources" / "source.git"
            source.mkdir(parents=True)
            subprocess.run(["git", "init", "--initial-branch=main"], cwd=source,
                           capture_output=True, check=True)
            (source / "fixture.txt").write_text("fixture\n")
            subprocess.run(["git", "add", "fixture.txt"], cwd=source, capture_output=True, check=True)
            subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                            "commit", "-m", "fixture"], cwd=source, capture_output=True, check=True)
            with patch.dict(statistics.os.environ, {
                "GIT_CONFIG_COUNT": "2",
                "GIT_CONFIG_KEY_0": "safe.bareRepository", "GIT_CONFIG_VALUE_0": "explicit",
                "GIT_CONFIG_KEY_1": f"url.{source.parent.as_uri()}/.insteadOf",
                "GIT_CONFIG_VALUE_1": "https://github.com/example/",
            }):
                cache = statistics.cached_repository("example", "source", "main", root / "cache")
                self.assertEqual(
                    statistics.cached_repository("example", "source", "main", root / "cache"), cache,
                )
                self.assertEqual(
                    statistics.run_git(
                        ["--git-dir", str(cache), "rev-parse", "--is-bare-repository"],
                    ).strip(), "true",
                )


class PublicationTests(unittest.TestCase):
    def test_failed_collection_keeps_published_snapshot_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot_file = root / "data.json"
            snapshot_file.write_text('{"previous": true}\n')
            config = root / "projects.json"
            config.write_text(json.dumps({
                "owner": "example", "timezone": "Europe/Madrid", "activity_months": 12,
                "repositories": ["source"],
            }))
            with patch.object(statistics, "collect", side_effect=statistics.CollectionError("Network failed.")), \
                 patch.object(statistics, "publish") as publish, \
                 patch("sys.stderr"):
                result = statistics.main(["--config", str(config)])
            self.assertEqual(result, 1)
            publish.assert_not_called()
            self.assertEqual(snapshot_file.read_text(), '{"previous": true}\n')

    def test_invalid_render_does_not_overwrite_any_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            data = output / "data.json"
            data.write_text("previous snapshot\n")
            svg = output / "overview.svg"
            svg.write_text("previous SVG\n")
            renderer = types.ModuleType("render_project_statistics")
            renderer.render = lambda snapshot: {"overview.svg": "<svg/>"}
            with patch.dict(sys.modules, {"render_project_statistics": renderer}):
                with self.assertRaises(statistics.CollectionError):
                    statistics.publish({}, output)
            self.assertEqual(data.read_text(), "previous snapshot\n")
            self.assertEqual(svg.read_text(), "previous SVG\n")
            self.assertEqual(sorted(path.name for path in output.iterdir()), ["data.json", "overview.svg"])

    def test_snapshot_and_views_are_written_flat_into_the_output_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "project-statistics"
            snapshot = statistics.read_json(FIXTURES / "snapshot" / "data.json")
            statistics.publish(snapshot, output)
            self.assertEqual(sorted(path.name for path in output.iterdir()), [
                "activity.svg", "data.json", "languages.svg", "overview.svg",
            ])
            self.assertEqual(json.loads((output / "data.json").read_text()), snapshot)


class RendererTests(unittest.TestCase):
    """tests/fixtures/snapshot holds a real published snapshot and its expected views.

    After an intentional renderer change, regenerate the expected files and
    review the SVG diff:

        python3 scripts/update_project_statistics.py \\
            --input tests/fixtures/snapshot/data.json --output tests/fixtures/snapshot
    """

    SNAPSHOT = FIXTURES / "snapshot"
    VIEWS = ("overview.svg", "languages.svg", "activity.svg")

    def published(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            statistics.publish(statistics.read_json(self.SNAPSHOT / "data.json"), output)
            return {path.name: path.read_text(encoding="utf-8") for path in output.iterdir()}

    def test_fixture_snapshot_renders_to_the_expected_files(self):
        published = self.published()
        self.assertEqual(sorted(published), sorted(("data.json", *self.VIEWS)))
        for name, content in published.items():
            with self.subTest(file=name):
                expected = (self.SNAPSHOT / name).read_text(encoding="utf-8")
                self.assertEqual(content, expected, f"{name} differs from the expected output; "
                                 "see RendererTests for how to regenerate it.")

    def test_views_are_well_formed_and_labelled(self):
        namespace = "{http://www.w3.org/2000/svg}"
        for name, content in self.published().items():
            if name not in self.VIEWS:
                continue
            with self.subTest(file=name):
                svg = ElementTree.fromstring(content)
                self.assertEqual(svg.tag, f"{namespace}svg")
                ids = {element.get("id") for element in svg.iter() if element.get("id")}
                labels = svg.get("aria-labelledby", "").split()
                self.assertTrue(labels, "the view has no aria-labelledby")
                self.assertLessEqual(set(labels), ids, "aria-labelledby names a missing element")
                self.assertTrue(svg.findtext(f"{namespace}title"), "the view has no title")
                self.assertTrue(svg.findtext(f"{namespace}desc"), "the view has no description")


class ReadmeConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.config = statistics.read_json(ROOT / "stats/projects.json")
        self.owner = self.config["owner"]

    def test_featured_repositories_match_the_readme(self):
        pattern = rf"(?:github\.com|raw\.githubusercontent\.com)/{re.escape(self.owner)}/([A-Za-z0-9_.-]+)"
        # The profile repository is named after its owner and is not a featured project.
        linked = {name.casefold(): name for name in re.findall(pattern, self.readme)}
        linked.pop(self.owner.casefold(), None)
        configured = {name.casefold(): name for name in self.config["repositories"]}
        problems = []
        if missing := sorted(linked[key] for key in linked.keys() - configured.keys()):
            problems.append(f"README links repositories missing from stats/projects.json: {missing}")
        if unlinked := sorted(configured[key] for key in configured.keys() - linked.keys()):
            problems.append(f"stats/projects.json lists repositories the README never links: {unlinked}")
        self.assertFalse(problems, "; ".join(problems))

    def test_readme_embeds_the_views_from_the_published_branch(self):
        workflow = (ROOT / ".github/workflows/project-statistics.yml").read_text(encoding="utf-8")
        match = re.search(r"^\s*STATISTICS_BRANCH:\s*(\S+)\s*$", workflow, re.MULTILINE)
        self.assertIsNotNone(match, "the workflow does not define STATISTICS_BRANCH")
        base = f"https://raw.githubusercontent.com/{self.owner}/{self.owner}/{match.group(1)}/"
        for name in RendererTests.VIEWS:
            with self.subTest(view=name):
                url = f"{base}{name}"
                self.assertTrue(f"({url})" in self.readme, f"README does not embed {url}")


if __name__ == "__main__":
    unittest.main()
