"""
A Markdown extension that makes links to other sites open in a new tab.

Adds target="_blank" rel="noopener noreferrer" to every http(s) link in a post when the blog is
built, so the posts don't need {:target="_blank" rel="noopener noreferrer"} after each link. Listed
in zensical.toml's markdown_extensions as external_links.

A link's own attributes win: {:target="_self"} after a link keeps it in the same tab. Links written
as raw HTML (<a href="...">) are left as they are.
"""
from urllib.parse import urlparse
from xml.etree.ElementTree import Element

from markdown import Extension, Markdown
from markdown.treeprocessors import Treeprocessor

ATTRIBUTES = {'target': '_blank', 'rel': 'noopener noreferrer'}


class ExternalLinksTreeprocessor(Treeprocessor):
    def run(self, root: Element) -> None:
        for link in root.iter('a'):
            if urlparse(link.get('href', '')).scheme in ('http', 'https'):
                for name, value in ATTRIBUTES.items():
                    if link.get(name) is None:
                        link.set(name, value)


class ExternalLinksExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        # After inline (20), which makes the links, and attr_list (8), which sets a link's own attributes.
        md.treeprocessors.register(ExternalLinksTreeprocessor(md), 'external_links', 7)


def makeExtension(**kwargs) -> ExternalLinksExtension:
    """Entry point Python-Markdown calls for the extension named external_links."""
    return ExternalLinksExtension(**kwargs)