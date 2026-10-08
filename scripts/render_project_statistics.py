"""Render repository statistics as standalone, accessible SVG cards.

The renderer consumes a collected snapshot and performs no network requests.
Only source repositories contribute language and activity measurements;
support forks are displayed as a separate overview count.
"""

from datetime import datetime
from html import escape
from math import ceil
from zoneinfo import ZoneInfo


WIDTH = 480
HEIGHT = 372
PALETTE = ("#159bb7", "#7c69d6", "#4386bc", "#409c95", "#a26fa6", "#708ca4", "#798792")

STYLE = """
svg { color-scheme: light dark; }
text {
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  fill: #172b3a;
}
.background { fill: #ffffff; stroke: #dce5ec; }
.muted { fill: #536775; }
.subtle { fill: #70828e; }
.rule { stroke: #e6edf2; }
.track { fill: #edf3f6; }
.activity { fill: #159bb7; }
.partial { fill: #7c69d6; stroke: #6754bd; stroke-width: 1.5; stroke-dasharray: 3 2; }
.accent { fill: #087f99; }
.empty { stroke: #b8c8d2; }
@media (prefers-color-scheme: dark) {
  text { fill: #e6edf3; }
  .background { fill: #111a24; stroke: #2b3b49; }
  .muted { fill: #acbcc8; }
  .subtle { fill: #91a5b5; }
  .rule { stroke: #2a3947; }
  .track { fill: #223341; }
  .activity { fill: #42b9d0; }
  .partial { fill: #9a87ef; stroke: #c3b4ff; }
  .accent { fill: #69cce0; }
  .empty { stroke: #586e7e; }
}
"""


def _number(value):
    return max(0, int(value or 0))


def _text(x, y, value, size=13, *, weight=400, css="", anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}"'
        f' class="{css}" text-anchor="{anchor}">{escape(str(value))}</text>'
    )


def _rect(x, y, width, height, *, radius=0, css="", fill=None):
    color = f' fill="{escape(fill, quote=True)}"' if fill else ""
    return (
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{width:.2f}"'
        f' height="{height:.2f}" rx="{radius}" class="{css}"{color}/>'
    )


def _line(x1, y1, x2, y2, css="rule"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{css}"/>'


def _timestamp(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def _date(value, timezone, pattern="%d %b %Y"):
    timestamp = _timestamp(value)
    if timestamp is None:
        return "—"
    if timestamp.tzinfo is not None:
        timestamp = timestamp.astimezone(timezone)
    return timestamp.strftime(pattern)


def _snapshot_date(snapshot, timezone):
    return "Updated " + _date(snapshot.get("generated_at"), timezone)


def _card(slug, title, description, subtitle, body, snapshot, timezone):
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}"',
            f' viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="{slug}-title {slug}-desc">',
            f'<title id="{slug}-title">{escape(title)}</title>',
            f'<desc id="{slug}-desc">{escape(description)}</desc>',
            f"<style>{STYLE}</style>",
            _rect(1, 1, WIDTH - 2, HEIGHT - 2, radius=18, css="background"),
            _text(26, 37, title, 22, weight=650),
            _text(26, 61, subtitle, 12, css="muted"),
            *body,
            _line(26, 334, 454, 334),
            _text(26, 355, _snapshot_date(snapshot, timezone), 11, css="subtle"),
            _text(454, 355, "Featured project index", 11, css="subtle", anchor="end"),
            "</svg>",
        ]
    )


def _overview(snapshot, timezone):
    summary = snapshot.get("summary", {})
    featured = _number(summary.get("featured_repositories"))
    sources = _number(summary.get("source_repositories"))
    forks = _number(summary.get("support_forks"))
    workflows = _number(summary.get("repositories_with_workflows"))
    active = _number(summary.get("active_repositories_90_days"))
    body = []
    for x, count, label in (
        (26, featured, "Featured repositories"),
        (190, sources, "Source repositories"),
        (354, forks, "Support forks"),
    ):
        body.extend(
            [_text(x, 115, f"{count:,}", 34, weight=650, css="accent"), _text(x, 139, label, 11, css="muted")]
        )
    body.append(_line(26, 160, 454, 160))
    for x, count, label in (
        (26, workflows, "Sources with workflows"),
        (264, active, "Active sources · past 90 days"),
    ):
        body.extend([_text(x, 198, f"{count:,}", 25, weight=600), _text(x, 220, label, 12, css="muted")])
    body.append(_text(26, 251, "RECENT SOURCE ACTIVITY", 11, weight=650, css="subtle"))
    repositories = [
        repo
        for repo in snapshot.get("repositories", [])
        if not repo.get("fork") and _timestamp(repo.get("last_commit_at")) is not None
    ]
    repositories.sort(key=lambda repo: _timestamp(repo["last_commit_at"]).timestamp(), reverse=True)
    for y, repo in zip((275, 297, 319), repositories[:3]):
        name = str(repo.get("name", ""))
        label = name if len(name) <= 31 else name[:30] + "…"
        url = str(repo.get("url", ""))
        row = _text(26, y, label, 12, weight=500)
        if url.startswith("https://"):
            row = f'<a href="{escape(url, quote=True)}"><title>{escape(name)}</title>{row}</a>'
        body.extend([row, _text(454, y, _date(repo["last_commit_at"], timezone), 12, css="muted", anchor="end")])
    if not repositories:
        body.append(_text(26, 279, "No source commit dates in this snapshot", 12, css="muted"))
    description = (
        f"{featured} featured repositories: {sources} source repositories and {forks} support forks. "
        f"{workflows} source repositories contain workflow files; this is not a CI success metric. "
        f"{active} sources have default-branch commit activity in the past 90 days. "
        "Recent activity uses source default-branch commit dates."
    )
    return _card(
        "overview",
        "Project overview",
        description,
        "Repository scope, workflows and recent source updates",
        body,
        snapshot,
        timezone,
    )


def _languages(snapshot, timezone):
    languages = sorted(
        (language for language in snapshot.get("languages", []) if _number(language.get("bytes")) > 0),
        key=lambda language: _number(language["bytes"]),
        reverse=True,
    )
    total = sum(_number(language["bytes"]) for language in languages)
    rows = list(languages[:7])
    remaining = languages[7:]
    if remaining:
        other_names = {str(language["name"]) for language in remaining}
        repositories = snapshot.get("repositories", [])
        containing_other = sum(
            1
            for repo in repositories
            if not repo.get("fork")
            and any(_number(repo.get("languages", {}).get(name)) > 0 for name in other_names)
        )
        rows.append(
            {
                "name": "Other",
                "bytes": sum(_number(language["bytes"]) for language in remaining),
                "repositories": containing_other,
            }
        )
    body = []
    descriptions = []
    for index, language in enumerate(rows):
        y = 92 + index * 29
        name = str(language["name"])
        share = _number(language["bytes"]) / total
        percent = "<0.1%" if 0 < share < 0.001 else f"{share:.1%}"
        repo_count = _number(language.get("repositories"))
        repo_label = f"{repo_count} repo" + ("s" if repo_count != 1 else "")
        color = PALETTE[index] if index < len(PALETTE) else "#8a94a0"
        body.extend(
            [
                _text(26, y, name, 13, weight=550),
                _text(382, y, repo_label, 11, css="muted", anchor="end"),
                _text(454, y, percent, 12, weight=550, anchor="end"),
                _rect(26, y + 7, 428, 6, radius=3, css="track"),
                _rect(26, y + 7, 428 * share, 6, radius=3, fill=color),
            ]
        )
        descriptions.append(f"{name}: {share:.2%}, {repo_count} repositories")
    if not rows:
        body.append(_text(26, 112, "No language bytes in this snapshot", 13, css="muted"))
    summary = snapshot.get("summary", {})
    sources = _number(summary.get("source_repositories"))
    language_count = _number(summary.get("language_count", len(languages)))
    description = (
        f"GitHub language-byte distribution across {sources} source repositories, excluding support forks. "
        "Repository composition is not a proficiency measure. " + "; ".join(descriptions) + "."
    )
    return _card(
        "languages",
        "Language mix",
        description,
        f"{language_count} languages · GitHub bytes · {sources} source repos",
        body,
        snapshot,
        timezone,
    )


def _month(value, pattern="%b"):
    try:
        return datetime.strptime(str(value), "%Y-%m").strftime(pattern)
    except ValueError:
        return str(value)


def _activity(snapshot, timezone):
    months = list(snapshot.get("activity", []))[-12:]
    total = sum(_number(month.get("commits")) for month in months)
    peak = max((_number(month.get("commits")) for month in months), default=0)
    ceiling = max(1, ceil(peak / 4) * 4)
    body = [
        _text(26, 108, f"{total:,}", 34, weight=650, css="accent"),
        _text(26, 132, "Non-merge default-branch commits", 13, css="muted"),
        _text(454, 106, "SOURCE REPOSITORIES", 10, weight=600, css="subtle", anchor="end"),
        _text(454, 128, "Includes automation", 12, css="muted", anchor="end"),
    ]
    chart_top, chart_bottom = 177, 275
    chart_left, chart_right = 47, 454
    for fraction in (0, 0.5, 1):
        y = chart_bottom - (chart_bottom - chart_top) * fraction
        body.extend(
            [
                _line(chart_left, y, chart_right, y),
                _text(39, y + 4, f"{int(ceiling * fraction):,}", 10, css="subtle", anchor="end"),
            ]
        )
    descriptions = []
    slot_width = (chart_right - chart_left) / max(12, len(months))
    for index, month in enumerate(months):
        commits = _number(month.get("commits"))
        x = chart_left + index * slot_width + slot_width / 2
        height = (chart_bottom - chart_top) * commits / ceiling
        partial = bool(month.get("partial"))
        label = _month(month.get("month", "")) + ("*" if partial else "")
        tooltip = f"{_month(month.get('month', ''), '%B %Y')}: {commits:,} commits"
        if partial:
            tooltip += " (partial month)"
        if commits:
            bar = _rect(
                x - 10,
                chart_bottom - height,
                20,
                height,
                radius=4,
                css="partial" if partial else "activity",
            )
        else:
            bar = _line(x - 8, chart_bottom - 1, x + 8, chart_bottom - 1, "empty")
        body.extend(
            [
                f"<g><title>{escape(tooltip)}</title>{bar}</g>",
                _text(round(x, 2), chart_bottom - height - 7, f"{commits:,}", 10, css="muted", anchor="middle"),
                _text(round(x, 2), 294, label, 10, css="muted", anchor="middle"),
            ]
        )
        descriptions.append(tooltip)
    if months:
        range_label = f"{_month(months[0].get('month'), '%b %Y')} – {_month(months[-1].get('month'), '%b %Y')}"
        body.append(_text(26, 320, range_label, 11, css="subtle"))
    if any(month.get("partial") for month in months):
        body.append(_text(454, 320, "* Partial month", 11, css="subtle", anchor="end"))
    description = (
        "Monthly non-merge default-branch commit counts across source repositories, including all actors. "
        "Support-fork and generated-branch histories are excluded. " + "; ".join(descriptions) + "."
    )
    return _card(
        "activity",
        "Source activity",
        description,
        "12 months · default branches · support forks excluded",
        body,
        snapshot,
        timezone,
    )


def render(snapshot):
    """Return the three SVG card filenames and their complete SVG contents."""
    timezone = ZoneInfo(snapshot.get("timezone", "Europe/Madrid"))
    return {
        "overview.svg": _overview(snapshot, timezone),
        "languages.svg": _languages(snapshot, timezone),
        "activity.svg": _activity(snapshot, timezone),
    }
