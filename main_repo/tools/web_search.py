"""
Web Search Tool
Searches the web for Bangladesh data using DuckDuckGo (free, no API key needed).
Returns a ranked list of results with titles, URLs, and snippets.
"""
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from ddgs import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential


class WebSearchInput(BaseModel):
    query: str = Field(
        description=(
            "The search query. Be specific — include source names for best results. "
            "Examples: 'Bangladesh education budget GDP percentage UNESCO 2023', "
            "'BBS Bangladesh poverty rate 2022 site:bbs.gov.bd'"
        )
    )
    max_results: int = Field(
        default=8,
        description="Maximum number of search results to return (default 8, max 15)"
    )


class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = (
        "Searches the internet for Bangladesh data and returns a list of relevant sources. "
        "Use this first to discover which URLs contain the data you need, "
        "then use 'Fetch Web Page' to read the actual content. "
        "Tip: include source names in your query for best results "
        "(e.g., 'site:data.worldbank.org Bangladesh GDP 2023'). "
        "Input: a search query string."
    )
    args_schema: Type[BaseModel] = WebSearchInput

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
    def _run(self, query: str, max_results: int = 8) -> str:
        try:
            max_results = min(max_results, 15)  # cap at 15

            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))

            if not results:
                return f"[NO RESULTS] No search results found for query: '{query}'. Try a different query."

            formatted = [f"[SEARCH RESULTS for: '{query}']\n"]
            for i, r in enumerate(results, 1):
                formatted.append(
                    f"{i}. {r.get('title', 'No title')}\n"
                    f"   URL: {r.get('href', 'No URL')}\n"
                    f"   Snippet: {r.get('body', 'No snippet')[:300]}\n"
                )

            return "\n".join(formatted)

        except Exception as e:
            return (
                f"[ERROR] Web search failed for query '{query}': {str(e)}. "
                "Try rephrasing the query or use 'Fetch Web Page' with a known URL."
            )
