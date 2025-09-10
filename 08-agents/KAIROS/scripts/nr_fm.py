#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nr_fm.py — валидатор фронтматтера (JSON Schema).

Режимы:
  --base <dir>   : пакетная проверка good/ и bad/
  --file <file>  : проверка одного файла

Дополнительно:
  --output {text,json,md}  : формат stdout (по умолчанию text)
  --summary <path>         : запись JSON-сводки (всегда JSON)
  --gh-summary             : пишет Markdown в $GITHUB_STEP_SUMMARY

Коды выхода:
  0 — все good прошли, все bad упали (как и должны)
  1 — отклонения (good не прошёл или bad «вдруг прошёл»)
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


def validate_instance(
    validator: Draft202012Validator, instance_path: Path
) -> Tuple[bool, str]:
    try:
        instance = load_json(instance_path)
        validator.validate(instance)
        return True, ""
    except ValidationError as e:
        loc = "/".join([str(p) for p in e.path]) or "(root)"
        msg = f"{e.message} [at: {loc}; validator: {e.validator}]"
        return False, msg


def collect_files(base: Path) -> Tuple[List[Path], List[Path]]:
    good_dir = base / "good"
    bad_dir = base / "bad"
    good = (
        sorted([p for p in good_dir.glob("*.json") if p.is_file()])
        if good_dir.exists()
        else []
    )
    bad = (
        sorted([p for p in bad_dir.glob("*.json") if p.is_file()])
        if bad_dir.exists()
        else []
    )
    return good, bad


def make_summary(schema: Path, base: Path, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    # аккуратно считаем показатели; НИКАКИХ "=" в условиях, только "=="
    good_total = sum(1 for r in results if r["group"] == "good")
    bad_total = sum(1 for r in results if r["group"] == "bad")

    good_pass = sum(1 for r in results if r["group"] == "good" and r["status"] == "pass")
    good_fail = sum(1 for r in results if r["group"] == "good" and r["status"] == "fail")

    bad_expected_fail = sum(
        1 for r in results if r["group"] == "bad" and r["status"] == "expected_fail"
    )
    bad_unexpected_pass = sum(
        1 for r in results if r["group"] == "bad" and r["status"] == "unexpected_pass"
    )

    return {
        "schema": str(schema),
        "base": str(base) if base else None,
        "counts": {
            "good_total": good_total,
            "good_pass": good_pass,
            "good_fail": good_fail,
            "bad_total": bad_total,
            "bad_expected_fail": bad_expected_fail,
            "bad_unexpected_pass": bad_unexpected_pass,
        },
        "files": results,
    }


def emit_markdown(summary: Dict[str, Any]) -> str:
    c = summary["counts"]
    lines = []
    lines.append("## Frontmatter validation summary")
    lines.append("")
    lines.append(f"- **Schema**: `{summary['schema']}`")
    if summary.get("base"):
        lines.append(f"- **Base**: `{summary['base']}`")
    lines.append("")
    lines.append("| Group | File | St
