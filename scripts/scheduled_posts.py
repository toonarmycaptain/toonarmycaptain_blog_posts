# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""
List scheduled posts, for deploy.yml and publish_scheduled_posts.yml.

The build leaves future-dated posts out (draft_if_future_date in zensical.toml), so a post only goes
live with the first deploy that starts after its date.

`upcoming` prints the future-dated posts, one per line, and nothing if there are none. Each deploy
runs it to turn publish_scheduled_posts.yml on while there are any, and off once there are none:

    uv run scripts/scheduled_posts.py upcoming

`due` prints the posts dated after a given time and up to now. publish_scheduled_posts.yml passes
the time the last deploy started, and deploys if this prints anything:

    uv run scripts/scheduled_posts.py due 2026-10-20T11:04:12Z

With --wait, `due` also looks that many minutes ahead, and if a post is due by then, waits until it
is before printing. The workflow uses this so the deploy starts at the post's time:

    uv run scripts/scheduled_posts.py due 2026-10-20T11:04:12Z --wait 30

Dates without a time zone are read as UTC, like the build does on GitHub's runners. Drafts are
skipped.

The block at the top makes uv run install only PyYAML, so the workflows don't need the whole
project. PyYAML's version matches uv.lock, where it comes in with Zensical. requires-python is
lower than the project's so uv uses the runner's own Python rather than downloading one.
"""
import argparse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from time import sleep

import yaml

POSTS_DIR = Path(__file__).resolve().parent.parent / 'docs' / 'posts'
END_OF_TIME = datetime.max.replace(tzinfo=timezone.utc)


def to_utc(value: date | str) -> datetime:
    """
    Return a date, datetime or ISO string as an aware datetime, reading one without a zone as UTC.

    PyYAML reads `2026-10-17` as a date and `2026-10-17 09:00:00` as a datetime, but
    `2026-10-17 09:00` as a string, as YAML timestamps need seconds. This takes any of them.
    """
    time = datetime.fromisoformat(str(value))
    return time if time.tzinfo else time.replace(tzinfo=timezone.utc)


def post_date(post: str) -> datetime | None:
    """Return the date in a post's front matter, or None for a draft or a post without one."""
    if not post.startswith('---\n'):
        return None
    front_matter = yaml.safe_load(post.split('---\n', 2)[1]) or {}
    if front_matter.get('draft') or 'date' not in front_matter:
        return None
    return to_utc(front_matter['date'])


def posts_dated(after: datetime, until: datetime) -> list[tuple[datetime, Path]]:
    """Return the posts dated after `after` and up to `until`, with their dates, earliest first."""
    posts = ((post_date(path.read_text()), path) for path in POSTS_DIR.rglob('*.md'))
    return sorted((dated, path) for dated, path in posts if dated and after < dated <= until)


def main() -> None:
    """Parse arguments, wait for a due post if asked to, and print the posts."""
    parser = argparse.ArgumentParser(description='List scheduled posts.')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('upcoming', help='Print the future-dated posts.')
    due = commands.add_parser('due', help='Print the posts dated after a time and up to now.')
    due.add_argument('since', type=to_utc, help='ISO time; posts dated after it count.')
    due.add_argument(
        '--wait',
        type=int,
        default=0,
        metavar='MINUTES',
        help='Also wait for the first post due within this many minutes.',
    )
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    if args.command == 'upcoming':
        posts = posts_dated(now, END_OF_TIME)
    else:
        soon = posts_dated(args.since, now + timedelta(minutes=args.wait))
        if soon:
            sleep(max(0.0, (soon[0][0] - now).total_seconds()))
        posts = posts_dated(args.since, datetime.now(timezone.utc))
    for _, path in posts:
        print(path.relative_to(POSTS_DIR))


if __name__ == '__main__':
    main()