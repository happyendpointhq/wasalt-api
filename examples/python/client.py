"""Minimal client for the Wasalt Saudi Data API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os

import requests

HOST = "wasalt-saudi-data.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` part of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def pages(path, key, max_pages=None, **params):
    """Yield rows page by page until hasMore is false.

    Page sizes are fixed per endpoint (16 for /search-properties, 10 for /search-rentals and
    /auction-search, 25 for /auction-lots). Never page against estimatedCount: on
    /search-properties it over-reports.
    """
    page = 1
    while True:
        data = get(path, page=page, **params)
        yield from data[key]
        if not data.get("hasMore") or page == max_pages:
            return
        page += 1
