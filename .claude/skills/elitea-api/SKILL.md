---
name: elitea-api
description: Answer any question about the ELITEA REST API using the live Postman collection at postman.com/projectalita/elitea-api-public. Use this skill whenever the user asks about ELITEA/Alita/projectalita HTTP endpoints, requests, methods, parameters, bodies, headers, auth, or wants a curl/Python snippet for a specific ELITEA API call — even if they don't name Postman explicitly. Prefer this skill over answering from memory; it fetches fresh data via the Postman API and uses scripted tools to search/inspect 535+ requests, so answers are authoritative and current.
---

# ELITEA API research skill

This skill answers questions about the ELITEA REST API by reading the
live Postman collection (`postman.com/projectalita/elitea-api-public`)
via the Postman API, with a tiny on-disk cache that is **revalidated
on every invocation** using a cheap 250-byte probe — the full ~800KB
download only happens when the collection has actually changed
upstream. Never answer ELITEA API questions from general knowledge;
always query the collection.

## Prerequisite

The skill needs a Postman API key (free; postman.com → Settings → API
Keys). `fetch.py` reads `POSTMAN_API_KEY` from the real environment
first, and if that's empty it walks up from the skill directory
looking for a `.env` file (stopping at the nearest git root) and
loads any `KEY=VALUE` pairs it finds. So either works:

```
# option A — project .env (preferred, file is in .gitignore):
echo 'POSTMAN_API_KEY=PMAK-...' >> /path/to/project/.env

# option B — shell export:
export POSTMAN_API_KEY='PMAK-...'
```

If neither is set, `fetch.py` exits 2 with a clear message. Never
paste the key into settings.local.json or a committed file.

## Workflow for answering a question

Treat every new question as "something changed upstream" unless you
just refreshed this turn. The workflow:

1. **Refresh** — always start with `python3 scripts/fetch.py` (silent;
   prints `cache-fresh: ...` or `downloaded: ...`). This is cheap and
   guarantees freshness. Skip only if you ran it earlier this turn.
2. **Locate the request** — use `scripts/search.py` when the user's
   phrasing is loose, or `scripts/list.py --folder NAME` when you
   already know the folder. Prefer `search.py` for questions like
   "how do I X"; prefer `list.py` for "what's in folder Y".
3. **Dump full details** — run `scripts/show.py "<path or name>"` to
   get method, URL, path/query vars, headers, auth, body, example
   responses, detected `{{variables}}`, and a ready-to-run curl.
4. **Answer** — in your reply, include the curl (or translate to the
   language the user asked for), point out `{{variables}}` the user
   must fill in (never invent values), and flag anything from the
   `archive/` folder as deprecated.

If something doesn't match, re-run `search.py` with a broader term or
regex (`-e 'regex'`) rather than guessing. The collection is the
source of truth.

## Scripts

All paths are relative to this skill's directory. Run from any CWD.

- `scripts/fetch.py` — refresh the cache (with probe-then-download).
  Use `--force` to skip the probe. Requires `POSTMAN_API_KEY`.
- `scripts/list.py` — structure browser.
  - no args: top-level folders with counts.
  - `--folder NAME`: requests inside a folder (fuzzy match).
  - `--all`: flat list of every request.
  - `--folders`: every folder, nested.
  - `--json`: machine-readable on any of the above.
- `scripts/search.py "query"` — find requests by substring across
  name, folder path, URL, description, headers, and raw body.
  - `-e 'regex'` for regex mode.
  - `--fields name,url,body,...` to narrow the scanned fields.
- `scripts/show.py "path or name"` — full request dump + curl.
  - Fuzzy-matches; if multiple hit, prints a numbered list and exits
    with instructions to re-run with `--pick N`.
  - `--no-curl` if the user explicitly doesn't want it.
- `scripts/defaults.py` — collection-level auth + variables + info.
  Use when the user asks about auth, tokens, or "what variables does
  this API need". Don't run it for normal per-request questions.

## Composing requests (when the user wants to actually call something)

`show.py` emits a curl with `{{placeholders}}` intact. To turn it into
a runnable command:

1. Identify every `{{var}}` in the output.
2. For each one, check whether the user already told you a value; if
   not, ask a single concise question naming all missing vars at once.
3. Substitute and present the final command. **Do not invent values
   for tokens, IDs, or URLs** — those are the user's to fill in.
4. If the user asks for a language other than curl (Python, JS,
   etc.), read `show.py --json` output and translate the structure
   directly rather than parsing the curl.

## Common pitfalls

- **Archive folder is deprecated.** Many requests with promising names
  live under `archive/` (chat, datasources, deprecated prompt_lib,
  flows). If a hit lands there, warn the user and prefer a non-archive
  counterpart in `elitea_core/` if one exists.
- **Auth inheritance.** If `show.py` prints no `-- auth --` section,
  the request inherits the collection-level `Bearer {{auth_token}}`
  (see `scripts/defaults.py`). Tell the user they need to send the
  bearer, even though the request-specific dump didn't list it.
- **Disabled query params.** Postman preserves disabled params in the
  JSON. They show up in `show.py` output marked `(disabled)` — those
  are examples, not required.
- **Name collisions.** "auth", "collection", "application", "tool",
  etc. match many folders. `list.py --folder` picks the shortest path
  and lists the others in stderr; `show.py` lists all candidates and
  wants `--pick N`.

## For deeper structural questions

`references/structure.md` has a map of top-level folders, the auth
model, common `{{variables}}`, and the Postman v2.1 JSON shape the
scripts parse. Read it when the user asks architectural questions
("how is the API organized", "what's the auth model", "what top-level
areas exist").

## Do not

- Do not answer from memory or general training data — always pull
  from the collection via the scripts.
- Do not cache query results across turns in your head; re-run
  `fetch.py` + the relevant script. It's cheap.
- Do not substitute values for `{{base_url}}`, `{{auth_token}}`,
  `{{project_id}}`, or any other `{{variable}}` unless the user gave
  you that value in this conversation.
- Do not paste the entire collection.json or long listings into the
  reply; always narrow to what the user asked for. The full file is
  ~800KB.
