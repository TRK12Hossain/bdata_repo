"""
PDF Reader Tool
Downloads and extracts text from PDF files (BBS reports, World Bank PDFs, etc.).
Handles both URL-based PDFs and local file paths.
"""
import io
import os
import tempfile
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests
import pdfplumber
from tenacity import retry, stop_after_attempt, wait_exponential


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Max characters to extract (keeps token usage in budget)
MAX_CHARS = 10000


class ReadPDFInput(BaseModel):
    source: str = Field(
        description=(
            "Either a URL to a PDF file (starting with http/https) "
            "or a local file path to a PDF. "
            "Examples: 'https://www.bbs.gov.bd/report.pdf' or '/tmp/report.pdf'"
        )
    )
    page_range: str = Field(
        default="all",
        description=(
            "Pages to extract. Use 'all' for entire document, "
            "or specify like '1-5' for pages 1 through 5, "
            "or '3' for a single page. Useful for large PDFs."
        )
    )


class ReadPDFTool(BaseTool):
    name: str = "Read PDF"
    description: str = (
        "Downloads and extracts text from a PDF file — either from a URL or local path. "
        "Use this for BBS Statistical Yearbooks, World Bank reports, UNESCO publications, "
        "or any other data source that is a PDF. "
        "Specify page_range to limit extraction for large documents (saves tokens). "
        "Returns extracted text with table data when detectable."
    )
    args_schema: Type[BaseModel] = ReadPDFInput

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _run(self, source: str, page_range: str = "all") -> str:
        try:
            # Determine if URL or local file
            if source.startswith("http://") or source.startswith("https://"):
                pdf_bytes = self._download_pdf(source)
                label = source
            elif os.path.exists(source):
                with open(source, "rb") as f:
                    pdf_bytes = f.read()
                label = source
            else:
                return f"[ERROR] Source '{source}' is neither a valid URL nor an existing file path."

            # Parse page range
            pages_to_extract = self._parse_page_range(page_range)

            # Extract text
            text = self._extract_text(pdf_bytes, pages_to_extract, label)
            return text

        except Exception as e:
            return (
                f"[ERROR] Failed to read PDF from '{source}': {str(e)}. "
                "Try fetching the parent webpage instead, or search for an HTML version of this data."
            )

    def _download_pdf(self, url: str) -> bytes:
        response = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        response.raise_for_status()
        return response.content

    def _parse_page_range(self, page_range: str):
        if page_range.lower() == "all":
            return None  # None means all pages
        if "-" in page_range:
            start, end = page_range.split("-")
            return list(range(int(start) - 1, int(end)))  # 0-indexed
        return [int(page_range) - 1]  # single page, 0-indexed

    def _extract_text(self, pdf_bytes: bytes, pages: list, label: str) -> str:
        extracted_parts = [f"[PDF SOURCE: {label}]\n"]

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            total_pages = len(pdf.pages)
            page_indices = pages if pages is not None else range(total_pages)

            extracted_parts.append(f"Total pages in document: {total_pages}\n")
            if pages:
                extracted_parts.append(f"Extracting pages: {[p+1 for p in page_indices]}\n\n")
            else:
                extracted_parts.append(f"Extracting all pages\n\n")

            total_chars = 0
            for i in page_indices:
                if i >= total_pages:
                    break

                page = pdf.pages[i]
                page_num = i + 1

                # Extract plain text
                page_text = page.extract_text() or ""

                # Try to extract tables too
                tables = page.extract_tables()
                table_text = ""
                if tables:
                    for table in tables:
                        table_text += "\n[TABLE]\n"
                        for row in table:
                            clean_row = [str(cell or "").strip() for cell in row]
                            table_text += " | ".join(clean_row) + "\n"
                        table_text += "[/TABLE]\n"

                page_content = f"--- Page {page_num} ---\n{page_text}\n{table_text}"
                extracted_parts.append(page_content)

                total_chars += len(page_content)
                if total_chars > MAX_CHARS:
                    extracted_parts.append(
                        f"\n[... extraction stopped at page {page_num} to stay within token budget. "
                        "Use page_range parameter to extract specific sections of this document ...]"
                    )
                    break

        return "\n".join(extracted_parts)
