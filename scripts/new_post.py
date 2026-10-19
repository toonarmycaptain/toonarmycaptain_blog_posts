"""
Scaffold a new draft blog post.

Creates docs/posts/<slug>/<slug>.md with front matter ready to edit:

    uv run new "demo post"
    uv run new "demo post" --title "How to do a demo post"

The positional argument seeds the slug (the post's folder, filename and URL): it's slugified and a
short random suffix is always appended, so scaffolding never collides. The title defaults to that
text with its first letter capitalized; pass --title to set a different display title.

The post starts as a draft (draft: true), so it stays out of the build and the feed until you
remove that line. The date is prefilled with the current time in UTC, marked with a "# UTC" comment
since the feed reads bare datetimes as UTC (see zensical.toml's rss date_from_meta). Edit it to when
you want the post to go out: a future UTC datetime keeps it hidden until then, and the daily rebuild
(deploy.yml) releases it once that time has passed.
"""
import argparse
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parent.parent / 'docs' / 'posts'


def slugify(title: str) -> str:
    """Return a URL-friendly slug: lowercase, non-alphanumeric runs collapsed to single hyphens."""
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    if not slug:
        raise SystemExit(f'Could not make a slug from {title!r}. Pass one with --slug.')
    return slug


def front_matter(title: str, slug: str, now_utc: datetime) -> str:
    """Return the Markdown for a new draft post with the given title and slug."""
    return (
        f'---\n'
        f'title: "{title}"\n'
        f'description: ""\n'
        f'date: {now_utc:%Y-%m-%d %H:%M}  # UTC\n'
        f'slug: {slug}\n'
        f'draft: true\n'
        f'categories: []\n'
        f'tags: []\n'
        f'---\n'
        f'\n'
    )


def create_post(title: str, slug: str) -> Path:
    """Write the new post file and return its path. Refuses to overwrite an existing post."""
    path = POSTS_DIR / slug / f'{slug}.md'
    if path.exists():
        raise SystemExit(f'{path} already exists.')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front_matter(title, slug, datetime.now(timezone.utc)))
    return path


def main() -> None:
    """Parse arguments and scaffold the post. Entry point for `uv run new`."""
    parser = argparse.ArgumentParser(description='Scaffold a new draft blog post.')
    parser.add_argument(
        'slug',
        help='Seeds the URL slug (quote it if it has spaces); a random suffix is always appended.',
    )
    parser.add_argument(
        '--title',
        help='Display title (default: the slug text with its first letter capitalized).',
    )
    args = parser.parse_args()

    slug = f'{slugify(args.slug)}-{secrets.token_hex(2)}'
    title = args.title or args.slug[:1].upper() + args.slug[1:]
    post = create_post(title, slug)
    print(f'Created {post.relative_to(Path.cwd())}')


if __name__ == '__main__':
    main()
