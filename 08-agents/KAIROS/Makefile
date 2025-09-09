PYTHON    ?= python3
SCHEMA    ?= schemas/frontmatter.schema.json
FIXTURES  ?= tests/fixtures/frontmatter

.PHONY: help schema.check fm.validate ci-validate

help:
	@echo "Targets:"
	@echo "  schema.check   - проверить корректность JSON Schema"
	@echo "  fm.validate    - прогнать все фикстуры (good/bad) против схемы"
	@echo "  ci-validate    - полный прогон для CI (schema.check + fm.validate)"

schema.check:
	$(PYTHON) scripts/json_schema_check.py $(SCHEMA)

fm.validate:
	$(PYTHON) scripts/nr_fm.py --schema $(SCHEMA) --base $(FIXTURES)

ci-validate: schema.check fm.validate
	@echo "[OK] CI validate passed"
