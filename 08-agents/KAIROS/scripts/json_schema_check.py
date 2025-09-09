#!/usr/bin/env python3
import sys, json
from jsonschema import Draft202012Validator

def main():
    if len(sys.argv) < 2:
        print("Usage: json_schema_check.py <schema.json>")
        sys.exit(2)
    schema_path = sys.argv[1]
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    Draft202012Validator.check_schema(schema)
    print(f"SCHEMA OK: {schema_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ci_spec_check.py — проверяет, что исполняемый GitHub Actions workflow соответствует контракту из spec.
Использование (из корня репо):
  python 08-agents/KAIROS/scripts/ci_spec_check.py \
    --spec 08-agents/KAIROS/pipelines/validation_ci.spec.yaml \
    --workflow .github/workflows/kairos-ci.yml
Код выхода: 0 — ок, 1 — нарушение контракта.
"""
import argparse, sys, re
from pathlib import Path

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--workflow", required=True)
    return ap.parse_args()

def extract_contract(spec_text: str):
    # очень простой извлекатель: ищем блоки id/must_contain
    blocks = []
    current = None
    for line in spec_text.splitlines():
        if re.match(r"^\s*-\s+id:\s*", line):
            if current: blocks.append(current)
            current = {"id": line.split(":",1)[1].strip().strip('"')}
        elif re.match(r"^\s*-\s+", line) and current is not None and "must_contain" in current:
            # строка must_contain уже открыта; просто добавляем элемент
            current.setdefault("items", []).append(line.strip().lstrip("- ").strip().strip('"'))
        elif "must_contain:" in line and current is not None:
            current["must_contain"] = True
            current["items"] = []
    if current: blocks.append(current)
    # нормализуем
    for b in blocks:
        b["items"] = b.get("items", [])
    return blocks

def main():
    args = parse_args()
    spec = Path(args.spec)
    wf = Path(args.workflow)
    if not spec.exists():
        print(f"[ERROR] Spec not found: {spec}", file=sys.stderr)
        return 1
    if not wf.exists():
        print(f"[ERROR] Workflow not found: {wf}", file=sys.stderr)
        return 1

    spec_text = read(spec)
    wf_text = read(wf)

    violations = []
    for block in extract_contract(spec_text):
        missing = [pat for pat in block["items"] if pat not in wf_text]
        if missing:
            violations.append((block["id"], missing))

    if violations:
        print("Spec violations detected:")
        for sid, miss in violations:
            print(f"  - Step '{sid}':")
            for m in miss:
                print(f"      missing pattern: {m}")
        return 1

    print("Spec check: OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
