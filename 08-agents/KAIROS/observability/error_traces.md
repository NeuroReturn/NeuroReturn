# Error Traces — KAIROS
Updated: 2025-09-07T14:19:30Z

Минимум для фиксации ошибки:
- `ts`, `run_id`, `request_id` (если есть)
- `phase_in/out`, `intent`, `mode`
- `exception.type`, `exception.message`
- `ci_tests_run`, `ci_result`
- ссылка на запись в `observability/logs/state_trace.yaml`

Процедура:
1. Зафиксировать запись в state_trace (новая `entries[*]`).
2. Сформировать краткий отчёт (эту страницу), линковать на trace entry.
3. Если severity ≥ fail → эскалация по authority_matrix.
