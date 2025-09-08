#!/usr/bin/env python3
import argparse, json, sys, re, unicodedata, datetime, os
from jsonschema import Draft202012Validator

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "frontmatter.schema.json")

TYPE_TO_CATEGORY = {
    "policy": "policy",
    "spec": "spec",
    "contract": "contract",
    "protocol": "workflow",
    "csv": "data",
    "md": "other",
    "yaml": "other",
    "test": "other",
    "note": "other",
    "template": "other",
}

PHASES = {"F0","F1","F2","F3"}
STATUS = {"draft","review","approved","canon","immutable"}

def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value or "untitled"

def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def validate(instance, schema=None):
    schema = schema or load_schema()
    Draft202012Validator(schema).validate(instance)

def cmd_new(args):
    schema = load_schema()
    title = args.title
    t = args.type
    if t not in TYPE_TO_CATEGORY:
        print(f"[error] unsupported type: {t}", file=sys.stderr)
        sys.exit(2)
    category = TYPE_TO_CATEGORY[t]
    today = datetime.date.today().isoformat()
    slug = slugify(title)
    fid = f"KAIROS_{slug}"
    doc = {
        "id": fid,
        "project": "NeuroReturn",
        "title": title,
        "version": args.version,
        "category": category,
        "type": t,
        "phase": args.phase,
        "status": args.status,
        "confidentiality": args.confidentiality,
        "source": args.source,
        "created_at": today
    }
    # Optional links
    if args.tags: doc["tags"] = args.tags
    validate(doc, schema)
    out = json.dumps(doc, ensure_ascii=False, indent=2)
    if args.output and args.output != "-":
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out + "\n")
        print(args.output)
    else:
        print(out)

def cmd_lint(args):
    schema = load_schema()
    ok = True
    for path in args.paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                inst = json.load(f)
            validate(inst, schema)
            print(f"{path}: PASS")
        except Exception as e:
            ok = False
            print(f"{path}: FAIL -> {e}", file=sys.stderr)
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser(prog="nr_fm", description="NeuroReturn/KAIROS frontmatter tool")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_new = sub.add_parser("new", help="create a new frontmatter JSON")
    ap_new.add_argument("--type", required=True, choices=list(TYPE_TO_CATEGORY.keys()))
    ap_new.add_argument("--title", required=True)
    ap_new.add_argument("--phase", default="F0", choices=list(PHASES))
    ap_new.add_argument("--status", default="draft", choices=list(STATUS))
    ap_new.add_argument("--version", default="0.1.0")
    ap_new.add_argument("--confidentiality", default="internal", choices=["public","internal","restricted","secret"])
    ap_new.add_argument("--source", default="decision", choices=["chat","decision","research","import","legacy"])
    ap_new.add_argument("--tags", nargs="*", default=[])
    ap_new.add_argument("-o", "--output", default="-")
    ap_new.set_defaults(func=cmd_new)

    ap_lint = sub.add_parser("lint", help="validate frontmatter JSON file(s) against schema")
    ap_lint.add_argument("paths", nargs="+")
    ap_lint.set_defaults(func=cmd_lint)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
