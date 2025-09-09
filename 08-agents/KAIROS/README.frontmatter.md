# KAIROS Frontmatter — quick start

Короткая памятка по локальной и CI-валидации фронтматтера (JSON Schema).

## Локальная проверка

1) Установи зависимости:
```bash
pip install -r requirements.txt

## ID naming policy

Разрешённые форматы (`id`):
- `NR_001_Name-Of-Thing`
- `NR-AB-F0-Name-Of-Thing`   (AB — 2 буквы кода; F0..F3 — фаза)
- `KAIROS_Name-Of-Thing`     (**после `KAIROS_` — только [A-Za-z0-9-]**)

Запрещено: второе подчёркивание после префикса (`KAIROS_FM_Policy` ❌).
