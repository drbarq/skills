#!/usr/bin/env bash
# Rebuild the downloadable artifacts in public/ from the skill sources in src/.
# Run this after editing anything under src/, then deploy public/ to joetustin.com/skills.
set -euo pipefail
cd "$(dirname "$0")"

mkdir -p public

for skill in src/*/; do
  name="$(basename "$skill")"
  [ -f "$skill/SKILL.md" ] || { echo "skip $name (no SKILL.md)"; continue; }

  echo "packaging $name ..."
  # tar.gz for Claude Code (top-level dir = skill name, extracts into ~/.claude/skills/)
  ( cd src && tar -czf "../public/$name.tar.gz" "$name" )
  # .skill (zip) for Claude.ai / Cowork upload
  ( cd src && rm -f "../public/$name.skill" && zip -r -q "../public/$name.skill" "$name" -x '*.pyc' -x '*/__pycache__/*' )
done

echo "done. artifacts in public/:"
ls -1 public/
echo
echo "Remember to keep public/index.json in sync with the skills you ship."
