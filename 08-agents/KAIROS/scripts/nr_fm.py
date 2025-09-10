#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nr_fm.py — валидатор фронтматтера (JSON Schema) с режимами:
  --base <dir>   : пакетная проверка good/ и bad/
  --file <file>  : проверка одного файла
Дополнительно:
  --output {text,json,md}  : формат основного вывода (по умолчанию text)
  --summary <path>         : путь для записи JSON-сводки (всегда JSON)
  --gh-summary             : если установлен, пишет Markdown в $GITHUB_STEP_SUMMARY

Коды выхода:
  0 — все good прошли, все bad упали (как и должны)
  1 — есть отклонения (good не прошёл или bad «вдруг прошёл»)
  2 — ошибка использования/IO/схемы
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

from jsonschema import Draft202012Validator, ValidationError

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def validate_instance(validator: Draft202012Validator, instance_path: Path) -> Tuple[bool, str]:
    try:
        instance = load_json(instance_path)
        validator.validate(instance)
        return True, ""
    except ValidationError as e:
        # компактное сообщение
        loc = "/".join([str(p) for p in e.path]) or "(root)"
        msg = f"{e.message} [at: {loc}; validator: {e.validator}]"
        return False, msg

def collect_files(base: Path) -> Tuple[List[Path], List[Path]]:
    good_dir = base / "good"
    bad_dir  = base / "bad"
    good = sorted([p for p in good_dir.glob("*.json") if p.is_file()]) if good_dir.exists() else []
    bad  = sorted([p for p in bad_dir.glob("*.json")  if p.is_file()]) if bad_dir.exists() else []
    return good, bad

def make_summary(schema: Path, base: Path, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    good_total = sum(1 for r in results if r["group"] == "good")
    bad_total  = sum(1 for r in results if r["group"] == "bad")
    good_pass  = sum(1 for r in results if r["group"] == "good" and r["status"] == "pass")
    good_fail  = sum(1 for r in results if r["group"] == "good" and r["status"] == "fail")
    bad_expected_fail   = sum(1 for r in results if r["group"] == "bad" and r["status"] == "expected_fail")
    bad_unexpected_pass = sum(1 for r in results if r["group"] == "bad" and r["status"] == "unexpected_pass")

    return {
        "schema": str(schema),
        "base": str(base) if base else None,
        "counts": {
            "good_total": good_total,
            "good_pass": good_pass,
            "good_fail": good_fail,
            "bad_total": bad_total,
            "bad_expected_fail": bad_expected_fail,
            "bad_unexpected_pass": bad_unexpected_pass
        },
        "files": results,
    }

def emit_markdown(summary: Dict[str, Any]) -> str:
    c = summary["counts"]
    lines = []
    lines.append("## Frontmatter validation summary")
    lines.append("")
    lines.append(f"- **Schema**: `{summary['schema']}`")
    if summary["base"]:
        lines.append(f"- **Base**: `{summary['base']}`")
    lines.append("")
    lines.append("| Group | File | Status | Detail |")
    lines.append("|---|---|---|---|")
    for r in summary["files"]:
        detail = r.get("error", "") or ""
        if len(detail) > 140:
            detail = detail[:137] + "..."
        lines.append(f"| {r['group']} | `{r['path']}` | {r['status']} | {detail} |")
    lines.append("")
    lines.append(f"**Totals:** good {c['good_pass']}/{c['good_total']} pass; "
                 f"bad expected-fail {c['bad_expected_fail']}/{c['bad_total']}; "
                 f"bad unexpected-pass {c['bad_unexpected_pass']}")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True, help="path to JSON Schema")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--base", help="base dir with good/ and bad/ subdirs")
    group.add_argument("--file", help="single JSON file to validate")
    ap.add_argument("--output", choices=["text", "json", "md"], default="text")
    ap.add_argument("--summary", help="path to write JSON summary file")
    ap.add_argument("--gh-summary", action="store_true", help="write Markdown into $GITHUB_STEP_SUMMARY if set")
    args = ap.parse_args()

    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"[ERROR] Schema not found: {schema_path}", file=sys.stderr)
        return 2

    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    results: List[Dict[str, Any]] = []
    exit_code = 0

    if args.base:
        base = Path(args.base)
        good, bad = collect_files(base)

        # good: must pass
        for p in good:
            ok, err = validate_instance(validator, p)
            if ok:
                print(f"[OK] {p}")
                results.append({"path": str(p), "group": "good", "status": "pass"})
            else:
                print(f"[FAIL: expected pass] {p}\n{err}")
                results.append({"path": str(p), "group": "good", "status": "fail", "error": err})
                exit_code = 1

        # bad: must fail
        for p in bad:
            ok, err = validate_instance(validator, p)
            if ok:
                print(f"[FAIL: expected fail] {p} — validated but should fail")
                results.append({"path": str(p), "group": "bad", "status": "unexpected_pass"})
                exit_code = 1
            else:
                print(f"[OK] {p} (expected fail)")
                results.append({"path": str(p), "group": "bad", "status": "expected_fail", "error": err})

        summary = make_summary(schema_path, base, results)

    else:
        f = Path(args.file)
        ok, err = validate_instance(validator, f)
        if ok:
            print(f"[OK] {f}")
            results.append({"path": str(f), "group": "single", "status": "pass"})
            summary = {
                "schema": str(schema_path),
                "file": str(f),
                "counts": {"pass": 1, "fail": 0},
                "files": results
            }
        else:
            print(f"[FAIL] {f}\n{err}")
            results.append({"path": str(f), "group": "single", "status": "fail", "error": err})
            summary = {
                "schema": str(schema_path),
                "file": str(f),
                "counts": {"pass": 0, "fail": 1},
                "files": results
            }
            exit_code = 1

    # write summary file if requested
    if args.summary:
        out = Path(args.summary)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[INFO] JSON summary written to: {out}")

    # write GitHub Job Summary if requested
    if args.gh_summary:
        gh_path = os.getenv("GITHUB_STEP_SUMMARY")
        if gh_path:
            Path(gh_path).write_text(emit_markdown(summary) + "\n", encoding="utf-8")
            print(f"[INFO] Markdown summary written to $GITHUB_STEP_SUMMARY")

    # main output format
    if args.output == "json":
        print(json.dumps(summary, ensure_ascii=False))
    elif args.output == "md":
        print(emit_markdown(summary))

    return exit_code

if __name__ == "__main__":
    sys.exit(main())
