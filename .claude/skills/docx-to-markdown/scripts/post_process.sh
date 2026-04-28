#!/usr/bin/env bash
# Post-process a Pandoc-generated Markdown file to strip common DOCX artifacts.
#
# Usage:
#   bash post_process.sh <output.md> [abs_path_prefix]
#
# Arguments:
#   output.md         Path to the Markdown file to clean up (edited in-place).
#   abs_path_prefix   Absolute path prefix to strip from image URLs so paths
#                     become relative. Defaults to the directory containing
#                     output.md (which is usually correct).

set -euo pipefail

FILE="${1:?Usage: post_process.sh <output.md> [abs_path_prefix]}"

# Auto-detect prefix from the output file's parent directory if not provided
if [[ -n "${2:-}" ]]; then
  PREFIX="$2"
else
  PREFIX="$(cd "$(dirname "$FILE")" && pwd)/"
fi

# 1. Strip {.underline} from linked underlined text: [[text]{.underline}](url) -> [text](url)
perl -i -pe 's/\[\[([^\]]*)\]\{\.underline\}\]/[$1]/g' "$FILE"

# 2. Strip {.underline} from bold-linked text: [**[text]{.underline}**](url) -> [**text**](url)
perl -i -pe 's/\[\*\*\[([^\]]*)\]\{\.underline\}\*\*\]/[**$1**]/g' "$FILE"

# 3. Strip remaining [text]{.underline} spans (plain underlined text, no link)
perl -i -pe 's/\[([^\]]*)\]\{\.underline\}/$1/g' "$FILE"

# 4. Remove image dimension attributes: {width="..." height="..."} and {width="..."}
perl -i -pe 's/ ?\{width="[^"]*"[^}]*\}//g' "$FILE"

# 5. Remove heading ID anchors: ## Title {#title} -> ## Title
perl -i -pe 's/^(#{1,6}\s+.*?)\s+\{#[^}]+\}\s*$/$1/g' "$FILE"

# 6. Fix double-space after heading marker: "#  Title" -> "# Title"
perl -i -pe 's/^(#{1,6})  /$1 /g' "$FILE"

# 7. Remove empty headings (lines that are only # symbols and optional whitespace)
perl -i -ne 'print unless /^#{1,6}\s*$/' "$FILE"

# 8. Move images out of headings: "### ![alt](url)" -> "![alt](url)"
perl -i -pe 's/^#{1,6}\s+(!\[)/$1/g' "$FILE"

# 9. Make image paths relative (strip absolute path prefix)
if [[ -n "$PREFIX" ]]; then
  perl -i -pe "s|\Q${PREFIX}\E||g" "$FILE"
fi

# 10. Collapse 3+ consecutive blank lines to 2
perl -i -0pe 's/\n{3,}/\n\n/g' "$FILE"

echo "Post-processing complete: $FILE"
