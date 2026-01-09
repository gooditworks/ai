#!/usr/bin/env python3
"""
Gather historical reflection data for deep analysis.

Parses markdown files in history/reflections/ to extract structured data
for cross-session pattern detection.

Usage:
    python scripts/gather_history.py [reflections_dir] [--json]

Output: JSON with parsed reflection data and recurring theme counts.
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def parse_reflection_file(filepath: Path) -> dict | None:
    """Parse a reflection markdown file into structured data."""
    try:
        content = filepath.read_text()
    except Exception:
        return None

    # Extract date and topic from filename (YYYY-MM-DD-topic.md)
    filename = filepath.stem
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", filename)
    if match:
        date = match.group(1)
        topic = match.group(2).replace("-", " ")
    else:
        date = ""
        topic = filename

    reflection = {
        "file": str(filepath),
        "date": date,
        "topic": topic,
        "summary": "",
        "discoveries": [],
        "improvements_made": [],
        "issues_created": [],
        "open_questions": [],
        "patterns_to_watch": [],
        "anti_patterns": [],
    }

    # Parse sections
    current_section = None
    current_items = []

    for line in content.split("\n"):
        line = line.strip()

        # Detect section headers
        if line.startswith("## "):
            # Save previous section
            if current_section and current_items:
                _save_section(reflection, current_section, current_items)
            current_section = line[3:].lower()
            current_items = []
        elif line.startswith("### "):
            # Subsection - treat as continuation
            pass
        elif line.startswith("- "):
            # List item
            item = line[2:].strip()
            # Handle checkbox items
            if item.startswith("[x] "):
                item = item[4:]
            elif item.startswith("[ ] "):
                item = item[4:]
            if item:
                current_items.append(item)
        elif line and current_section == "session summary":
            # Non-list content in summary
            reflection["summary"] = line

    # Save last section
    if current_section and current_items:
        _save_section(reflection, current_section, current_items)

    return reflection


def _save_section(reflection: dict, section: str, items: list[str]) -> None:
    """Save parsed items to the appropriate reflection field."""
    section_lower = section.lower()

    if "discover" in section_lower or "pattern" in section_lower and "watch" not in section_lower:
        reflection["discoveries"].extend(items)
    elif "improvement" in section_lower and "made" in section_lower:
        reflection["improvements_made"].extend(items)
    elif "issue" in section_lower or "created" in section_lower:
        reflection["issues_created"].extend(items)
    elif "question" in section_lower:
        reflection["open_questions"].extend(items)
    elif "watch" in section_lower or "pattern" in section_lower:
        reflection["patterns_to_watch"].extend(items)
    elif "anti" in section_lower:
        reflection["anti_patterns"].extend(items)


def extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords from text."""
    # Common words to skip
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "shall", "can", "to", "of", "in",
        "for", "on", "with", "at", "by", "from", "as", "into", "through",
        "during", "before", "after", "above", "below", "between", "under",
        "again", "further", "then", "once", "here", "there", "when", "where",
        "why", "how", "all", "each", "few", "more", "most", "other", "some",
        "such", "no", "nor", "not", "only", "own", "same", "so", "than",
        "too", "very", "just", "but", "and", "or", "if", "this", "that",
        "these", "those", "it", "its", "i", "we", "you", "he", "she", "they",
        "added", "updated", "created", "fixed", "issue", "bd", "see", "also",
    }

    # Extract words
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9_-]+\b", text.lower())

    # Filter and return meaningful keywords
    return [w for w in words if w not in stop_words and len(w) > 2]


def analyze_recurring_themes(reflections: list[dict]) -> dict:
    """Analyze reflections for recurring themes and patterns."""
    # Count keywords across all reflections
    discovery_keywords = Counter()
    improvement_keywords = Counter()
    question_keywords = Counter()
    pattern_keywords = Counter()

    keyword_dates = {}  # Track which dates mention each keyword

    for r in reflections:
        date = r.get("date", "unknown")

        for discovery in r.get("discoveries", []):
            for kw in extract_keywords(discovery):
                discovery_keywords[kw] += 1
                keyword_dates.setdefault(kw, set()).add(date)

        for improvement in r.get("improvements_made", []):
            for kw in extract_keywords(improvement):
                improvement_keywords[kw] += 1

        for question in r.get("open_questions", []):
            for kw in extract_keywords(question):
                question_keywords[kw] += 1
                keyword_dates.setdefault(kw, set()).add(date)

        for pattern in r.get("patterns_to_watch", []):
            for kw in extract_keywords(pattern):
                pattern_keywords[kw] += 1

    # Find keywords mentioned in multiple sessions (recurring)
    recurring = {
        kw: {"count": count, "dates": sorted(keyword_dates.get(kw, []))}
        for kw, count in discovery_keywords.most_common(20)
        if count >= 2  # Only include if mentioned 2+ times
    }

    return {
        "discovery_keywords": dict(discovery_keywords.most_common(15)),
        "improvement_keywords": dict(improvement_keywords.most_common(15)),
        "question_keywords": dict(question_keywords.most_common(10)),
        "pattern_keywords": dict(pattern_keywords.most_common(10)),
        "recurring_across_sessions": recurring,
    }


def main():
    # Parse arguments
    reflections_dir = Path("history/reflections")
    output_json = "--json" in sys.argv

    # Check for directory argument
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            reflections_dir = Path(arg)
            break

    if not reflections_dir.exists():
        print(json.dumps({"error": f"Directory not found: {reflections_dir}"}))
        sys.exit(1)

    # Find all reflection files
    reflection_files = sorted(reflections_dir.glob("*.md"), reverse=True)

    if not reflection_files:
        print(json.dumps({"error": "No reflection files found", "searched": str(reflections_dir)}))
        sys.exit(1)

    # Parse all reflections
    reflections = []
    for filepath in reflection_files:
        parsed = parse_reflection_file(filepath)
        if parsed:
            reflections.append(parsed)

    # Analyze themes
    themes = analyze_recurring_themes(reflections)

    # Build output
    output = {
        "timestamp": datetime.now().isoformat(),
        "reflections_dir": str(reflections_dir),
        "total_reflections": len(reflections),
        "reflections": reflections,
        "recurring_themes": themes,
    }

    if output_json:
        print(json.dumps(output, indent=2))
    else:
        # Human-readable summary
        print("=" * 60)
        print("REFLECTION HISTORY SUMMARY")
        print("=" * 60)
        print(f"Directory: {reflections_dir}")
        print(f"Total Reflections: {len(reflections)}")
        print()

        print("Recent Reflections:")
        for r in reflections[:5]:
            print(f"  - {r['date']}: {r['topic']}")
            if r["summary"]:
                print(f"    {r['summary'][:60]}...")
        print()

        print("Recurring Themes (mentioned 2+ times across sessions):")
        for kw, data in list(themes["recurring_across_sessions"].items())[:10]:
            dates = ", ".join(data["dates"][-3:])
            print(f"  - {kw}: {data['count']} mentions ({dates})")
        print()

        print("Top Discovery Keywords:")
        for kw, count in list(themes["discovery_keywords"].items())[:8]:
            print(f"  - {kw}: {count}")
        print()

        print("Open Question Keywords (potential recurring issues):")
        for kw, count in list(themes["question_keywords"].items())[:5]:
            print(f"  - {kw}: {count}")

        print()
        print("Run with --json for full structured output")


if __name__ == "__main__":
    main()
