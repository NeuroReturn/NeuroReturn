#!/usr/bin/env python3
import sys, re, json, yaml, pathlib
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(".")
SCHEMA_PATH = pathlib.Path("schemas/frontmatter.schema.json")

def extract_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    return yaml.safe_load(m.group(1)) if m else None

def check_one(md_path: pathlib.Path, validator) -> list[str]:
    errs = []
    data = md_path.read_text(encoding="utf-8").replace("\r\n","\n")
    fm = extract_frontmatter(data)
    if not fm:
        errs.append(f"[frontmatter] {md_path}: missing or malformed")
        return errs
    for e in sorted(validator.iter_errors(fm), key=str):
        errs.append(f"[schema] {md_path}: {e.message}")
    return errs

def main():
    if not SCHEMA_PATH.exists():
        print(f"Schema not found: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    targets = [pathlib.Path(p) for p in sys.argv[1:]] or list(ROOT.rglob("**/*.md"))
    errors = []
    for p in targets:
        if p.suffix.lower() != ".md": 
            continue
        try:
            p.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"[encoding] {p}: not UTF-8")
            continue
        errors.extend(check_one(p, validator))

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("frontmatter OK")

if __name__ == "__main__":
    main()
