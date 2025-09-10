# KAIROS — Паспорт проекта
version: 0.3.0
status: canon
updated_at: 2025-09-10
owner: NeuroReturn™ Engineering
repo_root: 08-agents/KAIROS/

![KAIROS CI](https://github.com/NeuroReturn/NeuroReturn/actions/workflows/kairos-ci.yml/badge.svg?branch=main)

> Назначение: CI-валидируемый агент для фазового восстановления субъектности (NeuroReturn™). Ноль мотивации, максимум проверяемости.

---

## 1) Контур и артефакты (минимум)
08-agents/KAIROS/
├─ schemas/
│ └─ frontmatter.schema.json
├─ scripts/
│ ├─ json_schema_check.py
│ └─ nr_fm.py
├─ pipelines/
│ └─ validation_ci.spec.yaml # спека CI (не исполняется)
├─ tests/
│ └─ fixtures/
│ └─ frontmatter/
│ ├─ good/
│ │ ├─ fm_policy.canon.json
│ │ └─ example_frontmatter_spec.json
│ └─ bad/
│ ├─ fm_bad_phase.json
│ ├─ fm_bad_version.json
│ ├─ fm_bad_status.json
│ ├─ fm_bad_id.json
│ └─ fm_bad_date.json
└─ Makefile

markdown
Копировать код

## 2) CI (источник истины)
Исполняемый workflow: `.github/workflows/kairos-ci.yml`  
Проверяет:
- **Sanity verify paths** — ключевые пути существуют.
- **Spec vs workflow sync check** — сверка с `08-agents/KAIROS/pipelines/validation_ci.spec.yaml`.
- **Schema self-check** — валидность `schemas/frontmatter.schema.json`.
- **Fixture validate** — пакетная проверка `good/*.json` и `bad/*.json`.
- **Make ci-validate** — `schema.check` + `fm.validate`.

## 3) Локальная валидация (не обязательна)
```bash
# из корня репозитория
pip install -r requirements.txt

# проверить схему
python 08-agents/KAIROS/scripts/json_schema_check.py \
  08-agents/KAIROS/schemas/frontmatter.schema.json

# проверить все примеры
python 08-agents/KAIROS/scripts/nr_fm.py \
  --schema 08-agents/KAIROS/schemas/frontmatter.schema.json \
  --base   08-agents/KAIROS/tests/fixtures/frontmatter

# Makefile (если установлен make)
make -C 08-agents/KAIROS ci-validate
4) Политика именования ID
Допустимые форматы:

NR_001_Name-Of-Thing

NR-AB-F0-Name-Of-Thing (AB — 2 латинские буквы; F0..F3 — фаза)

KAIROS_Name-Of-Thing (после KAIROS_ только [A-Za-z0-9-])

Пример канона: KAIROS_FM-Policy.

5) Acceptance
Все tests/fixtures/frontmatter/good/*.json проходят схему.

Все tests/fixtures/frontmatter/bad/*.json падают по схеме (и считаются OK).

KAIROS CI зелёный обязателен для merge в main.

6) Релизы
v0.3.0 — базовый CI, фронтматтер-схема, фикстуры, спека CI, Makefile.

v0.4.0 (план) — отчёт валидатора как artifact, автогенерация шаблонов фронтматтера, PR-template и CODEOWNERS.

yaml
Копировать код

---

# Слой 2 — Пояснение
Твои текущие проблемы были сугубо технические: незакрытый ```bash-блок «съедал» пол-README, заголовки «4)…6)» выпадали из структуры, а дерево каталогов без кода выглядело как случайный текст. Исправленная версия закрывает блоки, нормализует пути и фиксирует ссылку на спека-файл именно с полным префиксом. Теперь это читаемо человеком и предсказуемо для новых контрибьюторов. :contentReference[oaicite:1]{index=1}

Запихни файл как есть и жми ран. Если зелёный, идём к v0.4.0: отчёт валидатора как artifact и автогенерация шаблонов фронтматтера.
