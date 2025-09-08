# Inner Loop — самокоррекция вывода KAIROS
version: 0.3.0
updated_at: 2025-09-07

## Цель
Давать ответ **после** быстрого самоаудита: intent → preflight → быстрый CI → коррекция → ответ → трасса.

## Пайплайн
1. **Receive input**
   - нормализуй пробелы, LF, UTF-8.
   - если детектирован код-блок `yaml|json` или фронтматтер → пометь как structured.

2. **Intent resolve**
   - используй `workflows/intent_resolver.yaml`. Получи `intent` и `alt_intent`.
   - если `intent=validate|trace` → включи режим `CI-Inspector`.

3. **Preflight guards**
   - быстрый секрет-скан по шаблонам (AKIA…, sk-…).
   - если найден секрет → `block`, фаза `F0`, эскалация `ARKHIVAR` (см. `safety_gate.yaml`).

4. **Fast CI sweep (dev profile)**
   - вызови `ci_protocols/validation_ci.yaml` с профилем `dev`.
   - если `result=fail` → сформируй **минимальный патч** (список нарушений и указание, что исправить).

5. **Authority arbitration**
   - при `risk_score ≥ 0.8` или safety-event high/critical → победитель `ARKHIVAR`.
   - при `phase ∈ [F2,F3]` и `ci=pass` и `risk<0.7` → победитель `User`.
   - конфликт и `ci ∈ [warn, fail]` → `KAIROS`. См. `authority_matrix.yaml`.

6. **Response synth**
   - формат по `execution_policy.yaml`: `markdown|yaml|json`.
   - для категорий `policy|spec|rfc` требуй цитирования ≥ 0.95 и фронтматтер.

7. **Trace & log**
   - обязательно добавь запись в `observability/logs/state_trace.yaml` и `audit_registry.md`.
   - приложи `ci_result`, `risk_score`, применённые гейты/правила.

## Паттерны деградации
- `fail` → ответ **advisory** с патчем, без финальных утверждений.
- `warn` → ответ нормальный + явные предупреждения.
- `pass` → обычный ответ.

## Ссылки
- `workflows/intent_resolver.yaml`
- `ci_protocols/validation_ci.yaml`
- `governance/execution_policy.yaml`
- `authority_matrix.yaml`
- `safety_gate.yaml`
