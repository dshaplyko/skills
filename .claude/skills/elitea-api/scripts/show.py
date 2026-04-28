#!/usr/bin/env python3
"""Show the full details of one ELITEA request and emit a ready-to-run curl.

Usage:
  scripts/show.py "query"                 # fuzzy match a request by name or path
  scripts/show.py "auth/login"            # exact path (folder/.../name)
  scripts/show.py "query" --pick 2        # disambiguate when multiple match
  scripts/show.py "query" --json          # machine-readable
  scripts/show.py "query" --no-curl       # skip the curl block

Matching priority: exact path > substring on full path > substring on name.
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys

from _collection import folder_path_str, iter_requests, load, request_url


def find_matches(c: dict, query: str) -> list[tuple[list[str], dict]]:
    q = query.lower()
    exact, path_sub, name_sub = [], [], []
    for path, req in iter_requests(c.get("item", [])):
        full = (folder_path_str(path) + "/" + req.get("name", "")).lower()
        name = req.get("name", "").lower()
        if full == q or full.endswith("/" + q):
            exact.append((path, req))
        elif q in full:
            path_sub.append((path, req))
        elif q in name:
            name_sub.append((path, req))
    return exact or path_sub or name_sub


def extract_variables(text: str) -> set[str]:
    import re
    return set(re.findall(r"\{\{([^{}]+)\}\}", text or ""))


def to_curl(req: dict) -> str:
    """Render a readable, pasteable bash curl command.

    Each (flag, value) pair is grouped on its own continuation line so the
    output is easy to skim and edit. Only values are shell-quoted.
    """
    r = req.get("request", {})
    method = r.get("method", "GET")
    url = request_url(req)
    headers = r.get("header", []) or []
    if isinstance(headers, dict):
        headers = [headers]
    body = r.get("body") or {}

    lines: list[str] = [f"curl -X {method}"]

    for h in headers:
        if h.get("disabled"):
            continue
        key = h.get("key", "")
        val = h.get("value", "")
        if key:
            lines.append(f"-H {shlex.quote(f'{key}: {val}')}")

    if body:
        mode = body.get("mode")
        if mode == "raw" and body.get("raw"):
            if not any((h.get("key") or "").lower() == "content-type" for h in headers):
                lines.append("-H 'Content-Type: application/json'")
            lines.append(f"--data-raw {shlex.quote(body['raw'])}")
        elif mode == "formdata":
            for f in body.get("formdata", []):
                if f.get("disabled"):
                    continue
                k = f.get("key", "")
                if f.get("type") == "file":
                    src = f.get("src") or "FILE_PATH"
                    lines.append(f"-F {shlex.quote(f'{k}=@{src}')}")
                else:
                    v = f.get("value", "")
                    lines.append(f"-F {shlex.quote(f'{k}={v}')}")
        elif mode == "urlencoded":
            for f in body.get("urlencoded", []):
                if f.get("disabled"):
                    continue
                k = f.get("key", "")
                v = f.get("value", "")
                lines.append(f"--data-urlencode {shlex.quote(f'{k}={v}')}")

    lines.append(shlex.quote(url))
    return " \\\n  ".join(lines)


def render_request(path: list[str], req: dict, emit_curl: bool) -> str:
    r = req.get("request", {})
    out = []
    full_path = folder_path_str(path) + "/" + req.get("name", "")
    out.append(f"=== {full_path} ===")
    method = r.get("method", "")
    url = request_url(req)
    out.append(f"{method} {url}")
    desc = (r.get("description") or "").strip()
    if desc:
        out.append("\n-- description --")
        out.append(desc)

    # Path/query variables detected in URL object
    url_obj = r.get("url", {}) if isinstance(r.get("url"), dict) else {}
    vars_in_path = [v for v in url_obj.get("variable", []) if v.get("key")]
    if vars_in_path:
        out.append("\n-- path variables --")
        for v in vars_in_path:
            out.append(f"  :{v['key']}  = {v.get('value') or v.get('description') or '<value>'}")
    query = [q for q in url_obj.get("query", []) if q.get("key")]
    if query:
        out.append("\n-- query params --")
        for q in query:
            flag = " (disabled)" if q.get("disabled") else ""
            out.append(f"  {q['key']}={q.get('value','')}{flag}  {q.get('description') or ''}")

    headers = r.get("header", []) or []
    if isinstance(headers, dict):
        headers = [headers]
    if headers:
        out.append("\n-- headers --")
        for h in headers:
            flag = " (disabled)" if h.get("disabled") else ""
            out.append(f"  {h.get('key','')}: {h.get('value','')}{flag}")

    auth = r.get("auth")
    if auth:
        out.append("\n-- auth --")
        out.append(json.dumps(auth, indent=2))

    body = r.get("body") or {}
    if body:
        out.append("\n-- body --")
        out.append(f"mode: {body.get('mode')}")
        if body.get("mode") == "raw":
            raw = body.get("raw", "")
            lang = (body.get("options", {}) or {}).get("raw", {}).get("language", "")
            if lang:
                out.append(f"language: {lang}")
            out.append(raw)
        else:
            out.append(json.dumps(body, indent=2))

    # Collect {{vars}} anywhere in the serialized request
    serialized = json.dumps(r)
    vars_used = sorted(extract_variables(serialized))
    if vars_used:
        out.append("\n-- {{variables}} this request uses --")
        for v in vars_used:
            out.append(f"  {{{{{v}}}}}")

    responses = req.get("response") or []
    if responses:
        out.append(f"\n-- example responses ({len(responses)}) --")
        for ex in responses[:2]:
            out.append(f"* {ex.get('name','(unnamed)')}  status={ex.get('code')} {ex.get('status','')}")
            body_ex = ex.get("body") or ""
            if body_ex:
                snippet = body_ex if len(body_ex) < 1500 else body_ex[:1500] + "\n...[truncated]"
                out.append(snippet)

    if emit_curl:
        out.append("\n-- curl --")
        out.append(to_curl(req))

    return "\n".join(out)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query", help="path or substring to identify the request")
    p.add_argument("--pick", type=int, default=None, help="when multiple match, pick this 1-based index")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--no-curl", action="store_true", help="skip the curl block")
    args = p.parse_args()

    c = load()
    hits = find_matches(c, args.query)

    if not hits:
        print(f"no request matched {args.query!r}. Try scripts/search.py first.", file=sys.stderr)
        sys.exit(1)

    if len(hits) > 1 and args.pick is None:
        print(f"{len(hits)} requests matched {args.query!r}; narrow with --pick N (1-based) or a more specific path:", file=sys.stderr)
        for i, (path, req) in enumerate(hits[:20], 1):
            full = folder_path_str(path) + "/" + req.get("name", "")
            method = (req.get("request") or {}).get("method", "")
            print(f"  {i:>3}. {method:<6} {full}", file=sys.stderr)
        if len(hits) > 20:
            print(f"  ... and {len(hits) - 20} more", file=sys.stderr)
        sys.exit(2)

    idx = (args.pick - 1) if args.pick else 0
    if not (0 <= idx < len(hits)):
        print(f"--pick {args.pick} out of range (1..{len(hits)})", file=sys.stderr)
        sys.exit(2)
    path, req = hits[idx]

    if args.json:
        print(json.dumps({
            "path": folder_path_str(path) + "/" + req.get("name", ""),
            "request": req.get("request"),
            "responses": req.get("response", []),
        }, indent=2))
    else:
        print(render_request(path, req, emit_curl=not args.no_curl))


if __name__ == "__main__":
    main()
