#!/usr/bin/env python3
"""List ELITEA API folders or requests.

Usage:
  scripts/list.py                       # top-level folders with counts
  scripts/list.py --folder NAME         # requests inside a folder (fuzzy match)
  scripts/list.py --all                 # flat list of every request
  scripts/list.py --folders             # every folder (nested), with counts
  scripts/list.py --json                # machine-readable

Matching is case-insensitive and substring-based. Folder paths use "/".
"""
from __future__ import annotations

import argparse
import json
import sys

from _collection import (
    folder_path_str,
    iter_folders,
    iter_requests,
    load,
    request_url,
)


def count_requests(items: list) -> int:
    return sum(1 for _ in iter_requests(items))


def cmd_top(c: dict, as_json: bool) -> None:
    top = c.get("item", [])
    rows = []
    for it in top:
        if "item" in it:
            rows.append({"name": it.get("name"), "kind": "folder", "requests": count_requests(it["item"])})
        else:
            r = it.get("request", {})
            rows.append({"name": it.get("name"), "kind": "request", "method": r.get("method")})
    if as_json:
        print(json.dumps(rows, indent=2))
        return
    for r in rows:
        if r["kind"] == "folder":
            print(f"[F] {r['name']:<24}  {r['requests']} requests")
        else:
            print(f"[R] {r['name']:<24}  {r.get('method','')}")


def cmd_folder(c: dict, query: str, as_json: bool) -> None:
    q = query.lower()
    hits: list[tuple[list[str], dict]] = []
    for path, folder in iter_folders(c.get("item", [])):
        if q in folder_path_str(path).lower() or q == folder.get("name", "").lower():
            hits.append((path, folder))

    if not hits:
        print(f"no folder matched {query!r}", file=sys.stderr)
        sys.exit(1)

    # Prefer shortest/most specific match if there are multiple
    hits.sort(key=lambda h: (len(h[0]), h[0]))
    path, folder = hits[0]
    if len(hits) > 1:
        print(
            f"note: {len(hits)} folders matched {query!r}; using {folder_path_str(path)!r}. "
            f"Others: {[folder_path_str(p) for p,_ in hits[1:6]]}",
            file=sys.stderr,
        )

    rows = []
    for subpath, req in iter_requests(folder.get("item", []), list(path)):
        r = req.get("request", {})
        rows.append({
            "path": folder_path_str(subpath) + "/" + req.get("name", ""),
            "method": r.get("method"),
            "url": request_url(req),
        })

    if as_json:
        print(json.dumps(rows, indent=2))
        return
    for r in rows:
        print(f"{(r['method'] or ''):<6} {r['path']}")
        print(f"       {r['url']}")


def cmd_all(c: dict, as_json: bool) -> None:
    rows = []
    for path, req in iter_requests(c.get("item", [])):
        r = req.get("request", {})
        rows.append({
            "path": folder_path_str(path) + "/" + req.get("name", ""),
            "method": r.get("method"),
            "url": request_url(req),
        })
    if as_json:
        print(json.dumps(rows, indent=2))
        return
    for r in rows:
        print(f"{(r['method'] or ''):<6} {r['path']}")


def cmd_folders(c: dict, as_json: bool) -> None:
    rows = []
    for path, folder in iter_folders(c.get("item", [])):
        rows.append({
            "path": folder_path_str(path),
            "requests": count_requests(folder.get("item", [])),
        })
    if as_json:
        print(json.dumps(rows, indent=2))
        return
    for r in rows:
        print(f"{r['requests']:>4}  {r['path']}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--folder", help="fuzzy match a folder and list its requests")
    p.add_argument("--all", action="store_true", help="flat list of every request")
    p.add_argument("--folders", action="store_true", help="every folder, nested")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args()

    c = load()
    if args.folder:
        cmd_folder(c, args.folder, args.json)
    elif args.all:
        cmd_all(c, args.json)
    elif args.folders:
        cmd_folders(c, args.json)
    else:
        cmd_top(c, args.json)


if __name__ == "__main__":
    main()
