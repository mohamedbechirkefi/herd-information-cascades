# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Evidence audit (master prompt 11.5): trace every number of the manuscript to a committed artifact.

Three checks, all read-only:

1. Trace. Each row of research/publication/number_trace.csv names a printed token and a selector into a
   committed artifact. The selector is evaluated, rounded to the token's printed precision and compared.
2. Coverage. Every decimal number in the manuscript prose (outside generated tables, headings, code
   spans, hashes, dates, versions and identifiers) must have a trace row for that document.
3. Tables. Generated manuscript tables must match the result files (herd.paper check), and every
   line of the tables that herd.tables prints must appear verbatim in the experiment reports.

A row's relation is empty (equal at printed precision), 'lt' (strictly below the token) or 'le' (at most).

Selectors (fields separated by '|'):
  contrast|<run dir>|<filters>|<field>[|min|max|count]   rows of result.json "contrasts" (cell keys flattened)
  arm|<run dir>|<filters>|<metric>.<stat>[|agg]           rows of result.json "arms"
  check|<run dir>|<filters>|<field>[|agg]                 rows of result.json "checks"
  csv|<path>|<filters>|<column>[|agg]                     rows of a CSV file
  json|<path>|<dotted.key.path>                           one value of a JSON file
  const|<value>|<frozen source>                           a design parameter, not a result
  expr|<python expression over {selector} terms>          arithmetic on other selectors
Filters: '*' for all rows, or comma-separated key=value, key!=value, key<value, key>value (numbers
  compared numerically) or ?<python expression over the row's columns>. A field may be =<expression>.

  python -m herd.audit
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from .provenance import REPO_ROOT

TRACE = "research/publication/number_trace.csv"
COVERED = ["research/paper/manuscript.md"]
REPORT_TABLES = {
    "research/experiments/EXP-002/report.md": [("contrasts", "results/EXP-002/EXP-002-R001"), ("secondary", "results/EXP-002/EXP-002-R001")],
    "research/experiments/EXP-003/report.md": [("contrasts", "results/EXP-003/EXP-003-R001"), ("secondary", "results/EXP-003/EXP-003-R001"),
                                               ("robustness", "results/EXP-003/EXP-003-R001/tables/robustness_vs_EXP-002-R001.csv")],
}

NUM = re.compile(r"(?<![\w.])-?\d+\.\d+(?:\s*\\times\s*10\^\{-?\d+\})?(?![\w])(?!\.\d)")
SKIP = [re.compile(p) for p in (r"`[^`]*`", r"\b[0-9a-f]{7,64}\b", r"\d+\.\d+\.\d+", r"\d{4}-\d{2}-\d{2}(T[\d:]+Z)?",
                                  r"EXP-\d{3}(-R\d{3})?", r"\bv\d+\.\d+", r"https?://\S+", r"\b\d+\(\d+\)",
                                  r"[Ss]ections? \d+(\.\d+)?(,? (and|to) \d+(\.\d+)?)?", r"\d+\.\d+ and \d+\.\d+\)",
                                  r"<!--.*?-->")]
_cache: dict = {}


def _load(path: str):
    if path not in _cache:
        p = REPO_ROOT / path
        if p.suffix == ".csv":
            with open(p, newline="", encoding="utf-8") as fh:
                _cache[path] = list(csv.DictReader(fh))
        else:
            _cache[path] = json.loads(p.read_text(encoding="utf-8"))
    return _cache[path]


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return x


def _env(row: dict) -> dict:
    return {k: _num(v) for k, v in row.items() if isinstance(k, str) and k.isidentifier()}


_SAFE = {"__builtins__": {}, "abs": abs, "float": float, "min": min, "max": max, "all": all, "any": any}


def _filter(rows: list[dict], spec: str) -> list[dict]:
    """'*' or comma-separated conditions: key=value, key!=value, key<value, key>value, or ?python-expr."""
    if spec.strip() == "*":
        return rows
    out = []
    for r in rows:
        ok = True
        for cond in spec.split(","):
            if cond.startswith("?"):
                ok = bool(eval(cond[1:], _SAFE, _env(r)))
            else:
                k, op, v = re.fullmatch(r"(\w+)(!=|<|>|=)(.*)", cond).groups()
                a, b = _num(r.get(k)), _num(v)
                if op == "=":
                    ok = a == b if isinstance(b, float) else str(r.get(k)) == v
                elif op == "!=":
                    ok = a != b if isinstance(b, float) else str(r.get(k)) != v
                else:
                    ok = a is not None and (a < b if op == "<" else a > b)
            if not ok:
                break
        if ok:
            out.append(r)
    return out


def _get(row: dict, field: str):
    if field.startswith("="):
        return eval(field[1:], _SAFE, _env(row))
    cur = row
    for part in field.split("."):
        cur = cur[part]
    return cur


def _agg(vals: list, agg: str | None):
    if agg is None:
        if len(vals) != 1:
            raise ValueError(f"selector matched {len(vals)} rows, expected exactly 1")
        return vals[0]
    if agg == "count":
        return float(len(vals))
    if agg in ("min", "max"):
        return (min if agg == "min" else max)(float(v) for v in vals)
    raise ValueError(f"unknown aggregate {agg}")


def _flat(row: dict) -> dict:
    return {**row, **row.get("cell", {})}


def resolve(sel: str) -> float:
    parts = sel.split("|")
    kind = parts[0]
    if kind == "expr":
        expr = re.sub(r"\{([^{}]+)\}", lambda m: repr(resolve(m.group(1))), sel[len("expr|"):])
        return float(eval(expr, {"__builtins__": {}}, {"abs": abs, "max": max, "min": min}))
    if kind == "const":
        return float(parts[1])
    if kind == "json":
        return float(_get(_load(parts[1]), parts[2]))
    agg = parts[4] if len(parts) > 4 else None
    if kind in ("contrast", "arm", "check"):
        res = _load(f"{parts[1]}/result.json")
        rows = [_flat(r) for r in res[{"contrast": "contrasts", "arm": "arms", "check": "checks"}[kind]]]
    elif kind == "csv":
        rows = _load(parts[1])
    else:
        raise ValueError(f"unknown selector kind {kind}")
    rows = _filter(rows, parts[2])
    if agg == "count":
        return float(len(rows))
    return float(_agg([_get(r, parts[3]) for r in rows], agg))


def token_value(tok: str) -> tuple[float, float]:
    tok = tok.replace(" ", "")
    m = re.fullmatch(r"(-?\d+(?:\.(\d+))?)(?:\\times10\^\{(-?\d+)\})?", tok)
    if m is None:
        raise ValueError(f"unparsable token {tok}")
    exp = int(m.group(3) or 0)
    dec = len(m.group(2) or "")
    return float(m.group(1)) * 10 ** exp, 0.5 * 10 ** (exp - dec) * (1 + 1e-9)


def check_trace() -> tuple[list[dict], list[dict]]:
    with open(REPO_ROOT / TRACE, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    bad = []
    for r in rows:
        try:
            value = resolve(r["selector"])
            target, tol = token_value(r["token"])
            if r.get("relation", "") == "lt":
                ok = value < target
            elif r.get("relation", "") == "le":
                ok = value <= target + tol
            else:
                ok = abs(value - target) <= tol
            r["resolved"] = value
            if not ok:
                bad.append({**r, "problem": f"resolved {value!r}"})
        except Exception as exc:  # report every failure, never stop at the first
            bad.append({**r, "problem": f"{type(exc).__name__}: {exc}"})
    return rows, bad


def prose_tokens(doc: str) -> list[tuple[int, str]]:
    text = (REPO_ROOT / doc).read_text(encoding="utf-8")
    text = re.sub(r"<!-- BEGIN GENERATED.*?<!-- END GENERATED [^>]*-->",
                  lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    out = []
    for ln, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        masked = line
        for s in SKIP:
            masked = s.sub(lambda m: " " * len(m.group(0)), masked)
        out += [(ln, m.group(0).replace(" ", "")) for m in NUM.finditer(masked)]
    return out


def check_coverage(trace: list[dict]) -> list[dict]:
    missing = []
    for doc in COVERED:
        have = {r["token"].replace(" ", "") for r in trace if r["doc"] == doc}
        for ln, tok in prose_tokens(doc):
            if tok not in have:
                missing.append({"doc": doc, "line": ln, "token": tok})
    return missing


def check_report_tables() -> list[str]:
    from .serialize import read_result
    from .tables import contrasts_table, robustness_table, secondary_table

    problems = []
    for doc, specs in REPORT_TABLES.items():
        text = (REPO_ROOT / doc).read_text(encoding="utf-8")
        lines = set(text.splitlines())
        for kind, src in specs:
            if kind == "robustness":
                table = robustness_table(REPO_ROOT / src)
            else:
                res = read_result(REPO_ROOT / src / "result.json")
                table = contrasts_table(res) if kind == "contrasts" else secondary_table(res)
            missing = [ln for ln in table.splitlines()[2:] if ln not in lines]
            if missing:
                problems.append(f"{doc}: {len(missing)} of {len(table.splitlines()) - 2} {kind} rows not found verbatim")
    return problems


def main(argv: list[str] | None = None) -> int:
    argparse.ArgumentParser(prog="herd.audit").parse_args(argv)
    from .paper import main as paper_main

    trace, bad = check_trace()
    print(f"trace: {len(trace)} rows, {len(trace) - len(bad)} verified, {len(bad)} failed")
    for b in bad:
        print(f"  FAILED {b['id']} token {b['token']}: {b['problem']}")
    missing = check_coverage(trace)
    print(f"coverage: {len(missing)} manuscript prose numbers without a trace row")
    for m in missing:
        print(f"  MISSING {m['doc']}:{m['line']} {m['token']}")
    tables = check_report_tables()
    print("report tables: " + ("; ".join(tables) if tables else "all generated rows present verbatim"))
    stale = paper_main(["check"])
    return 1 if (bad or missing or tables or stale) else 0


if __name__ == "__main__":
    sys.exit(main())
