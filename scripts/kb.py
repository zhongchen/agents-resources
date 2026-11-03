#!/usr/bin/env python3
"""Search the knowledge bank by symptom.

Titles and summaries describe a lesson. They do not contain the error text
that a session actually sees. Each entry can carry a `symptoms` list of
verbatim strings for that, and this script ranks matches over symptoms,
title, summary, tags and body.

Usage:
    kb.py search "NoClassDefFoundError aws-crt"
    kb.py search --limit 10 quota

All terms must match the same entry (AND). Matching is case-insensitive
substring, so partial words work. Use it from any directory.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_entries import parse_frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"

WEIGHTS = [
    ("symptoms", 6),
    ("title", 4),
    ("summary", 3),
    ("tags", 3),
    ("body", 1),
]
SNIPPET_LEN = 150


def evidence(fm, body, terms):
    """Weightiest field that holds a term, and a short quote from it."""
    for field, _ in WEIGHTS:
        if field == "body":
            for line in body.splitlines():
                low = line.lower()
                if any(t in low for t in terms):
                    return field, line.strip()
            continue
        value = fm.get(field, "")
        values = value if isinstance(value, list) else [value]
        for item in values:
            low = str(item).lower()
            if any(t in low for t in terms):
                return field, str(item)
    return "", ""


def search(terms, limit):
    hits = []
    for path in sorted(ENTRIES.rglob("*.md")):
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fm:
            continue
        lowered = {}
        for field, _ in WEIGHTS:
            value = fm.get(field, "")
            values = value if isinstance(value, list) else [value]
            lowered[field] = [str(v).lower() for v in values]
        lowered["body"] = [body.lower()]

        score = 0
        for term in terms:
            matched = False
            for field, weight in WEIGHTS:
                if any(term in v for v in lowered[field]):
                    score += weight
                    matched = True
            if not matched:
                break
        else:
            field, quote = evidence(fm, body, terms)
            hits.append((score, path, fm.get("title", path.stem), field, quote))

    hits.sort(key=lambda h: (-h[0], str(h[1])))
    return hits[:limit]


def main(argv):
    if not argv or argv[0] != "search":
        print(__doc__.strip())
        return 2

    args = argv[1:]
    limit = 5
    if "--limit" in args:
        i = args.index("--limit")
        try:
            limit = int(args[i + 1])
        except (IndexError, ValueError):
            print("--limit needs a number", file=sys.stderr)
            return 2
        del args[i:i + 2]

    terms = [a.lower() for a in args if a.strip()]
    if not terms:
        print("Give at least one search term.", file=sys.stderr)
        return 2

    hits = search(terms, limit)
    if not hits:
        print(f"No entry matches: {' '.join(terms)}")
        print("If this is a new gotcha, add an entry and give it a symptoms list.")
        return 0

    for score, path, title, field, quote in hits:
        rel = path.relative_to(ROOT).as_posix()
        print(f"{score:>2} {rel} — {title}")
        quote = " ".join(quote.split())
        if len(quote) > SNIPPET_LEN:
            quote = quote[:SNIPPET_LEN].rstrip() + "..."
        print(f"   {field}: {quote}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
