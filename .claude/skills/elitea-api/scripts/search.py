#!/usr/bin/env python3
"""Regex/substring search across the ELITEA API collection.

Scans: request names, folder paths, URLs, descriptions, header keys,
and raw request bodies. Returns matching request paths with a short
snippet showing where the match landed.

Usage:
  scripts/search.py "query"                # case-insensitive substring
  scripts/search.py -e 'pattern'           # python regex
  scripts/search.py "project" --fields url,name
  scripts/search.py "project" --json
  scripts/search.py "project" --limit 20
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from _collection import folder_path_str, iter_requests, load, request_url


FIELDS = ("name", "path", "method", "url", "description", "headers", "body")


def describe_request(path: list[str], req: dict) -> dict:
    r = req.get("request", {})
    headers = r.get("header", []) or []
    if isinstance(headers, dict):
        headers = [headers]
    body = r.get("body", {}) or {}
    body_raw = ""
    if isinstance(body, dict):
        body_raw = body.get("raw") or json.dumps(body.get("formdata") or body.get("urlencoded") or body.get("graphql") or "")
    return {
        "name": req.get("name", ""),
        "path": folder_path_str(path) + "/" + req.get("name", ""),
        "method": r.get("method", ""),
        "url": request_url(req),
        "description": r.get("description", "") or "",
        "headers": " ".join(f"{h.get('key','')}:{h.get('value','')}" for h in headers),
        "body": body_raw or "",
    }


def snippet(haystack: str, match: re.Match, pad: int = 40) -> str:
    start = max(0, match.start() - pad)
    end = min(len(haystack), match.end() + pad)
    out = haystack[start:end].replace("\n", " ")
    return ("…" if start > 0 else "") + out + ("…" if end < len(haystack) else "")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query", help="substring to find (case-insensitive) unless -e given")
    p.add_argument("-e", "--regex", action="store_true", help="treat query as a python regex")
    p.add_argument("--fields", default=",".join(FIELDS),
                   help=f"comma-separated fields to search (default: all). options: {','.join(FIELDS)}")
    p.add_argument("--limit", type=int, default=50, help="max hits to print (default 50)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args()

    fields = [f.strip() for f in args.fields.split(",") if f.strip() in FIELDS]
    if not fields:
        print(f"no valid fields: {args.fields}", file=sys.stderr)
        sys.exit(2)

    if args.regex:
        pat = re.compile(args.query, re.IGNORECASE | re.MULTILINE)
    else:
        pat = re.compile(re.escape(args.query), re.IGNORECASE)

    c = load()
    hits = []
    for path, req in iter_requests(c.get("item", [])):
        row = describe_request(path, req)
        matched_fields = []
        first_snip = None
        for f in fields:
            haystack = row[f]
            if not haystack:
                continue
            m = pat.search(haystack)
            if m:
                matched_fields.append(f)
                if first_snip is None:
                    first_snip = f"[{f}] {snippet(haystack, m)}"
        if matched_fields:
            hits.append({
                "path": row["path"],
                "method": row["method"],
                "url": row["url"],
                "fields": matched_fields,
                "snippet": first_snip,
            })

    if args.json:
        print(json.dumps({"total": len(hits), "hits": hits[: args.limit]}, indent=2))
        return

    print(f"{len(hits)} hits (showing up to {args.limit}):")
    for h in hits[: args.limit]:
        print(f"  {(h['method'] or ''):<6} {h['path']}")
        print(f"         {h['url']}")
        if h["snippet"]:
            print(f"         {h['snippet']}")
    if len(hits) > args.limit:
        print(f"... and {len(hits) - args.limit} more. Use --limit to widen.")


if __name__ == "__main__":
    main()
