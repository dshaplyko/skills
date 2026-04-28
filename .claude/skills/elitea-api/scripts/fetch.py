#!/usr/bin/env python3
"""Fetch the ELITEA Postman collection, freshly.

Strategy (the Postman API doesn't honor If-Modified-Since, so we do our own):

  1. Cheap probe (~250 bytes): GET /collections?workspace=<ws> returns
     the collection's updatedAt timestamp.
  2. Compare against the timestamp stored alongside the cache.
  3. If the same, reuse the ~800KB cached JSON. If different (or the
     cache is missing, or --force is passed), download the full
     collection and replace the cache.

This gives the user genuinely fresh data on every invocation while
touching the network with ~250 bytes unless something has actually
changed.

Reads POSTMAN_API_KEY from the environment.

Exit codes:
  0 - cache is current (either fresh download or probe said unchanged)
  2 - missing/invalid POSTMAN_API_KEY
  3 - network / HTTP error, no usable cache
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE_ID = "8b74059a-13ef-4d82-838b-d55eec621a08"
COLLECTION_UID = "3650685-1016a7c9-2fc6-40ac-a1dd-cc318feaf294"
CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
COLLECTION_FILE = CACHE_DIR / "collection.json"
META_FILE = CACHE_DIR / "meta.json"


def _load_dotenv(start: Path) -> None:
    """Populate POSTMAN_API_KEY from a .env file if it isn't already set.

    Walks up from `start` looking for a .env, stopping at the git root or
    the filesystem root. Only sets variables that aren't already in the
    environment so real env vars always win. Minimal parser: KEY=VALUE,
    ignores blank lines and # comments, strips a matching pair of quotes.
    """
    if os.environ.get("POSTMAN_API_KEY", "").strip():
        return
    for d in [start, *start.parents]:
        env_path = d / ".env"
        if env_path.is_file():
            try:
                for line in env_path.read_text().splitlines():
                    s = line.strip()
                    if not s or s.startswith("#") or "=" not in s:
                        continue
                    k, _, v = s.partition("=")
                    k = k.strip()
                    v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                        v = v[1:-1]
                    os.environ.setdefault(k, v)
            except OSError:
                pass
            return
        if (d / ".git").exists():
            return


def _get(url: str, key: str) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"X-API-Key": key})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main(argv: list[str]) -> int:
    force = "--force" in argv or "-f" in argv

    _load_dotenv(Path(__file__).resolve().parent)
    key = os.environ.get("POSTMAN_API_KEY", "").strip()
    if not key:
        print(
            "ERROR: POSTMAN_API_KEY is not set.\n"
            "Generate one at postman.com -> Settings -> API Keys, then either:\n"
            "  (a) add POSTMAN_API_KEY=PMAK-... to your project's .env, or\n"
            "  (b) export POSTMAN_API_KEY='PMAK-...' in your shell.",
            file=sys.stderr,
        )
        return 2

    CACHE_DIR.mkdir(exist_ok=True)

    cached_updated_at: str | None = None
    if META_FILE.exists():
        try:
            cached_updated_at = json.loads(META_FILE.read_text()).get("updatedAt")
        except (ValueError, OSError):
            cached_updated_at = None

    if force or not COLLECTION_FILE.exists():
        remote_updated_at = None  # skip probe, go straight to download
    else:
        status, body = _get(
            f"https://api.getpostman.com/collections?workspace={WORKSPACE_ID}", key
        )
        if status == 401:
            print("ERROR: 401 from Postman API. POSTMAN_API_KEY is invalid.", file=sys.stderr)
            return 2
        if status != 200:
            print(f"WARN: probe returned {status}: {body[:200]!r}", file=sys.stderr)
            remote_updated_at = None  # fall back to download
        else:
            try:
                cols = json.loads(body).get("collections", [])
                match = next((c for c in cols if c.get("uid") == COLLECTION_UID), None)
                remote_updated_at = match.get("updatedAt") if match else None
            except ValueError:
                remote_updated_at = None

        if remote_updated_at and remote_updated_at == cached_updated_at:
            print(
                f"cache-fresh: updatedAt={remote_updated_at} path={COLLECTION_FILE}"
            )
            return 0

    # Full download path
    status, body = _get(
        f"https://api.getpostman.com/collections/{COLLECTION_UID}", key
    )
    if status == 401:
        print("ERROR: 401 from Postman API. POSTMAN_API_KEY is invalid.", file=sys.stderr)
        return 2
    if status != 200:
        print(f"ERROR: download returned {status}: {body[:400]!r}", file=sys.stderr)
        if COLLECTION_FILE.exists():
            print(f"falling back to stale cache: {COLLECTION_FILE}", file=sys.stderr)
            return 0
        return 3

    COLLECTION_FILE.write_bytes(body)

    # Re-probe to capture the authoritative updatedAt (the collection body
    # has its own timestamps but the listing's is what the probe compares).
    probe_status, probe_body = _get(
        f"https://api.getpostman.com/collections?workspace={WORKSPACE_ID}", key
    )
    updated_at = None
    if probe_status == 200:
        try:
            for c in json.loads(probe_body).get("collections", []):
                if c.get("uid") == COLLECTION_UID:
                    updated_at = c.get("updatedAt")
                    break
        except ValueError:
            pass

    META_FILE.write_text(json.dumps({"updatedAt": updated_at}, indent=2))
    print(
        f"downloaded: bytes={len(body)} updatedAt={updated_at} path={COLLECTION_FILE}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
