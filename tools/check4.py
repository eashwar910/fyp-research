#!/usr/bin/env python3
"""Validate run-4 stage-4 verifier outputs.

Stdlib-only, intentionally small JSON Schema subset plus runbook-specific
cross-field rules.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATE_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")
MAX_BY_KEY = {
    "reason": 600,
    "why": 300,
    "notes": 500,
    "nearest_neighbours_do_not": 400,
}

# These were accepted in the interrupted run and are the Phase-0 acceptance
# fixtures. Keep new files strict while not rewriting another lane's evidence.
LEGACY_BARE_YEAR_DATE_WAIVERS = {
    ("nov", "R4-S01"),
    ("nov", "R4-S23"),
}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def resolve_ref(ref: str, schemas: dict[str, Any]) -> Any:
    file_name, _, pointer = ref.partition("#")
    if not file_name:
        raise ValueError(f"local-only ref unsupported: {ref}")
    target = schemas[file_name]
    if pointer:
        for part in pointer.lstrip("/").split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            target = target[part]
    return target


def type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_schema(value: Any, schema: dict[str, Any], path: str, schemas: dict[str, Any], out: list[str]) -> None:
    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], schemas)

    if "type" in schema:
        expected = schema["type"]
        options = expected if isinstance(expected, list) else [expected]
        if not any(type_ok(value, t) for t in options):
            out.append(f"{path}: expected type {'|'.join(options)}, got {type(value).__name__}")
            return

    if "enum" in schema and value not in schema["enum"]:
        out.append(f"{path}: expected one of {schema['enum']}, got {value!r}")

    if isinstance(value, str):
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            out.append(f"{path}: length {len(value)} exceeds maxLength {schema['maxLength']}")
        if "pattern" in schema and not re.match(schema["pattern"], value):
            out.append(f"{path}: does not match pattern {schema['pattern']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            out.append(f"{path}: has {len(value)} items, needs at least {schema['minItems']}")
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(value):
                validate_schema(item, item_schema, f"{path}[{i}]", schemas, out)

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                out.append(f"{path}: missing required key {key!r}")
        props = schema.get("properties", {})
        for key, item in value.items():
            if key in props:
                validate_schema(item, props[key], f"{path}.{key}", schemas, out)


def walk(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, item in value.items():
            yield f"{path}.{key}", key, item
            yield from walk(item, f"{path}.{key}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield f"{path}[{i}]", "", item
            yield from walk(item, f"{path}[{i}]")


def extra_rules(role: str, cid: str, data: dict[str, Any], out: list[str]) -> None:
    waive_legacy_dates = (role, cid) in LEGACY_BARE_YEAR_DATE_WAIVERS

    for path, key, value in walk(data):
        if key in MAX_BY_KEY and isinstance(value, str) and len(value) > MAX_BY_KEY[key]:
            out.append(f"{path}: length {len(value)} exceeds maxLength {MAX_BY_KEY[key]}")
        if key == "date" and isinstance(value, str) and not DATE_RE.match(value):
            if not (waive_legacy_dates and re.fullmatch(r"\d{4}", value)):
                out.append(f"{path}: date {value!r} must be YYYY-MM or YYYY-MM-DD; bare years are invalid")
        if key == "application_deadline" and isinstance(value, str) and value and not DATE_RE.match(value):
            out.append(f"{path}: date {value!r} must be YYYY-MM or YYYY-MM-DD")

    if role == "nov":
        queries = data.get("queries")
        if not isinstance(queries, list) or len(queries) < 3:
            out.append("$.queries: novelty verdicts need at least 3 queries")
        elif any(not isinstance(q, dict) or "q" not in q or "useful" not in q for q in queries):
            out.append("$.queries: every query item must contain q and useful")

        verdict = data.get("verdict")
        if data.get("product_search") is None:
            out.append("$.product_search: required for every novelty verdict")
        if verdict == "closed" and not data.get("closing_item"):
            out.append("$.closing_item: required when verdict=closed")
        if verdict == "type_b":
            tbf = data.get("type_b_fields")
            needed = {
                "named_prior_solution_url",
                "measurable_axis",
                "attributable_to",
                "prior_deployed_in_target_region",
            }
            if not isinstance(tbf, dict):
                out.append("$.type_b_fields: object required when verdict=type_b")
            else:
                missing = sorted(needed - set(tbf))
                if missing:
                    out.append(f"$.type_b_fields: missing {', '.join(missing)}")
        if verdict == "unclear" and not data.get("human_should_check"):
            out.append("$.human_should_check: required when verdict=unclear")


def main(argv: list[str]) -> int:
    if len(argv) != 2 or ":" not in argv[1]:
        print("1. usage: python3 tools/check4.py <nov|dat>:<id>")
        return 1

    role, cid = argv[1].split(":", 1)
    if role not in {"nov", "dat"}:
        print("1. role must be nov or dat")
        return 1

    schema_name = "novelty_verdict.schema.json" if role == "nov" else "data_verification.schema.json"
    data_path = ROOT / ".research" / ("novelty" if role == "nov" else "data") / f"{cid}.json"
    if not data_path.exists():
        print(f"1. missing file {data_path}")
        return 1

    schemas = {
        schema_name: load_json(ROOT / "schemas" / schema_name),
        "_common.schema.json": load_json(ROOT / "schemas" / "_common.schema.json"),
    }

    violations: list[str] = []
    try:
        data = load_json(data_path)
    except Exception as exc:
        print(f"1. invalid JSON: {exc}")
        return 1

    validate_schema(data, schemas[schema_name], "$", schemas, violations)
    if isinstance(data, dict):
        extra_rules(role, cid, data, violations)
    else:
        violations.append("$: top-level value must be an object")

    if violations:
        for i, msg in enumerate(violations, 1):
            print(f"{i}. {msg}")
        return 1

    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
