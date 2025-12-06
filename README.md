# MCP-Agent

A FastMCP server providing search and wiki tools for AI agents.

## Features

- **`/search`** - Search the web using DuckDuckGo
- **`/wiki`** - Search and retrieve Wikipedia article summaries

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the MCP server:

```bash
python main.py
```

Or run with FastMCP CLI:

```bash
fastmcp run main.py
```

## Tools

### search

Search for information using DuckDuckGo.

**Parameters:**
- `query` (str): The search query string

**Returns:** Search results as text

### wiki

Search Wikipedia and return a summary of the article.

**Parameters:**
- `query` (str): The topic to search for on Wikipedia
- `sentences` (int, optional): Number of sentences to return (default: 3)

**Returns:** Wikipedia article summary or search suggestions

## Dependencies

- fastmcp>=2.13.0
- wikipedia>=1.4.0
- requests>=2.31.0
- beautifulsoup4>=4.12.0