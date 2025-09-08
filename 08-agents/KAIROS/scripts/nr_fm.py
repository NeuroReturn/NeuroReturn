#!/usr/bin/env python3
import sys, json, os, glob
from jsonschema import Draft202012Validator

def validate_json(validator, path, should_pass=True):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    try:
        validator.validate(data)
        ok = True
        err = None
    except Exception as e:
        ok = False
        err = e
    if should_pass and not ok:
        print(f"FAIL (expected pass): {path}\n{err}")
        return 1
    if not should_pass and ok:
        print(f"FAIL (expected fail): {path}")
        return 1
    print(f"OK: {path}")
    return 0

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "tests/fixtures/frontmatter"
    schema_path = "schemas/frontmatter.schema.json"
    if not os.path.exists(schema_path):
        print(f"SKIP: schema not found at {schema_path}")
        return 0
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)

    rc = 0
    for p in sorted(glob.glob(os.path.join(base, "good", "*.json"))):
        rc |= validate_json(validator, p, True)
    for p in sorted(glob.glob(os.path.join(base, "bad", "*.json"))):
        rc |= validate_json(validator, p, False)
    return rc

if __name__ == "__main__":
    sys.exit(main())
