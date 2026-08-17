#!/usr/bin/env python3
"""Integrity check for the study curriculum (study/**.mdx).

Checks: frontmatter present with title/section/order/minutes; section label
matches its directory per STUDY_SPEC.md; order inside the section's range;
/problems/<slug> links resolve to real bank problems; mermaid fences are
balanced; non-trivial word count.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
STUDY = os.path.join(ROOT, "study")
PROBLEMS = os.path.join(ROOT, "problems")

SECTIONS = {
    "00-foundations": ("0 · Foundations", range(1, 10)),
    "01-data-structures": ("1 · Data Structures", range(10, 20)),
    "02-patterns": ("2 · Algorithm Patterns", range(20, 30)),
    "03-graphs": ("3 · Graphs", range(30, 40)),
    "04-dp": ("4 · Dynamic Programming", range(40, 50)),
    "05-google": ("5 · The Google Loop", range(50, 60)),
    "06-system-design": ("6 · System Design", range(60, 70)),
    "07-behavioral": ("7 · Behavioral (G&L)", range(70, 80)),
}


def main():
    from app import parse_frontmatter  # reuse the server's parser

    slugs = set(os.listdir(PROBLEMS)) if os.path.isdir(PROBLEMS) else set()
    failed = total = 0
    for dirpath, _dirs, files in os.walk(STUDY):
        for fname in sorted(files):
            if not fname.endswith((".mdx", ".md")):
                continue
            total += 1
            rel = os.path.relpath(os.path.join(dirpath, fname), STUDY)
            section_dir = rel.split(os.sep)[0]
            text = open(os.path.join(dirpath, fname), encoding="utf-8").read()
            meta, body = parse_frontmatter(text)
            errors = []
            for field in ("title", "section", "order", "minutes"):
                if field not in meta:
                    errors.append(f"frontmatter missing {field}")
            expected = SECTIONS.get(section_dir)
            if expected:
                label, orders = expected
                if meta.get("section") != label:
                    errors.append(f"section label {meta.get('section')!r} != {label!r}")
                if isinstance(meta.get("order"), int) and meta["order"] not in orders:
                    errors.append(f"order {meta['order']} outside {orders}")
            else:
                errors.append(f"unknown section dir {section_dir}")
            for slug in re.findall(r"\(/problems/([a-z0-9-]+)\)", body):
                if slug not in slugs:
                    errors.append(f"broken practice link: {slug}")
            if body.count("```mermaid") and body.count("```") % 2 != 0:
                errors.append("unbalanced code fences")
            words = len(re.sub(r"```.*?```", "", body, flags=re.S).split())
            if words < 350:
                errors.append(f"too thin: {words} words")
            if errors:
                failed += 1
                print(f"✗ {rel}")
                for e in errors:
                    print(f"    - {e}")
            else:
                print(f"✓ {rel} ({words}w)")
    print(f"\n{total - failed}/{total} chapters pass.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
