# Project statistics

Statistics cover the featured repositories in [projects.json](projects.json). The snapshot and charts describe the projects, with source repositories and support forks counted separately.

[Snapshot data](https://github.com/naelolaiz/naelolaiz/blob/project-statistics/data.json) · [Generator](../scripts/update_project_statistics.py) · [Refresh workflow](../.github/workflows/project-statistics.yml)

## What the charts measure

- **Project overview:** featured repositories, original source repositories, support forks, and source repositories containing GitHub Actions workflow files.
- **Languages:** detected-language count and GitHub-reported code bytes across source repositories' default branches. The bars show language proportions and how many repositories contain each language. These measure code composition; they do not measure proficiency or time spent.
- **Activity:** non-merge commits reachable from source repositories' default branches, grouped by committer date into the latest 12 calendar months in Europe/Madrid. All contributors and automation are included. The current month is partial.
- **Recent activity:** source repositories whose latest default-branch commit falls within the last 90 days.
- **Workflows:** presence of `.github/workflows/*.yml` or `*.yaml` files. This count does not indicate that tests exist or that CI is passing.

The PlatformIO, Espressif Linux and Sipeed SDK forks are included in the project count, while their languages and inherited commit history are excluded from aggregate source statistics. Private repositories and account-wide contribution metrics are outside this snapshot.

GitHub's language detection uses [Linguist](https://github.com/github-linguist/linguist/blob/main/docs/how-linguist-works.md) and repository attributes, including generated/vendored-file rules. [The language API](https://docs.github.com/en/rest/repos/repos#list-repository-languages) supplies byte counts. Activity and workflow presence come from the public default-branch Git trees.

## Refresh

The workflow refreshes the snapshot daily, and when the README, configuration, scripts, tests or workflow change on the default branch. The tests run first on every trigger and on pull requests; a failing test stops the refresh. It publishes `data.json` and the three SVG views as a single commit on the [`project-statistics`](https://github.com/naelolaiz/naelolaiz/tree/project-statistics) branch, replaced on every refresh, so the default branch history carries no refresh commits. The README embeds the views from that branch. A failed collection publishes nothing and leaves the last complete snapshot in place; its "Updated" date then shows how old it is.

Manual runs on other branches are dry runs: they collect and render the snapshot, keep it as a workflow artifact, and publish nothing.

A local refresh uses Python 3 and Git, and writes to `build/project-statistics/` unless `--output` names another directory:

```sh
python3 scripts/update_project_statistics.py --config stats/projects.json
```

The optional `GITHUB_TOKEN` environment variable raises the GitHub API allowance. The workflow supplies its repository token automatically. Git history is cached outside the checkout, and bare caches are accessed explicitly so the collector works with Git's `safe.bareRepository=explicit` setting. Only aggregate metrics are published, with no author names or email addresses.

To redraw the charts from an existing snapshot, such as the published `data.json`:

```sh
python3 scripts/update_project_statistics.py --input data.json --output build/project-statistics
```
