# toonarmycaptain's blog

Source for [blog.toonarmycaptain.com](https://blog.toonarmycaptain.com/).

Spotted a mistake, or have a suggestion? Please
[open an issue](https://github.com/toonarmycaptain/toonarmycaptain_blog_posts/issues).

## Notes

Built with [Zensical](https://zensical.org/). The header, footer, and RSS feed image aren't kept in
this repo:`scripts/generate_header_footer.py` grabs them from the `master` branch of
[toonarmycaptain_website](https://github.com/toonarmycaptain/toonarmycaptain_website), and the blog
rebuilds automatically when changes are pushed to it.

Serve locally, at <http://localhost:8000>:

```shell
uv sync
uv run python scripts/generate_header_footer.py
uv run zensical serve
```

Rerun `generate_header_footer.py` after the website's header or footer changes. To try website
changes before pushing them, add `--website ../toonarmycaptain_website` to use a local checkout.

After building, the deploy runs `scripts/add_itunes_image.py`, which copies the RSS feed's image
into the `<itunes:image>` tag podcast apps look for. The local preview's feed doesn't have it.

Posts live in `docs/posts/<slug>/<slug>.md`, with images beside them. Front matter:

```yaml
---
title: "My post"
description: "One sentence, for search results and RSS."
date: 2026-10-17
slug: my-post
categories: [Python]
tags: [pytest]
draft: true
---
```

- `draft: true` keeps a post off the built site but shows it in the local preview.
- Put `<!-- more -->` where the home page excerpt should end.
- Start headings at `##`; the title is the `#`.

Lint runs on commit once set up with `uv run pre-commit install --allow-missing-config`.
`uv run pymarkdown fix -r docs/posts` fixes most of what it flags.
