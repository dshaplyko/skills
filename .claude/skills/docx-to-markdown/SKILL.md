---
name: docx-to-markdown
description: Convert DOCX (or .doc) Word documents to clean, readable Markdown using Pandoc, with images preserved in a dedicated subfolder. Use this skill whenever the user wants to convert, transform, extract, parse, or read content from a Word file — even if they don't explicitly say "Markdown". Trigger for phrases like "turn this Word doc into markdown", "get the text out of my .docx", "convert my Word file", "I have a .docx I need to process", "read this Word document", or any time a .docx or .doc file path appears in the request alongside a desire to work with its contents.
---

# DOCX to Markdown Conversion

Converts Word documents to clean, portable Markdown. Pandoc does the heavy lifting; a bundled post-processing script (`scripts/post_process.sh`) removes common Pandoc artifacts in one shot.

## Prerequisites

Pandoc must be installed:

```bash
brew install pandoc        # macOS
sudo apt install pandoc    # Debian/Ubuntu
winget install pandoc      # Windows
```

Verify: `pandoc --version`

> If Pandoc cannot be installed in this environment, see **Troubleshooting** below.

## Conversion Workflow

### Step 1: Identify inputs

Determine:
- **Input**: path to the `.docx` (or `.doc`) file
- **Output**: desired `.md` filename (default: same stem as input, same directory)
- **Images folder**: `<output_stem>_images/` next to the output file

> **`.doc` files (older binary format)**: Pandoc can read `.doc` directly, but fidelity is lower than `.docx`. If the result looks garbled, ask the user to open it in Word or LibreOffice and re-save as `.docx` first.

### Step 2: Run Pandoc

```bash
pandoc "<input.docx>" \
  -o "<output.md>" \
  --extract-media="<output_stem>_images" \
  --markdown-headings=atx \
  --wrap=none
```

**Flags:**
- `--extract-media`: pulls embedded images into a subfolder and rewrites their paths in the Markdown
- `--markdown-headings=atx`: forces `#`/`##`/`###` style headings (not underline-style)
- `--wrap=none`: disables hard line-wrapping for cleaner diffs and editing

### Step 3: Post-process

Run the bundled script to strip Pandoc artifacts in one step:

```bash
bash "<skill-dir>/scripts/post_process.sh" "<output.md>"
```

The script auto-detects the absolute path prefix from the output file's directory, so no second argument is usually needed. Pass one explicitly only if images are extracted to a different location:

```bash
bash "<skill-dir>/scripts/post_process.sh" "<output.md>" "/absolute/prefix/to/strip/"
```

**What the script cleans:**

| Pattern | Fix |
|---|---|
| `[[text]{.underline}](url)` | → `[text](url)` |
| `[**[text]{.underline}**](url)` | → `[**text**](url)` |
| `[text]{.underline}` | → `text` |
| `{width="..." height="..."}` image attributes | Removed |
| `## Title {#anchor-id}` heading anchors | → `## Title` |
| `#  Double-spaced heading` | → `# Single-spaced heading` |
| Empty headings (`##` with no text) | Removed |
| Images inside headings (`### ![…](url)`) | Image promoted out of heading |
| Absolute image path prefixes | Replaced with relative paths |
| 3+ consecutive blank lines | Collapsed to 2 |

### Step 4: Manual review

Skim the output for these issues that the script can't fix automatically:

1. **Tables** — Complex or merged-cell tables may lose structure. Fix manually or flag for the user.
2. **Raw HTML** — Look for stray `<div>`, `<span>`, `<br>`, or `<!--...-->` and remove or convert.
3. **List indentation** — Nested lists should use consistent 2- or 4-space indentation.
4. **Footnotes** — Converted to `[^1]` style; verify they're complete and not duplicated.
5. **Missing content** — Text boxes and floating shapes are often dropped silently. If the user reports missing content, search for key phrases from the original.

### Step 5: Confirm output

Report to the user:
- Path to the `.md` file
- Path to the images subfolder and count of extracted images (if any)
- Any elements that may need manual attention (tables, footnotes, text boxes, tracked changes)

---

## Example

**Input:** `~/docs/Project Brief.docx`

```bash
# Convert
pandoc "~/docs/Project Brief.docx" \
  -o "~/docs/Project Brief.md" \
  --extract-media="~/docs/Project Brief_images" \
  --markdown-headings=atx \
  --wrap=none

# Post-process
bash /path/to/docx-to-markdown/scripts/post_process.sh "~/docs/Project Brief.md"
```

**Output structure:**
```
~/docs/
├── Project Brief.md
└── Project Brief_images/
    ├── image1.png
    └── image2.jpeg
```

---

## Known Limitations

| Element | Behavior |
|---|---|
| Merged table cells | May lose structure — flag for manual review |
| Text boxes / floating shapes | Often dropped silently — flag if user reports missing content |
| Footnotes | Converted to inline `[^n]` — check for completeness |
| Tracked changes | Accepted silently (final version only) |
| Smart quotes / em-dashes | Preserved as Unicode characters |
| Comments | Stripped |
| `.doc` (old binary format) | Supported but lower fidelity — recommend re-saving as `.docx` |
| Password-protected files | Pandoc will error — ask user to remove protection in Word first |
| Embedded Excel charts | Extracted as flat images, not editable data |

---

## Troubleshooting

**Pandoc not available**: Try `unoconv` + LibreOffice headless as an alternative, or ask the user to copy-paste the document text directly.

**Images not extracted**: Verify `--extract-media` path has no trailing slash and the target directory is writable.

**Garbled heading levels**: The source document likely uses manual font sizing instead of Word heading styles. Inform the user and suggest applying Heading 1/2/3 styles in Word before re-exporting.

**`perl` not found**: The post-processing script requires Perl (pre-installed on macOS and most Linux distros). On Windows, install it via `winget install StrawberryPerl.StrawberryPerl` or run the commands individually in PowerShell with appropriate regex equivalents.

**Unicode/encoding errors**: Add `--from=docx+styles` to the Pandoc command, or run `iconv -f utf-8 -t utf-8 -c "<output.md>"` to strip invalid characters.

**Large file takes long**: Pandoc processes synchronously — just wait; it handles large files well.
