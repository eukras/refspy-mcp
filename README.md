# refspy-mcp

An basic/experimental MCP server that identifies Bible references in text using [refspy](https://github.com/eukras/refspy).

(Made with Claude Code.)

## Tools

All tools take `text`, plus:

- `canon`: `protestant` (default), `catholic` or `orthodox`
- `locale`: `en_US` (default) or `fr_FR`

### `find_bible_references(text, ..., include_books=False)`

Set `include_books` to also match bare book names like "Genesis". Returns one
entry per match, e.g. for "See Rom 3:23 and 5:8":

```json
[
  { "match": "Rom 3:23", "name": "Romans 3:23", "abbrev_name": "Rom 3:23" },
  { "match": "5:8", "name": "Romans 5:8", "abbrev_name": "Rom 5:8" }
]
```

### `summarize_bible_references(text, ...)`

Sorted list with overlapping and adjacent references merged, e.g.
`"Rom 3:21, 23–24; 5:1–6, 8"`. Returns null if there are no references.

### `index_bible_references(text, ...)`

Sorted list without merging, e.g. `"Rom 3:21, 23, 24; 5:1–3, 2–6, 8"`.
Returns null if there are no references.

### `find_bible_hotspots(text, ..., max_chapters=7, min_references=2)`

Most referenced chapters, in descending order:

```json
[
  { "chapter": "Rom 3", "count": 3 },
  { "chapter": "Rom 5", "count": 3 }
]
```

## Usage

Works with any MCP client that can run a local (stdio) server, such as Claude
Code, Cursor, VS Code, Gemini CLI or Codex CLI. Replace `/path/to/refspy-mcp`
with where you cloned this repo.

Most clients take a config like this:

```json
{
  "mcpServers": {
    "refspy": {
      "command": "uv",
      "args": ["--directory", "/path/to/refspy-mcp", "run", "server.py"]
    }
  }
}
```

Or add it to Claude Code from the command line:

```sh
claude mcp add refspy -- uv --directory /path/to/refspy-mcp run server.py
```
