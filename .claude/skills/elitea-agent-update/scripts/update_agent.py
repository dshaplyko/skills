#!/usr/bin/env python3
"""Update an ELITEA agent's instructions (and optionally other fields) from a
local .md instruction file.

The .md file is expected to start with a header block of `Key: Value` lines
followed by the instruction body. Recognised header keys:

  Agent ID:    <int>   (application_id)
  Version ID:  <int>   (application_version_id)
  Project ID:  <int>
  URL:         <base_url, e.g. https://next.elitea.ai/>

Everything from the first blank line / first Markdown heading onward is
treated as the new `instructions` body.

The script:
  1. Loads ELITEA_API_TOKEN from the nearest .env (walking up from CWD).
  2. GETs the current agent version so unrelated fields (llm_settings,
     tools, tags, welcome_message, conversation_starters) are preserved.
  3. Builds a PUT payload with the new instructions (and any extra fields
     passed via --set name=... / --set description=...).
  4. Dry-run by default: prints a diff-style summary and exits.
     Pass --apply to actually PUT.

Usage:
  python3 update_agent.py path/to/instruction.md
  python3 update_agent.py path/to/instruction.md --apply
  python3 update_agent.py path/to/instruction.md --set description="New desc" --apply
  python3 update_agent.py path/to/instruction.md \
      --agent-id 79 --version-id 79 --project-id 29 \
      --base-url https://next.elitea.ai
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path


HEADER_KEYS = {
    "agent id": "agent_id",
    "version id": "version_id",
    "project id": "project_id",
    "url": "base_url",
}


def load_env_token() -> str | None:
    """Look for ELITEA_API_TOKEN in env, or walk up directories for a .env file."""
    tok = os.environ.get("ELITEA_API_TOKEN")
    if tok:
        return tok
    here = Path.cwd().resolve()
    for parent in [here, *here.parents]:
        env_file = parent / ".env"
        if env_file.is_file():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                if k.strip() == "ELITEA_API_TOKEN":
                    return v.strip().strip('"').strip("'")
        if (parent / ".git").exists():
            break
    return None


def parse_instruction_file(path: Path) -> tuple[dict, str]:
    """Return (header_dict, instruction_body)."""
    text = path.read_text()
    lines = text.splitlines()
    header: dict = {}
    body_start = 0
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            # Stop scanning header on first blank line, but only if we've seen at least one key.
            if header:
                body_start = i + 1
                break
            continue
        # Stop at first markdown heading regardless.
        if line.startswith("#"):
            body_start = i
            break
        m = re.match(r"^([A-Za-z][A-Za-z ]+?)\s*:\s*(.+)$", line)
        if m and m.group(1).strip().lower() in HEADER_KEYS:
            key = HEADER_KEYS[m.group(1).strip().lower()]
            val = m.group(2).strip()
            header[key] = val
        else:
            # Non-matching, non-heading, non-blank line: treat as body start.
            body_start = i
            break
    body = "\n".join(lines[body_start:]).strip("\n")
    return header, body


def normalise_base_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def http_request(method: str, url: str, token: str, body: dict | None = None) -> dict:
    data = None
    headers = {"Authorization": f"Bearer {token}"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            if not raw:
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code} {method} {url}\n{body_text}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error {method} {url}: {e.reason}")


def get_application(base_url: str, project_id: int, agent_id: int, token: str) -> dict:
    """GET the application top-level (returns app fields + versions[] + version_details)."""
    url = f"{base_url}/api/v2/elitea_core/application/prompt_lib/{project_id}/{agent_id}"
    return http_request("GET", url, token)


def get_application_version(base_url: str, project_id: int, agent_id: int, version_name: str, token: str) -> dict:
    url = f"{base_url}/api/v2/elitea_core/application/prompt_lib/{project_id}/{agent_id}/{version_name}"
    return http_request("GET", url, token)


def put_application(base_url: str, project_id: int, agent_id: int, payload: dict, token: str) -> dict:
    """App-level PUT — body shape {name, description, version: {...}}."""
    url = f"{base_url}/api/v2/elitea_core/application/prompt_lib/{project_id}/{agent_id}"
    return http_request("PUT", url, token, payload)


def summarise(label: str, old: str, new: str) -> str:
    if old == new:
        return f"  {label}: unchanged ({len(old)} chars)"
    return (
        f"  {label}: CHANGED  {len(old)} -> {len(new)} chars\n"
        f"    - old (first 80): {old[:80]!r}\n"
        f"    + new (first 80): {new[:80]!r}"
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Update an ELITEA agent's instructions from a .md file.")
    p.add_argument("file", type=Path, help="Path to the .md instruction file.")
    p.add_argument("--apply", action="store_true", help="Actually send the PUT (default is dry-run).")
    p.add_argument("--set", dest="extra", action="append", default=[],
                   metavar="FIELD=VALUE",
                   help="Override a top-level field, e.g. --set name='New' --set description='New desc'.")
    p.add_argument("--agent-id", type=int, help="Override Agent ID from the file header.")
    p.add_argument("--version-id", type=int, help="Override Version ID from the file header.")
    p.add_argument("--project-id", type=int, help="Override Project ID from the file header.")
    p.add_argument("--base-url", help="Override URL from the file header.")
    args = p.parse_args()

    if not args.file.is_file():
        print(f"error: file not found: {args.file}", file=sys.stderr)
        return 2

    header, instructions = parse_instruction_file(args.file)
    if not instructions.strip():
        print("error: no instruction body found in file (everything after the header block was empty).",
              file=sys.stderr)
        return 2

    agent_id = args.agent_id or (int(header["agent_id"]) if "agent_id" in header else None)
    version_id = args.version_id or (int(header["version_id"]) if "version_id" in header else None)
    project_id = args.project_id or (int(header["project_id"]) if "project_id" in header else None)
    base_url = args.base_url or header.get("base_url")

    missing = [name for name, val in [
        ("Agent ID", agent_id), ("Version ID", version_id),
        ("Project ID", project_id), ("URL", base_url),
    ] if not val]
    if missing:
        print("error: missing required values: " + ", ".join(missing), file=sys.stderr)
        print("       provide them in the .md header block or via CLI flags.", file=sys.stderr)
        return 2

    base_url = normalise_base_url(base_url)

    token = load_env_token()
    if not token:
        print("error: ELITEA_API_TOKEN not found in environment or in any .env file walking up from CWD.",
              file=sys.stderr)
        return 2

    extras: dict = {}
    for kv in args.extra:
        if "=" not in kv:
            print(f"error: --set value must be FIELD=VALUE, got {kv!r}", file=sys.stderr)
            return 2
        k, _, v = kv.partition("=")
        extras[k.strip()] = v

    print(f"Fetching application: agent={agent_id} project={project_id}")
    print(f"  GET {base_url}/api/v2/elitea_core/application/prompt_lib/{project_id}/{agent_id}")
    app = get_application(base_url, project_id, agent_id, token)

    versions = app.get("versions") or []
    matching = [v for v in versions if v.get("id") == version_id]
    if not matching:
        names = ", ".join(f"{v.get('name')}#{v.get('id')}" for v in versions) or "(none)"
        print(f"error: version_id={version_id} not found on agent {agent_id}. Available: {names}", file=sys.stderr)
        return 2
    version_name = matching[0].get("name")
    print(f"  resolved version_id={version_id} -> version_name={version_name!r}")

    # Get full version details (instructions, llm_settings, tools, etc.)
    print(f"  GET {base_url}/api/v2/elitea_core/application/prompt_lib/{project_id}/{agent_id}/{version_name}")
    detail = get_application_version(base_url, project_id, agent_id, version_name, token)
    current_version = detail.get("version_details") or detail

    old_instructions = current_version.get("instructions", "")
    # Build new version object: copy current, override instructions.
    new_version = dict(current_version)
    new_version["instructions"] = instructions

    # PUT body shape for v2 app-level: {name, description, version: {...}}.
    # name/description default to current app values to avoid clobbering them.
    payload: dict = {
        "name": app.get("name"),
        "description": app.get("description"),
        "version": new_version,
    }
    for k, v in extras.items():
        if k in {"name", "description"}:
            payload[k] = v
        elif k == "welcome_message":
            new_version["welcome_message"] = v
        else:
            payload[k] = v

    # --- diff summary ---
    print("\nPlanned changes:")
    print(summarise("instructions", old_instructions, instructions))
    for k, v in extras.items():
        print(f"  {k}: -> {v!r}")
    print(f"\nTarget: PUT {base_url}/api/v2/elitea_core/application/prompt_lib/{project_id}/{agent_id}")

    if not args.apply:
        print("\nDry-run only. Re-run with --apply to send the PUT.")
        return 0

    print("\nSending PUT...")
    resp = put_application(base_url, project_id, agent_id, payload, token)
    print("OK. Server response keys:", sorted(resp.keys()) if isinstance(resp, dict) else type(resp).__name__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
