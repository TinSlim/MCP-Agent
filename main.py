"""
MCP Agent Server with FastMCP

This server provides two tools:
- search: Perform a web search query
- wiki: Search and retrieve Wikipedia articles
"""

from fastmcp import FastMCP
import wikipedia
import requests


# Create the MCP server
mcp = FastMCP(
    name="MCP-Agent",
    version="1.0.0",
    instructions="MCP Agent providing search and wiki tools"
)


@mcp.tool
def search(query: str) -> str:
    """
    Search for information using DuckDuckGo.
    
    Args:
        query: The search query string
        
    Returns:
        Search results as text
    """
    try:
        # Use DuckDuckGo HTML search
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.post(url, data={"q": query}, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse basic results from HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for result in soup.select('.result')[:5]:  # Get top 5 results
            title_elem = result.select_one('.result__title')
            snippet_elem = result.select_one('.result__snippet')
            
            if title_elem and snippet_elem:
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True)
                results.append(f"**{title}**\n{snippet}")
        
        if results:
            return "\n\n".join(results)
        else:
            return f"No results found for: {query}"
            
    except requests.RequestException as e:
        return f"Search error: {str(e)}"
    except Exception as e:
        return f"Error performing search: {str(e)}"


@mcp.tool
def wiki(query: str, sentences: int = 3) -> str:
    """
    Search Wikipedia and return a summary of the article.
    
    Args:
        query: The topic to search for on Wikipedia
        sentences: Number of sentences to return in the summary (default: 3)
        
    Returns:
        Wikipedia article summary or search suggestions
    """
    try:
        # Search Wikipedia
        search_results = wikipedia.search(query, results=5)
        
        if not search_results:
            return f"No Wikipedia articles found for: {query}"
        
        # Try to get summary for the first result
        try:
            page = wikipedia.page(search_results[0])
            summary = wikipedia.summary(search_results[0], sentences=sentences)
            
            return f"**{page.title}**\n\nURL: {page.url}\n\n{summary}"
            
        except wikipedia.DisambiguationError as e:
            # Return disambiguation options
            options = e.options[:5]  # Limit to 5 options
            options_text = "\n".join(f"- {opt}" for opt in options)
            return f"Multiple articles found for '{query}'. Please be more specific:\n\n{options_text}"
            
        except wikipedia.PageError:
            # Return search suggestions if page not found
            suggestions = "\n".join(f"- {s}" for s in search_results)
            return f"Article not found. Did you mean:\n\n{suggestions}"
            
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"


if __name__ == "__main__":
    # Run the server
    mcp.run()
