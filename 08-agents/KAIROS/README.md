# NeuroReturn / KAIROS

![KAIROS CI](https://github.com/NeuroReturn/NeuroReturn/actions/workflows/kairos-ci.yml/badge.svg?branch=main)
[Страница ранoв CI](https://github.com/NeuroReturn/NeuroReturn/actions/workflows/kairos-ci.yml)

## Назначение
Строгий CI для валидации фронтматтера по JSON Schema и прогон фикстур (`good/`, `bad/`) в проекте KAIROS.

## Где смотреть результаты
- **Job Summary** (вверху страницы рана) — Markdown‑сводка по всем файлам.
- **Artifacts → `fm-summary`** — `08-agents/KAIROS/observability/fm_summary.json` (машиночитаемая сводка).

## Ручной прогон CI
1. GitHub → **Actions** → **KAIROS CI** → **Run workflow** → Branch: `main` → **Run**.
2. Открыть свежий ран → **Summary** и **Artifacts**.

## Релизы
Релизный workflow публикует GitHub Release и прикрепляет `fm_summary.json`:
1. GitHub → **Actions** → **KAIROS Release** → **Run workflow**.
2. Поле **version**: `v0.3.0` (или другая семантическая версия) → **Run**.
3. Проверить: **Releases** → создан релиз, прикреплён `fm_summary.json`.

## Структура
```
.github/workflows/kairos-ci.yml
.github/workflows/release.yml
08-agents/KAIROS/scripts/nr_fm.py
08-agents/KAIROS/scripts/json_schema_check.py
08-agents/KAIROS/schemas/frontmatter.schema.json
08-agents/KAIROS/tests/fixtures/frontmatter/{good,bad}/*.json
08-agents/KAIROS/observability/fm_summary.json   # создаётся на ранe
```

## Сверка спеки и workflow
Спека пайплайна: `08-agents/KAIROS/pipelines/validation_ci.spec.yaml`.  

В ранe запускается шаг `Spec vs workflow sync check`, предотвращающий расхождение спеки и workflow.

## Локальная валидация (опционально)
```bash
# из корня репозитория
pip install -r requirements.txt

# проверить схему
python 08-agents/KAIROS/scripts/json_schema_check.py   08-agents/KAIROS/schemas/frontmatter.schema.json

# прогнать фикстуры
python 08-agents/KAIROS/scripts/nr_fm.py   --schema 08-agents/KAIROS/schemas/frontmatter.schema.json   --base   08-agents/KAIROS/tests/fixtures/frontmatter
```
_Обновлено: 2025-09-10 UTC_
