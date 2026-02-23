"""
Web Fetch Tool
Fetches the text content of a web page for the Research and Fact-Checker agents.
Strips HTML, returns clean readable text.
"""
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
}


class FetchWebPageInput(BaseModel):
    url: str = Field(description="Full URL of the web page to fetch (must start with http or https)")


class FetchWebPageTool(BaseTool):
    name: str = "Fetch Web Page"
    description: str = (
        "Fetches and extracts the readable text content from a given URL. "
        "Use this to read data from government portals (BBS, World Bank, UNESCO), "
        "PDF landing pages, or any web source. Returns clean text stripped of HTML. "
        "Input: a single URL string."
    )
    args_schema: Type[BaseModel] = FetchWebPageInput

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _run(self, url: str) -> str:
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            # If PDF, tell the agent to use ReadPDFTool instead
            if "application/pdf" in content_type or url.lower().endswith(".pdf"):
                return (
                    f"[PDF DETECTED] The URL '{url}' points to a PDF file. "
                    "Please use the 'Read PDF' tool with this URL to extract its content."
                )

            soup = BeautifulSoup(response.text, "lxml")

            # Remove noise: scripts, styles, nav, footer
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
                tag.decompose()

            # Extract meaningful text
            text = soup.get_text(separator="\n", strip=True)

            # Collapse excessive blank lines
            lines = [line for line in text.splitlines() if line.strip()]
            clean_text = "\n".join(lines)

            # Truncate to ~8000 chars to stay within token budget
            if len(clean_text) > 8000:
                clean_text = clean_text[:8000] + "\n\n[... content truncated for token efficiency ...]"

            return f"[SOURCE: {url}]\n\n{clean_text}"

        except requests.exceptions.Timeout:
            return f"[ERROR] Request timed out for URL: {url}. Try a different source."
        except requests.exceptions.HTTPError as e:
            return f"[ERROR] HTTP {e.response.status_code} when fetching {url}. The page may be down or require login."
        except requests.exceptions.ConnectionError:
            return f"[ERROR] Could not connect to {url}. Check if the domain is correct or try an alternative source."
        except Exception as e:
            return f"[ERROR] Unexpected error fetching {url}: {str(e)}"
