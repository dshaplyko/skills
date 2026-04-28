#!/usr/bin/env python3
"""Print the collection-level defaults: auth, variables, and info.

Individual requests that omit an `auth` block inherit this one, and any
{{variable}} they use is defined here (or expected to come from the
user's Postman environment).

Usage:
  scripts/defaults.py           # human-readable
  scripts/defaults.py --json
"""
from __future__ import annotations

import argparse
import json

from _collection import load


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    c = load()
    info = c.get("info", {})
    auth = c.get("auth")
    variables = c.get("variable", []) or []

    if args.json:
        print(json.dumps({
            "info": info,
            "auth": auth,
            "variables": variables,
        }, indent=2))
        return

    print(f"collection: {info.get('name')}")
    print(f"schema    : {info.get('schema')}")
    desc = (info.get("description") or "").strip()
    if desc:
        print(f"description: {desc[:400]}")

    print("\n-- collection-level auth (inherited when a request omits its own) --")
    if auth:
        print(json.dumps(auth, indent=2))
    else:
        print("(none)")

    print("\n-- collection-level variables (pre-set) --")
    if variables:
        for v in variables:
            print(f"  {{{{{v.get('key')}}}}}  = {v.get('value','')!r}  {v.get('description') or ''}")
    else:
        print("(none)")

    print(
        "\nNote: variables like {{base_url}}, {{auth_token}}, {{project_id}} that"
        "\nappear in individual requests are expected to come from your Postman"
        "\nenvironment at runtime. The skill does not invent values for them."
    )


if __name__ == "__main__":
    main()
