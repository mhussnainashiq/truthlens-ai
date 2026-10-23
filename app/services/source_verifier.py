
import logging
from urllib.parse import urlparse

import httpx

from app.config import get_settings


logger = logging.getLogger(__name__)

TAVILY_SEARCH_URL = "https://api.tavily.com/search"
MAX_CLAIMS_TO_SEARCH = 5
MAX_RESULTS_PER_CLAIM = 5


async def verify_sources(claims: list[str]) -> dict:
    """
    Search the web for candidate sources related to claims.

    Search results are leads for review, not proof that a claim
    is true or false.
    """
    settings = get_settings()

    if not settings.tavily_api_key:
        return {
            "performed": False,
            "results_by_claim": {},
            "message": (
                "Web search was not performed because no Tavily API "
                "key is configured."
            ),
        }

    if not claims:
        return {
            "performed": False,
            "results_by_claim": {},
            "message": "No claims were available to search.",
        }

    results_by_claim = {}
    searched_count = 0

    timeout = max(1, min(settings.request_timeout_seconds, 30))

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            for claim in claims[:MAX_CLAIMS_TO_SEARCH]:
                response = await client.post(
                    TAVILY_SEARCH_URL,
                    json={
                        "api_key": settings.tavily_api_key,
                        "query": claim,
                        "search_depth": "basic",
                        "topic": "general",
                        "max_results": MAX_RESULTS_PER_CLAIM,
                        "include_answer": False,
                    },
                )

                response.raise_for_status()
                payload = response.json()
                searched_count += 1

                clean_results = []

                for item in payload.get("results", []):
                    url = item.get("url", "")
                    title = item.get("title", "")
                    content = item.get("content", "")

                    if not isinstance(url, str) or not url.startswith(
                        ("https://", "http://")
                    ):
                        continue

                    if not isinstance(title, str) or not title.strip():
                        continue

                    if not isinstance(content, str):
                        content = ""

                    parsed = urlparse(url)
                    publisher = parsed.hostname or "Unknown publisher"

                    clean_results.append(
                        {
                            "title": title[:500],
                            "publisher": publisher,
                            "url": url,
                            "finding": content[:2000],
                            "relevance": (
                                "Search relevance score: "
                                + str(item.get("score", "unavailable"))
                            ),
                            "publication_date": item.get(
                                "published_date"
                            ),
                        }
                    )

                results_by_claim[claim] = clean_results

    except httpx.TimeoutException:
        logger.warning("Tavily search timed out.")
        return {
            "performed": False,
            "results_by_claim": results_by_claim,
            "message": (
                "Web search timed out. Some claims may not have been "
                "searched; retrieved results, if any, are incomplete."
            ),
        }

    except httpx.HTTPStatusError as exc:
        logger.warning(
            "Tavily returned HTTP status %s.",
            exc.response.status_code,
        )
        return {
            "performed": False,
            "results_by_claim": results_by_claim,
            "message": (
                "Tavily rejected or could not process the search request. "
                "Check your API key, account limits, and service status."
            ),
        }

    except (httpx.HTTPError, ValueError):
        logger.warning("Tavily search request failed.")
        return {
            "performed": False,
            "results_by_claim": results_by_claim,
            "message": (
                "Web search could not be completed. Please try again later."
            ),
        }

    total_results = sum(
        len(items) for items in results_by_claim.values()
    )

    if total_results == 0:
        message = (
            "Web search completed, but no usable results were returned. "
            "The claims remain unverified."
        )
    else:
        message = (
            f"Web search completed for {searched_count} claim(s) and "
            f"returned {total_results} candidate source(s). "
            "The sources have not been independently validated."
        )

    return {
        "performed": True,
        "results_by_claim": results_by_claim,
        "message": message,
    }
