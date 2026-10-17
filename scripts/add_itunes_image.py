"""
Add an <itunes:image> to the built RSS feeds, for podcast apps.

The feeds' image, set in zensical.toml, is a plain RSS <image>. Podcast apps look for <itunes:image>
first, and some ignore <image>. Zensical can't write <itunes:image>, so this copies the <image>'s URL
into one in the feeds in site/, after the build:

    uv run zensical build
    uv run python scripts/add_itunes_image.py
"""
import re
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent / 'site'
ITUNES_NAMESPACE = 'xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"'


def add_itunes_image(feed: str) -> str:
    """Return the feed with an <itunes:image> after its <image>, with the same URL."""
    image = re.search(r'<image>\s*<url>([^<]*)</url>.*?</image>', feed, re.DOTALL)
    if not image:
        raise SystemExit('No <image> in the feed. Is the rss plugin\'s image set in zensical.toml?')
    if '<rss ' not in feed:
        raise SystemExit('No <rss> element in the feed.')
    # Already escaped by Zensical, and fine in an attribute as it is: a URL can't contain a quote.
    feed = feed[:image.end()] + f'<itunes:image href="{image.group(1)}" />' + feed[image.end():]
    return feed.replace('<rss ', f'<rss {ITUNES_NAMESPACE} ', 1)


if __name__ == '__main__':
    feeds = sorted(SITE_DIR.glob('feed_rss_*.xml'))
    if not feeds:
        raise SystemExit(f'No RSS feeds in {SITE_DIR}. Run zensical build first.')
    for path in feeds:
        feed = path.read_text()
        if '<itunes:image ' in feed:
            print(f'{path.name} already has an <itunes:image>.')
            continue
        path.write_text(add_itunes_image(feed))
        print(f'Added an <itunes:image> to {path.name}.')
