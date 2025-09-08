# Fallback generation rules
- если термин не найден в curated, создать временную запись в glossary/auto/
- формат см. schemas/glossary.fallback.schema.json
- каждую запись помечать source: "autogen" и confidence <= 0.6
- схема рядом: glossary/glossary.fallback.schema.json (копия для удобства редактирования)
