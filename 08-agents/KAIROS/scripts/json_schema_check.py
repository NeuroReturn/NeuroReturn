#!/usr/bin/env python3
import sys, json
from jsonschema import Draft202012Validator

def main():
    if len(sys.argv) < 2:
        print("Usage: json_schema_check.py <schema.json>")
        sys.exit(2)
    schema_path = sys.argv[1]
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    Draft202012Validator.check_schema(schema)
    print(f"SCHEMA OK: {schema_path}")

if __name__ == "__main__":
    main()
