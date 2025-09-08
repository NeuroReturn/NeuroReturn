# Makefile — KAIROS (локальные команды инженера)
# Запускать из каталога 08-agents/KAIROS
# Требуется: python3

PY ?= python3

.DEFAULT_GOAL := help

help:
	@echo "KAIROS Make targets"
	@echo "  make fm-validate         # Проверить примеры фронтматтера тестами"
	@echo "  make schema-check        # Проверить корректность схемы фронтматтера"
	@echo "  make ci-validate         # Мини-оркестрация локальной CI-проверки (stub)"
	@echo "  make pre-commit-install  # Установить git-hook pre-commit"
	@echo "  make pre-commit-run      # Запустить все хуки на всём дереве"
	@echo "  make audit-add MSG='...' # Добавить запись в журнал аудита"

fm-validate:
	$(PY) scripts/nr_fm.py tests/fixtures/frontmatter

schema-check:
	$(PY) scripts/json_schema_check.py schemas/frontmatter.schema.json

# Простая связка базовых проверок. Расширим, когда появятся реальные пайплайны.
ci-validate: schema-check fm-validate
	@echo "[ci-validate] OK"

pre-commit-install:
	@pre-commit install || (echo 'Установи pre-commit: pip install pre-commit' && false)

pre-commit-run:
	@pre-commit run --all-files || (echo 'Смотри замечания выше' && false)

# Упрощённая запись в аудит (UTC)
audit-add:
	@[ -n "$(MSG)" ] || (echo 'Укажи сообщение: make audit-add MSG="..."' && false)
	@python3 - <<'PY'
import datetime, pathlib, os
log = pathlib.Path('observability/logs/audit_registry.md')
ts = datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z'
msg = os.environ.get('MSG')
line = f"{ts} | manual_audit | {msg} | info | KAIROS | F1 | pass | ref: governance/changes/\n"
log.parent.mkdir(parents=True, exist_ok=True)
with log.open('a', encoding='utf-8') as f:
    f.write(line)
print('[audit-add]', line.strip())
PY
