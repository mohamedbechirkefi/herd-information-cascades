# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Minimal JSON Schema validator (subset of draft 2020-12) and schema loading.

Supported keywords: type, enum, const, required, properties, additionalProperties,
items, minItems, minimum, maximum, minLength, pattern, $ref (local '#/$defs/...').
Unknown keywords raise, so a schema cannot silently use an unsupported feature.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"
SUPPORTED = {"$schema", "$id", "$defs", "title", "description", "type", "enum", "const", "required",
             "properties", "additionalProperties", "items", "minItems", "minimum", "maximum",
             "minLength", "pattern", "$ref"}
_TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


class SchemaError(ValueError):
    """Raised when a document does not conform to its schema."""


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    if not path.is_file():
        raise SchemaError(f"schema not found: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def errors(instance, schema: dict, root: dict | None = None, path: str = "$") -> list[str]:
    root = schema if root is None else root
    out: list[str] = []
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise SchemaError(f"unsupported schema keywords at {path}: {sorted(unknown)}")
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            raise SchemaError(f"only local $defs references are supported, got {ref}")
        return errors(instance, root["$defs"][ref[len("#/$defs/"):]], root, path)
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_TYPES[t](instance) for t in types):
            return [f"{path}: expected type {types}, got {type(instance).__name__}"]
    if isinstance(instance, float) and instance != instance:
        out.append(f"{path}: NaN is not allowed")
    if "enum" in schema and instance not in schema["enum"]:
        out.append(f"{path}: {instance!r} not in {schema['enum']}")
    if "const" in schema and instance != schema["const"]:
        out.append(f"{path}: expected {schema['const']!r}")
    if _TYPES["number"](instance):
        if "minimum" in schema and instance < schema["minimum"]:
            out.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            out.append(f"{path}: {instance} > maximum {schema['maximum']}")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            out.append(f"{path}: string shorter than {schema['minLength']}")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            out.append(f"{path}: {instance!r} does not match {schema['pattern']}")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                out.append(f"{path}: missing required key {key!r}")
        props = schema.get("properties", {})
        for key, value in instance.items():
            if key in props:
                out.extend(errors(value, props[key], root, f"{path}.{key}"))
            else:
                extra = schema.get("additionalProperties", True)
                if extra is False:
                    out.append(f"{path}: unexpected key {key!r}")
                elif isinstance(extra, dict):
                    out.extend(errors(value, extra, root, f"{path}.{key}"))
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            out.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, item in enumerate(instance):
                out.extend(errors(item, schema["items"], root, f"{path}[{i}]"))
    return out


def validate(instance, schema: dict) -> None:
    errs = errors(instance, schema)
    if errs:
        shown = "; ".join(errs[:10])
        raise SchemaError(f"{len(errs)} schema error(s): {shown}")
