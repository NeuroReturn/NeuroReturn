#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ci_spec_check.py — сверяет исполняемый workflow с контрактом из spec.
Без внешних зависимостей (PyYAML не нужен).

Usage (из корня репо):
  python 08-agents/KAIROS/scripts/ci_spec_check.py \
    --spec 08-agents/KAIROS/pipelines/validation_ci.spec.yaml \
    --workflow .github/workflows/kairos-ci.yml

Exit codes: 0 — OK, 1 — нарушения.
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
    """
    Мини-парсер YAML-лайк структуры:
    - читаем только блок 'contract:' до любого другого верхнеуровневого ключа
    - собираем элементы must_contain только внутри текущего id-блока
    """
    lines = spec_text.splitlines()
    in_contract = False
    blocks = []
    current = None
    collecting = False

    for raw in lines:
        line = raw.rstrip("\n")

        # Входим в contract
        if re.match(r"^\s*contract\s*:\s*$", line):
            in_contract = True
            current = None
            collecting = False
            continue

        # Любой другой верхнеуровневый ключ завершает contract
        if in_contract and re.match(r"^[A-Za-z0-9_]+\s*:\s*$", line):
            # это новый ключ верхнего уровня (например version:, pipeline_name:)
            # завершаем обработку contract
            if current:
                blocks.append(current)
                current = None
            in_contract = False
            collecting = False
            continue

        if not in_contract:
            continue

        # Новый блок id
        m_id = re.match(r"^\s*-\s+id:\s*(.+?)\s*$", line)
        if m_id:
            if current:
                blocks.append(current)
            current = {"id": m_id.group(1).strip().strip('"'), "items": []}
            collecting = False
            continue

        # Старт списка must_contain
        if current and re.match(r"^\s*must_contain\s*:\s*$", line):
            collecting = True
            continue

        # Элементы must_contain
        if current and collecting:
            m_item = re.match(r"^\s*-\s+(.+?)\s*$", line)
            if m_item:
                item = m_item.group(1).strip().strip('"')
                current["items"].append(item)
                continue
            # закончился список (следующая строка не начинается с "- ")
            # не сбрасываем collecting насильно, но элементы уже не добавятся

    if current:
        blocks.append(current)
    return blocks

def main():
    args = parse_args()
    spec = Path(args.spec)
    wf = Path(args.workflow)
    if not spec.exists():
        print(f"[ERROR] Spec not found: {spec}", file=sys.stderr); return 1
    if not wf.exists():
        print(f"[ERROR] Workflow not found: {wf}", file=sys.stderr); return 1

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
