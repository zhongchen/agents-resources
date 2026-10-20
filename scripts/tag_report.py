#!/usr/bin/env python3
"""Print a Markdown report of tag usage across entries. Always exits 0."""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_entries import load_allowed_tags, parse_frontmatter  # noqa: E402

ENTRIES_DIR = Path("entries")


def collect():
    """Map each tag to the entry paths that use it."""
    tags = defaultdict(list)
    for path in sorted(ENTRIES_DIR.rglob("*.md")):
        fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fm or not isinstance(fm.get("tags"), list):
            continue
        rel = path.as_posix()
        for t in fm["tags"]:
            tags[t].append(rel)
    return tags


def main():
    tags = collect()
    allowed = load_allowed_tags() or set()

    print("# Tag report")
    print()

    print("## Tag counts")
    if tags:
        for t, paths in sorted(tags.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            print(f"- `{t}`: {len(paths)}")
    else:
        print("None.")
    print()

    unlisted = {t: p for t, p in tags.items() if t not in allowed}
    multi = sorted(t for t, p in unlisted.items() if len(p) >= 2)
    single = sorted(t for t, p in unlisted.items() if len(p) == 1)

    print("## Unlisted tags used by 2+ entries (candidates to add)")
    if multi:
        for t in multi:
            print(f"- `{t}`: {', '.join(unlisted[t])}")
    else:
        print("None.")
    print()

    print("## Unlisted tags used by 1 entry (candidates to drop or replace)")
    if single:
        for t in single:
            print(f"- `{t}`: {unlisted[t][0]}")
    else:
        print("None.")
    print()

    unused = sorted(t for t in allowed if t not in tags)
    print("## Listed tags used by no entry (candidates to remove)")
    if unused:
        for t in unused:
            print(f"- `{t}`")
    else:
        print("None.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
