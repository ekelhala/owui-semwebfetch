"""
title: Web fetch tool.
description: A tool for precise and token-efficient retrieval of web content, with the help of semantic search.
author: ekelhala
version: 0.2
"""

import requests
from typing import Union, List
from pydantic import BaseModel, Field

class Tools:
    """
    Thin wrapper around the web fetch HTTP API.
    """

    class Valves(BaseModel):
        base_url: str = Field(
            default="http://web-fetch:8000",
            description="Base URL of the sidecar service (HTTP endpoint).",
        )
        chunk_size: int = Field(
            default=800,
            description="Size of each text chunk (in characters).",
        )
        overlap: int = Field(
            default=150,
            description="Number of characters that overlap between consecutive chunks.",
        )
        min_score: float = Field(
            default=0.25,
            description="Minimum similarity score to keep a chunk.",
        )

    def __init__(self):
        """
        Initialise the tool.  All configuration values are read from the
        Open-WebUI Valves.  The valve defaults are the same as the
        service constants.
        """
        self.valves = self.Valves()

    # ------------------------------------------------------------------ #
    def fetch_and_semantic_search(
        self,
        urls: Union[str, List[str]],
        search_query: str,
        top_k: int = 3,
    ) -> str:
        """
        Fetch one or more URLs, perform a semantic ranking of text chunks
        and return the most relevant pieces in clean Markdown.

        Args:
            urls: str or list[str]
                One or more target URLs to fetch. If a single string is given,
                it is treated as a one-element list.
            search_query: str
                The user's question or keyword that drives the semantic comparison.
            top_k: int, default=3
                Number of top-scoring chunks to include in the output.

        Returns:
            str
                Markdown text that lists, for each selected chunk:
                * the source URL,
                * the cosine-similarity score (rounded to two decimals), and
                * the chunk itself.
                If fetching any URL fails, the function continues processing the rest
                and appends a succinct error line to the final output.
        """
        # Build the request URL from the valve
        base_url = self.valves.base_url.rstrip("/")
        payload = {
            "urls": urls,
            "search_query": search_query,
            "top_k": top_k,
            # Pass the valve values
            "chunk_size": self.valves.chunk_size,
            "overlap": self.valves.overlap,
            "min_score": self.valves.min_score,
        }
        try:
            resp = requests.post(f"{base_url}/semantic-search", json=payload, timeout=60)
            resp.raise_for_status()
            return resp.text
        except Exception as exc:
            return f"Error contacting fetch service: {exc}"