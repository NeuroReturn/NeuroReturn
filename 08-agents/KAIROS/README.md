# KAIROS — Паспорт проекта
version: 0.3.0
status: draft
updated_at: 2025-09-08
owner: NeuroReturn™ Engineering
repo_root: 08-agents/KAIROS/

> Назначение: CI-валидируемый агент для фазового восстановления субъектности (NeuroReturn™). Этот документ — точка входа для инженеров. Ноль мотивации, максимум проверяемости.

---

## 1. Контекст и границы (Scope)
- **Цель:** операционализировать протоколы TPMA, SafetyGate и управление фазами F0–F3.
- **Вне границ:** UI, хранение PHI/PII; интеграция с внешними EMR/FHIR — отдельный профиль.
- **Артефакты верхнего уровня:** `contract.core.json`, `contract.full.json`, `ci_runtime_behavior.yaml`.

## 2. Быстрый запуск локальной валидации
```bash
# из корня репозитория
python3 scripts/json_schema_check.py schemas/frontmatter.schema.json
python3 scripts/nr_fm.py tests/fixtures/frontmatter

# пайплайн (локальный оркестр шагов)
# см. pipelines/validation_ci.yaml
```
Минимальный ожидаемый результат: без исключений и с отчётом «OK» по примерам фронтматтера.

## 3. Контракты и политики
| Блок | Файл | Назначение |
|---|---|---|
| Contract (core) | `contract.core.json` | Инварианты и идентичность агента |
| Contract (full) | `contract.full.json` | Сводный реестр путей на политики/схемы/воркфлоу |
| Execution Policy | `governance/execution_policy.yaml` | Правила intent→persona, префлайт-блоки, эскалации |
| Authority Matrix | `authority_matrix.yaml` | Кто выигрывает при конфликте условий |
| Safety Gate | `safety_gate.yaml` | Шлюзы и ограничения по фазам/рискам |

## 4. Пороговые значения и арбитраж
```yaml
thresholds:
  risk_override: 0.7   # ранняя эскалация в F0/F1
  risk_block:    0.8   # абсолютный блок
  score_min_pass: 0.6

authority:
  - when: "risk_score >= thresholds.risk_block"                  -> ARKHIVAR
  - when: "phase in [F0, F1] and risk_score >= thresholds.risk_override" -> ARKHIVAR
  - when: "phase in [F2, F3] and ci_result == pass"              -> User
  - when: "ci_result == fail"                                    -> KAIROS
  - else: consensus
```
Источник: `ci_runtime_behavior.yaml` и `authority_matrix.yaml` (значения синхронизированы).

## 5. Маршрутизация, состояние и активации
- **Routing:** `routing_rules.yaml` (+ `schemas/routing_rules.schema.json`)
- **State machine:** `state_machine.yaml`
- **Activation:** `activation.yaml` (триггеры: dev toggle, nightly CI)

## 6. CI-протоколы
| Протокол | Файл | Проверяет |
|---|---|---|
| Validation CI | `ci_protocols/validation_ci.yaml` | базовые проверки репозитория |
| TPMA Integrity | `ci_protocols/tpma_integrity.yaml` | заголовки/строки TPMA |
| ReturnScore Eval | `ci_protocols/returnscore_eval.yaml` | вклад в ReturnScore |
| Adjust Protocol | `ci_protocols/adjust_protocol.yaml` | корректность Adjust-логики |
| Glossary Match | `ci_protocols/glossary_match.yaml` | покрытие терминов |

## 7. Наблюдаемость (Observability)
- Логи: `observability/logs/*` (`audit_registry.md`, `state_trace.yaml`, `symbol_trace.yaml`, `adjust_layer.yaml`, `audit_sample.json`)
- Графы: `observability/graphs/architecture.puml`
- Метрики/ошибки: `observability/{metrics.md,error_traces.md,decisions.md}`

## 8. Глоссарий
- Автогенерация: `glossary/auto/` по правилам `glossary_autogen_rules.yaml`
- Схемы: `schemas/glossary.fallback.schema.json` (копия в `glossary/` допустима)
- Покрытие и требования: `glossary_match.yaml`

## 9. Управление изменениями (Provenance)
- Патчи: `governance/changes/*.diff`
- Аудит: `observability/logs/audit_registry.md` (каждая запись содержит `ref:` на diff)
- Правила хранения/редакции: `governance/memory_policy.yaml`

## 10. Конформность стандартам (минимальная матрица)
| Требование | Где покрыто |
|---|---|
| ISO/IEC TR 24028 — Trustworthiness (governance, audit, risk) | `governance/*`, `observability/logs/*`, `ci_runtime_behavior.yaml` |
| ACM Agent Contract Spec — контракты/роллинг/арбитраж | `contract.*`, `authority_matrix.yaml`, `execution_policy.yaml` |
| OpenAI DevSpec 2024 — I/O форматы и guardrails | `ci_runtime_behavior.yaml`, `routing_rules.yaml`, схемы |
| FHIR Agent Protocols — профиль данных (будущее) | отдельный профиль; сейчас PHI/PII disabled в `memory_policy.yaml` |

## 11. Ответственность и роли
- Owner: NeuroReturn™ Engineering
- Change Approvers: Owner, Safety, CI
- Контакт: добавить при подключении хостинга/таск-трекера

## 12. Архитектурный план (минимум)
- Ссылка на диаграмму: `observability/graphs/architecture.puml`
- План расширений: FHIR-профиль, eval-наборы, интеграция сторожей секретов.
![KAIROS CI](https://github.com/balkonslando-dotcom/NeuroReturn/actions/workflows/kairos-ci.yml/badge.svg?branch=main)

---

### Checklists
- [ ] Синхронизированы пороги в `ci_runtime_behavior.yaml` и `execution_policy.yaml`
- [ ] `contract.full.json/policies` указывает на актуальные пути
- [ ] Примеры фронтматтера проходят валидацию
- [ ] Аудит содержит запись о каждом изменении с `ref: governance/changes/...`
- [ ] PHI/PII хранение отключено (см. `governance/memory_policy.yaml`)
