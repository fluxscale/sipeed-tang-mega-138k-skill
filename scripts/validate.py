#!/usr/bin/env python3
"""Validate the portable package and local reference graph without dependencies."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/sipeed-tang-mega-138k"
errors = []
text = (SKILL / "SKILL.md").read_text()
match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
if not match:
    errors.append("SKILL.md: missing YAML frontmatter")
else:
    fields = dict(re.findall(r"^(name|description): (.+)$", match[1], re.M))
    if fields.get("name") != SKILL.name:
        errors.append("SKILL.md: name must match directory")
    if not fields.get("description") or len(fields["description"]) > 1024:
        errors.append("SKILL.md: missing or oversized description")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields.get("name", "")):
        errors.append("SKILL.md: invalid name")
# All installable reference files must be reachable from the skill entry point.
reached = set()
queue = [SKILL / "SKILL.md"]
while queue:
    file = queue.pop().resolve()
    if file in reached:
        continue
    reached.add(file)
    for target in re.findall(r"\]\(([^)]+)\)", file.read_text()):
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        dest = (file.parent / target.split("#")[0]).resolve()
        if not dest.is_relative_to(SKILL.resolve()):
            errors.append(f"{file.relative_to(ROOT)}: reference escapes installable skill: {target}")
        elif not dest.exists():
            errors.append(f"{file.relative_to(ROOT)}: broken link: {target}")
        elif dest.suffix == ".md":
            queue.append(dest)
for file in (SKILL / "references").glob("*.md"):
    if file.resolve() not in reached:
        errors.append(f"Unreachable reference: {file.name}")
for file in [ROOT / "README.md"]:
    for target in re.findall(r"\]\(([^)]+)\)", file.read_text()):
        if not re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) and not target.startswith("#"):
            if not (file.parent / target.split("#")[0]).exists():
                errors.append(f"README.md: broken link: {target}")
for file in SKILL.rglob("*"):
    if file.name == "__pycache__" or file.suffix == ".pyc":
        continue
    if file.is_file() and file.stat().st_size > 1_000_000:
        errors.append(f"Unexpected large package file: {file.name}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Package valid: {len(reached) - 1} reachable reference documents; local links resolve.")
