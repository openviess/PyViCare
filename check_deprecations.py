#!/usr/bin/env python3
"""Check for deprecated Viessmann API features and maintain the deprecation database.

Usage:
    check_deprecations.py                  Report using the database
    check_deprecations.py --update         Rescan test data, update database
    check_deprecations.py --update f.json  Also ingest a fresh device dump

The database (tests/deprecated_features.json) accumulates deprecation info from
test response files and fresh device dumps. Features deprecated in one API response
are deprecated everywhere, so we merge and propagate across all sources.

Exit code 1 if deprecated features are used in code (outside the ignore list).
"""

import argparse
import glob
import json
import re
import sys
from collections import OrderedDict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent
DB_PATH = ROOT / "tests" / "deprecated_features.json"
RESPONSE_DIR = ROOT / "tests" / "response"
PYVICARE_DIR = ROOT / "PyViCare"


def load_database():
    """Load the deprecation database, or return empty if it doesn't exist."""
    if DB_PATH.exists():
        with open(DB_PATH) as f:
            data = json.load(f)
        return data.get("features", {})
    return {}


def save_database(features):
    """Save the deprecation database."""
    output = {
        "_meta": {
            "description": "Known deprecated Viessmann API features, merged from test data and device dumps.",
            "updated": str(date.today()),
            "feature_count": len(features),
        },
        "features": OrderedDict(sorted(features.items())),
    }
    with open(DB_PATH, "w") as f:
        json.dump(output, f, indent=2)
        f.write("\n")


def scan_json_file(filepath, source_label):
    """Extract deprecated features from a JSON file. Returns dict of feature -> info."""
    found = {}
    with open(filepath) as f:
        data = json.load(f)

    items = data.get("data", data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        return found

    for item in items:
        dep = item.get("deprecated")
        if dep:
            feat = item["feature"]
            found[feat] = {
                "removalDate": dep.get("removalDate", ""),
                "info": dep.get("info", ""),
                "source": source_label,
            }
    return found


def update_database(extra_files=None):
    """Rescan test data and optional extra files, merge into database. Returns new features."""
    db = load_database()
    new_features = {}
    today = str(date.today())

    def add_feature(feat, info, source_label):
        if feat not in db:
            db[feat] = {
                "removalDate": info["removalDate"],
                "info": info["info"],
                "firstSeenIn": source_label,
                "firstSeenOn": today,
                "sources": [],
            }
            new_features[feat] = {**info, "source": source_label}
        if source_label not in db[feat]["sources"]:
            db[feat]["sources"].append(source_label)

    # Scan test response files
    for filepath in sorted(glob.glob(f"{RESPONSE_DIR}/*.json")):
        filename = Path(filepath).name
        for feat, info in scan_json_file(filepath, filename).items():
            add_feature(feat, info, filename)

    # Scan extra dump files
    for filepath in extra_files or []:
        path = Path(filepath)
        if not path.exists():
            print(f"Warning: {filepath} not found, skipping", file=sys.stderr)
            continue
        label = f"dump:{path.name}"
        for feat, info in scan_json_file(filepath, label).items():
            add_feature(feat, info, label)

    save_database(db)
    return new_features


def find_code_usage():
    """Find all feature paths referenced via getProperty() in PyViCare code."""
    usage = {}  # feature pattern -> [files]
    sources = {}  # filename -> full source content

    for filepath in sorted(glob.glob(f"{PYVICARE_DIR}/**/*.py", recursive=True)):
        filename = Path(filepath).name
        with open(filepath) as f:
            content = f.read()
        sources[filename] = content

        for match in re.findall(r'getProperty\(\s*f?"([^"]+)"\s*\)', content):
            normalized = re.sub(r"\{[^}]+\}", "*", match)
            if normalized not in usage:
                usage[normalized] = []
            usage[normalized].append(filename)

    return usage, sources


def feature_matches_code(feature, code_usage, sources):
    """Check if a deprecated feature is used in code.

    For wildcard matches (e.g., heating.circuits.*.operating.programs.*),
    verifies that the specific segment value appears as a string literal
    in the source file to avoid false positives from dynamic iteration.
    """
    matching_files = []
    for pattern, files in code_usage.items():
        if "*" in pattern:
            regex = re.escape(pattern).replace(r"\*", r"([^.]+)")
            m = re.fullmatch(regex, feature)
            if m:
                segments = m.groups()
                all_confirmed = True
                for seg in segments:
                    if seg.isdigit():
                        continue
                    for f in files:
                        if f"'{seg}'" in sources.get(f, "") or f'"{seg}"' in sources.get(f, ""):
                            break
                    else:
                        all_confirmed = False
                if all_confirmed:
                    matching_files.extend(files)
        elif pattern == feature:
            matching_files.extend(files)
    return list(set(matching_files))


def report(db):
    """Print deprecation report and return exit code."""
    code_usage, sources = find_code_usage()
    today = date.today()

    used_in_code = []
    past_due = []
    upcoming = []

    for feature in sorted(db):
        info = db[feature]
        removal_str = info.get("removalDate", "")
        replacement = info.get("info", "")
        feature_sources = info.get("sources", [])
        code_files = feature_matches_code(feature, code_usage, sources)

        try:
            removal_date = datetime.strptime(removal_str, "%Y-%m-%d").date()
            is_past_due = removal_date <= today
            days = (removal_date - today).days
            date_label = f"{removal_str} ({'PAST DUE' if is_past_due else f'{days} days left'})"
        except (ValueError, TypeError):
            removal_date = None
            is_past_due = False
            date_label = removal_str or "unknown"

        entry = {
            "feature": feature,
            "date_label": date_label,
            "replacement": replacement,
            "sources": feature_sources,
            "code_files": code_files,
            "is_past_due": is_past_due,
        }

        if code_files:
            used_in_code.append(entry)
        elif is_past_due:
            past_due.append(entry)
        else:
            upcoming.append(entry)

    def print_entry(entry):
        print(f"  {entry['feature']}")
        print(f"    Removal: {entry['date_label']}")
        if entry["replacement"] and entry["replacement"] != "none":
            print(f"    Replaced by: {entry['replacement']}")
        if entry.get("code_files"):
            print(f"    Used in code: {', '.join(entry['code_files'])}")
        dump_sources = [s for s in entry.get("sources", []) if s.startswith("dump:")]
        if dump_sources:
            print(f"    From dump: {', '.join(s.removeprefix('dump:') for s in dump_sources)}")
        print()

    def collapse_entries(entries):
        """Group entries that only differ by numeric indices (e.g. rooms.0, rooms.1)."""
        groups = {}  # pattern -> {entry (first), count}
        for entry in entries:
            pattern = re.sub(r"\b\d+\b", "*", entry["feature"])
            if pattern in groups:
                groups[pattern]["count"] += 1
            else:
                collapsed = dict(entry)
                collapsed["feature"] = pattern
                groups[pattern] = {"entry": collapsed, "count": 1}
        result = []
        for pattern, group in groups.items():
            entry = group["entry"]
            if group["count"] > 1:
                entry["feature"] = f"{pattern} ({group['count']}x)"
            result.append(entry)
        return result

    if used_in_code:
        print("=== WARNING: Deprecated features used in code ===\n")
        for entry in collapse_entries(used_in_code):
            print_entry(entry)

    if past_due:
        print(f"=== Past removal date (not used in code): {len(past_due)} features ===\n")
        for entry in collapse_entries(past_due):
            print_entry(entry)

    if upcoming:
        print("=== Upcoming deprecations ===\n")
        for entry in collapse_entries(upcoming):
            print_entry(entry)

    total = len(db)
    in_code = len(used_in_code)
    print("=== Summary ===")
    print(f"{total} deprecated features in database")
    print(f"{in_code} used in code {'(ACTION NEEDED)' if in_code else '(clean)'}")
    print(f"{len(past_due)} past removal date")
    print(f"{len(upcoming)} upcoming")

    return 1 if in_code else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--update", action="store_true", help="Rescan test data and update the database")
    parser.add_argument("dumps", nargs="*", help="Additional dump files to ingest (implies --update)")
    args = parser.parse_args()

    if args.dumps:
        args.update = True

    if args.update:
        new = update_database(args.dumps)
        if new:
            print(f"=== {len(new)} NEW deprecated features found ===\n")
            for feat, info in sorted(new.items()):
                print(f"  {feat}")
                print(f"    Removal: {info['removalDate']}")
                if info["info"] and info["info"] != "none":
                    print(f"    Replaced by: {info['info']}")
                print(f"    Discovered in: {info['source']}")
                print()
        else:
            print("Database up to date, no new deprecated features found.\n")

    db = load_database()
    if not db:
        print("No deprecation database found. Run with --update first.", file=sys.stderr)
        sys.exit(1)

    sys.exit(report(db))


if __name__ == "__main__":
    main()
