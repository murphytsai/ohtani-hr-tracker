#!/usr/bin/env python3
"""Audit MLB highlight links and apply durable manual video overrides."""

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


POSITIVE_PATTERNS = (
    r"\bhome run\b",
    r"\bhomer(?:s|ed)?\b",
    r"\bhr\b",
    r"\bbig fly\b",
)
INVALID_PATTERNS = {
    "strikeout_video": (r"\bstrikes? out\b", r"\bfans? (?:shohei )?ohtani\b"),
}
REVIEW_PATTERNS = {
    "interview_or_reaction": (
        r"\binterview\b", r"\breacts?\b", r"\bon .*home runs?\b",
        r"\bdiscuss(?:es|ing)?\b", r"\btalks? about\b",
    ),
    "analysis_not_play": (r"\bdeep dive\b", r"\bdata viz\b", r"\bbat tracking\b"),
    "game_recap": (r"\brecap\b",),
}


def _matches(patterns, text):
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def assess_video(hr):
    """Return (status, confidence, reason) using deliberately conservative rules."""
    url = (hr.get("video_url") or "").strip()
    title = (hr.get("video_title") or "").strip()
    text = title.lower()

    if not url:
        return "missing", 0.0, "no_video_url"
    if not title:
        return "review", 0.25, "missing_title"
    if "ohtani" not in text:
        return "review", 0.35, "title_missing_ohtani"
    for reason, patterns in INVALID_PATTERNS.items():
        if _matches(patterns, text):
            return "invalid", 0.0, reason
    for reason, patterns in REVIEW_PATTERNS.items():
        if _matches(patterns, text):
            return "review", 0.3, reason
    if not _matches(POSITIVE_PATTERNS, text):
        return "review", 0.4, "title_missing_home_run_term"

    number_matches = [int(n) for n in re.findall(r"\((\d{1,3})\)", title)]
    season_number = hr.get("season_hr_num")
    if number_matches and season_number and season_number not in number_matches:
        return "review", 0.45, "season_hr_number_mismatch"

    return "probable", 0.8, "title_matches_home_run"


def load_overrides(path):
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    entries = raw.get("overrides", raw) if isinstance(raw, dict) else raw
    return {int(item["hr_num"]): item for item in entries}


def apply_overrides(rows, overrides):
    for hr in rows:
        override = overrides.get(int(hr.get("hr_num", -1)))
        if not override:
            continue
        expected_date = override.get("date")
        if expected_date and expected_date != hr.get("date"):
            raise ValueError(
                f"Override HR #{hr.get('hr_num')} expects {expected_date}, "
                f"but dataset contains {hr.get('date')}"
            )
        action = override.get("action", "replace")
        if action == "remove":
            hr["video_url"] = None
            hr["video_title"] = None
            hr["video_thumbnail"] = None
        elif action == "replace":
            for field in ("video_url", "video_title", "video_thumbnail"):
                if field in override:
                    hr[field] = override[field]
        else:
            raise ValueError(f"Unknown override action for HR #{hr.get('hr_num')}: {action}")
        hr["video_override"] = True
    return rows


def audit(rows):
    results = []
    urls = defaultdict(list)
    for hr in rows:
        if hr.get("video_url"):
            urls[hr["video_url"]].append(hr)

    for hr in rows:
        status, confidence, reason = assess_video(hr)
        same_url = urls.get(hr.get("video_url"), [])
        if len(same_url) > 1:
            distinct_dates = {item.get("date") for item in same_url}
            if len(distinct_dates) > 1:
                status, confidence, reason = "invalid", 0.0, "duplicate_url_across_dates"
            elif status == "probable":
                status, confidence, reason = "review", 0.55, "duplicate_url_same_game"
        results.append({
            "hr_num": hr.get("hr_num"),
            "season_hr_num": hr.get("season_hr_num"),
            "date": hr.get("date"),
            "pitcher_name": hr.get("pitcher_name"),
            "video_title": hr.get("video_title") or "",
            "video_url": hr.get("video_url") or "",
            "status": status,
            "confidence": f"{confidence:.2f}",
            "reason": reason,
        })
    return results


def write_report(results, path):
    fields = list(results[0]) if results else ["hr_num", "status", "reason"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="ohtani_hrs.json")
    parser.add_argument("--report", default="video_audit_report.csv")
    parser.add_argument("--overrides", default="manual_video_overrides.json")
    parser.add_argument("--apply", action="store_true", help="Apply overrides back to the input JSON")
    args = parser.parse_args()

    input_path = Path(args.input)
    rows = json.loads(input_path.read_text(encoding="utf-8"))
    overrides = load_overrides(Path(args.overrides))
    if args.apply:
        apply_overrides(rows, overrides)
        input_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    results = audit(rows)
    write_report(results, Path(args.report))
    counts = {status: sum(r["status"] == status for r in results) for status in ("invalid", "review", "probable", "missing")}
    print(f"Audited {len(results)} records: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    print(f"Report: {args.report}")


if __name__ == "__main__":
    main()
