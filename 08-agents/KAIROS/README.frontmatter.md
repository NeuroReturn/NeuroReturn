# KAIROS Frontmatter — quick start

Этот файл — короткая памятка по локальной проверке фронтматтера (metadata) с помощью схемы JSON Schema.

## Быстрый запуск (локально)

1) Установи Python 3.11+ и зависимости:
```bash
pip install -r requirements.txt
```

2) Запусти валидатор примеров (good/bad):
```bash
python 08-agents/KAIROS/scripts/nr_fm.py       --schema 08-agents/KAIROS/schemas/frontmatter.schema.json       --base   08-agents/KAIROS/tests/fixtures/frontmatter
```

3) Проверить один JSON можно так:
```bash
python 08-agents/KAIROS/scripts/nr_fm.py       --schema 08-agents/KAIROS/schemas/frontmatter.schema.json       --file   08-agents/KAIROS/tests/fixtures/frontmatter/good/example_frontmatter_policy.json
```

## Запуск в GitHub Actions

В CI шаг `Fixture validate (if present)` вызывает:
```bash
python 08-agents/KAIROS/scripts/nr_fm.py       --schema 08-agents/KAIROS/schemas/frontmatter.schema.json       --base   08-agents/KAIROS/tests/fixtures/frontmatter
```

Код выхода 0 = всё ок, любой другой = ошибка.
