"""Shared loader / traversal helpers for the cached ELITEA collection."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterator

CACHE = Path(__file__).resolve().parent.parent / ".cache" / "collection.json"


def load() -> dict:
    if not CACHE.exists():
        print(
            f"ERROR: no cached collection at {CACHE}. Run scripts/fetch.py first.",
            file=sys.stderr,
        )
        raise SystemExit(4)
    with CACHE.open() as f:
        return json.load(f)["collection"]


def iter_requests(items: list, path: list[str] | None = None) -> Iterator[tuple[list[str], dict]]:
    """Yield (folder_path, request_item) pairs in depth-first order."""
    path = path or []
    for it in items:
        if "item" in it:
            yield from iter_requests(it["item"], path + [it.get("name", "")])
        else:
            yield path, it


def iter_folders(items: list, path: list[str] | None = None) -> Iterator[tuple[list[str], dict]]:
    path = path or []
    for it in items:
        if "item" in it:
            new_path = path + [it.get("name", "")]
            yield new_path, it
            yield from iter_folders(it["item"], new_path)


def request_url(req: dict) -> str:
    """Reconstruct the raw URL template from a request dict."""
    r = req.get("request", {})
    url = r.get("url", {})
    if isinstance(url, str):
        return url
    if isinstance(url, dict):
        return url.get("raw") or "/".join(url.get("path", []))
    return ""


def folder_path_str(path: list[str]) -> str:
    return "/".join(p for p in path if p)
