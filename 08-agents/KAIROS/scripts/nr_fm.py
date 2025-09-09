#!/usr/bin/env python3
import argparse, json, sys, os, glob
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
        print(f"[FAIL: expected pass] {path}\n{err}", file=sys.stderr)
        return 1
    if (not should_pass) and ok:
        print(f"[FAIL: expected fail]  {path}", file=sys.stderr)
        return 1
    print(f"[OK] {path}")
    return 0

def main(argv=None):
    p = argparse.ArgumentParser(
        description="Validate KAIROS frontmatter JSON files against JSON Schema."
    )
    p.add_argument("--schema", required=True, help="Path to frontmatter.schema.json")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--base", help="Folder with fixtures containing 'good' and/or 'bad' subfolders")
    g.add_argument("--file", help="Validate a single JSON file (must be valid)")
    args = p.parse_args(argv)

    with open(args.schema, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)

    rc = 0
    if args.file:
        rc |= validate_json(validator, args.file, should_pass=True)
    else:
        good_dir = os.path.join(args.base, "good")
        bad_dir  = os.path.join(args.base, "bad")
        for pth in sorted(glob.glob(os.path.join(good_dir, "*.json"))):
            rc |= validate_json(validator, pth, True)
        for pth in sorted(glob.glob(os.path.join(bad_dir, "*.json"))):
            rc |= validate_json(validator, pth, False)
    return rc

if __name__ == "__main__":
    sys.exit(main())
