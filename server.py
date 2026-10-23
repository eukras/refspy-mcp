"""MCP server that identifies Bible references in text using refspy."""

from functools import lru_cache
from typing import Literal

from mcp.server.mcpserver import MCPServer
from refspy import refspy
from refspy.manager import Manager

mcp = MCPServer("refspy")

Canon = Literal["protestant", "catholic", "orthodox"]
Locale = Literal["en_US", "fr_FR"]


@lru_cache
def get_manager(canon: Canon, locale: Locale) -> Manager:
    return refspy(canon, locale)


@mcp.tool()
def find_bible_references(
    text: str,
    canon: Canon = "protestant",
    locale: Locale = "en_US",
    include_books: bool = False,
) -> list[dict[str, str]]:
    """Find Bible references in text, e.g. "Rom 3:23", "Matt 5:3,7-9".

    Partial references are resolved from context, so in "see Rom 3:23 and
    5:8" the second match is Romans 5:8.

    Args:
        text: The text to search.
        canon: Which books to recognise; catholic and orthodox add the
            Deuterocanonical books.
        locale: Language of book names and reference syntax.
        include_books: Also match bare book names such as "Genesis".

    Returns:
        One entry per match, in order: the matched text, and the reference
        as a full and abbreviated name.
    """
    manager = get_manager(canon, locale)
    return [
        {
            "match": match,
            "name": manager.name(ref) if ref is not None else "",
            "abbrev_name": manager.abbrev_name(ref) if ref is not None else "",
        }
        for match, ref in manager.find_references(text, include_books=include_books)
    ]


def find_refs(text: str, canon: Canon, locale: Locale) -> tuple[Manager, list]:
    manager = get_manager(canon, locale)
    return manager, [ref for _, ref in manager.find_references(text)]


@mcp.tool()
def summarize_bible_references(
    text: str,
    canon: Canon = "protestant",
    locale: Locale = "en_US",
) -> str | None:
    """Summarize the Bible references in text as a sorted, combined list,
    with overlapping and adjacent references merged, e.g.
    "Rom 3:23; 5:8; 1 Cor 13".

    Args:
        text: The text to search.
        canon: Which books to recognise; catholic and orthodox add the
            Deuterocanonical books.
        locale: Language of book names and reference syntax.

    Returns:
        The summary, or null if no references were found.
    """
    manager, refs = find_refs(text, canon, locale)
    return manager.make_summary(refs)


@mcp.tool()
def index_bible_references(
    text: str,
    canon: Canon = "protestant",
    locale: Locale = "en_US",
) -> str | None:
    """Index the Bible references in text as a sorted one-line list,
    without merging overlapping references.

    Args:
        text: The text to search.
        canon: Which books to recognise; catholic and orthodox add the
            Deuterocanonical books.
        locale: Language of book names and reference syntax.

    Returns:
        The index, or null if no references were found.
    """
    manager, refs = find_refs(text, canon, locale)
    return manager.make_index(refs)


@mcp.tool()
def find_bible_hotspots(
    text: str,
    canon: Canon = "protestant",
    locale: Locale = "en_US",
    max_chapters: int = 7,
    min_references: int = 2,
) -> list[dict[str, str | int]]:
    """Find the most referenced chapters (hotspots) in text.

    Args:
        text: The text to search.
        canon: Which books to recognise; catholic and orthodox add the
            Deuterocanonical books.
        locale: Language of book names and reference syntax.
        max_chapters: The maximum number of chapters to return.
        min_references: The minimum references for a chapter to qualify.

    Returns:
        Chapters in descending order of reference count.
    """
    manager, refs = find_refs(text, canon, locale)
    return [
        {"chapter": manager.abbrev_name(ref), "count": count}
        for ref, count in manager.make_hotspot_tuples(
            refs, max_chapters, min_references
        )
    ]


if __name__ == "__main__":
    mcp.run()
