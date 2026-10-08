"""Checks for statistical boundaries, source scope, and failed-refresh preservation."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import update_project_statistics as statistics


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
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)

            def git(*arguments, input=None):
                return subprocess.run(
                    ["git", *arguments], cwd=repository, input=input, text=True,
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
                arguments = ["git", "commit-tree", tree]
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
            result = statistics.git_activity(repository, "main", window)
            self.assertEqual(result["commits_by_month"]["2026-10"], 2)
            self.assertEqual(sum(result["commits_by_month"].values()), 2)
            self.assertEqual(result["last_commit_at"], "2026-10-09T12:00:00+00:00")
            self.assertEqual(result["workflow_files"], [])


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
            root = Path(temporary)
            data = root / "stats/data.json"
            data.parent.mkdir(parents=True)
            data.write_text("previous snapshot\n")
            svg = root / "assets/project-statistics/overview.svg"
            svg.parent.mkdir(parents=True)
            svg.write_text("previous SVG\n")
            renderer = types.ModuleType("render_project_statistics")
            renderer.render = lambda snapshot: {"overview.svg": "<svg/>"}
            with patch.dict(sys.modules, {"render_project_statistics": renderer}):
                with self.assertRaises(statistics.CollectionError):
                    statistics.publish({}, root)
            self.assertEqual(data.read_text(), "previous snapshot\n")
            self.assertEqual(svg.read_text(), "previous SVG\n")


if __name__ == "__main__":
    unittest.main()
