// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
// Published results: loaded from public/data/results.json, which
// scripts/export_demo_data.py writes from committed results only.
// Validation fails closed: any missing or malformed field means no numbers are shown.

export const SCHEMA = "lab-demo-results";
export const SCHEMA_MAJOR = 1;

export interface Estimate {
  label: string;
  estimate: number;
  ci_low: number | null;
  ci_high: number | null;
  ci_level: number | null;
  unit: string;
  /** Exact text the manuscript prints for the estimate and interval; shown verbatim when present. */
  display: string | null;
  interval_display: string | null;
}

export interface Experiment {
  id: string;
  title: string;
  status: string;
  verdict: string;
  estimates: Estimate[];
  claim_ids: string[];
  report_path: string;
  notes: string[];
}

export interface Assumption {
  name: string;
  value: string;
  source: string;
}

export interface Source {
  path: string;
  sha256: string;
}

export interface Results {
  schema: string;
  schema_version: string;
  project: string;
  question: string;
  status_label: string;
  code_revision: string;
  sources: Source[];
  experiments: Experiment[];
  assumptions: Assumption[];
  limitations: string[];
  // HERD extensions (validated below, failing closed like the template fields).
  title: string;
  run_revisions: RunRevision[];
  contrast_map: Contrast[];
  cells: Cell[];
}

export interface RunRevision {
  run_id: string;
  exp_id: string;
  label: string;
  code_revision: string;
  result_path: string;
}

/** One paired accuracy contrast (social rule minus the independent baseline). */
export interface Contrast {
  run_id: string;
  exp_id: string;
  label: "confirmatory" | "exploratory";
  variation: string;
  variation_label: string;
  rule: "bayesian" | "imitation";
  q: number;
  network: string;
  v: number;
  n_agents: number;
  tie_rule: string;
  estimate: number;
  ci_low: number;
  ci_high: number;
  display: string;
  interval_display: string;
  holm_significant: boolean;
  status: string;
}

export interface Arm {
  rule: "independent" | "bayesian" | "imitation";
  n_episodes: number;
  edges: number[];
  counts: number[];
  accuracy: Estimate;
  wrong_cascade: Estimate;
  longest_wrong_run: Estimate;
  share_below_baseline: Estimate | null;
}

/** One EXP-002 cell with the episode-accuracy distribution of each rule. */
export interface Cell {
  q: number;
  network: string;
  v: number;
  n_agents: number;
  arms: Arm[];
}

export class ResultsError extends Error {}

type Obj = Record<string, unknown>;

function obj(v: unknown, where: string): Obj {
  if (typeof v !== "object" || v === null || Array.isArray(v)) {
    throw new ResultsError(`${where}: expected an object`);
  }
  return v as Obj;
}

function str(o: Obj, k: string, where: string): string {
  const v = o[k];
  if (typeof v !== "string" || v.length === 0) {
    throw new ResultsError(`${where}.${k}: expected a non-empty string`);
  }
  return v;
}

function num(o: Obj, k: string, where: string, nullable = false): number | null {
  const v = o[k];
  if (nullable && v === null) return null;
  if (typeof v !== "number" || !Number.isFinite(v)) {
    throw new ResultsError(`${where}.${k}: expected a finite number`);
  }
  return v;
}

function arr(o: Obj, k: string, where: string): unknown[] {
  const v = o[k];
  if (!Array.isArray(v)) throw new ResultsError(`${where}.${k}: expected an array`);
  return v;
}

function strArr(o: Obj, k: string, where: string): string[] {
  return arr(o, k, where).map((v, i) => {
    if (typeof v !== "string") throw new ResultsError(`${where}.${k}[${i}]: expected a string`);
    return v;
  });
}

function estimate(v: unknown, where: string): Estimate {
  const o = obj(v, where);
  const e: Estimate = {
    label: str(o, "label", where),
    estimate: num(o, "estimate", where) as number,
    ci_low: num(o, "ci_low", where, true),
    ci_high: num(o, "ci_high", where, true),
    ci_level: num(o, "ci_level", where, true),
    unit: typeof o.unit === "string" ? o.unit : "",
    display: typeof o.display === "string" ? o.display : null,
    interval_display: typeof o.interval_display === "string" ? o.interval_display : null,
  };
  if ((e.ci_low === null) !== (e.ci_high === null)) {
    throw new ResultsError(`${where}: interval must have both bounds or neither`);
  }
  if (e.ci_low !== null && e.ci_high !== null && e.ci_low > e.ci_high) {
    throw new ResultsError(`${where}: ci_low exceeds ci_high`);
  }
  return e;
}

export function validateResults(raw: unknown): Results {
  const o = obj(raw, "results");
  if (o.schema !== SCHEMA) throw new ResultsError(`results.schema: expected "${SCHEMA}"`);
  const version = str(o, "schema_version", "results");
  if (Number(version.split(".")[0]) !== SCHEMA_MAJOR) {
    throw new ResultsError(`results.schema_version: unsupported major version ${version}`);
  }
  const experiments = arr(o, "experiments", "results").map((v, i) => {
    const w = `experiments[${i}]`;
    const e = obj(v, w);
    return {
      id: str(e, "id", w),
      title: str(e, "title", w),
      status: str(e, "status", w),
      verdict: str(e, "verdict", w),
      estimates: arr(e, "estimates", w).map((x, j) => estimate(x, `${w}.estimates[${j}]`)),
      claim_ids: strArr(e, "claim_ids", w),
      report_path: str(e, "report_path", w),
      notes: strArr(e, "notes", w),
    };
  });
  if (experiments.length === 0) throw new ResultsError("results.experiments: empty");
  return {
    schema: SCHEMA,
    schema_version: version,
    project: str(o, "project", "results"),
    question: str(o, "question", "results"),
    status_label: str(o, "status_label", "results"),
    code_revision: str(o, "code_revision", "results"),
    sources: arr(o, "sources", "results").map((v, i) => {
      const s = obj(v, `sources[${i}]`);
      const sha = str(s, "sha256", `sources[${i}]`);
      if (!/^[0-9a-f]{64}$/.test(sha)) throw new ResultsError(`sources[${i}].sha256: not a sha256`);
      return { path: str(s, "path", `sources[${i}]`), sha256: sha };
    }),
    experiments,
    assumptions: arr(o, "assumptions", "results").map((v, i) => {
      const a = obj(v, `assumptions[${i}]`);
      return {
        name: str(a, "name", `assumptions[${i}]`),
        value: str(a, "value", `assumptions[${i}]`),
        source: str(a, "source", `assumptions[${i}]`),
      };
    }),
    limitations: strArr(o, "limitations", "results"),
    ...extensions(o),
  };
}

function bool(o: Obj, k: string, where: string): boolean {
  const v = o[k];
  if (typeof v !== "boolean") throw new ResultsError(`${where}.${k}: expected a boolean`);
  return v;
}

function oneOf<T extends string>(o: Obj, k: string, where: string, allowed: readonly T[]): T {
  const v = str(o, k, where);
  if (!(allowed as readonly string[]).includes(v)) throw new ResultsError(`${where}.${k}: unexpected value ${v}`);
  return v as T;
}

function displayed(e: Estimate, where: string): Estimate {
  if (e.display === null) throw new ResultsError(`${where}: missing display text`);
  if (e.ci_low !== null && e.interval_display === null) throw new ResultsError(`${where}: interval without display text`);
  return e;
}

const NETWORK = /^(complete|window-[1-9][0-9]*)$/;

function contrast(v: unknown, where: string): Contrast {
  const o = obj(v, where);
  const network = str(o, "network", where);
  if (!NETWORK.test(network)) throw new ResultsError(`${where}.network: unknown network`);
  const c: Contrast = {
    run_id: str(o, "run_id", where),
    exp_id: str(o, "exp_id", where),
    label: oneOf(o, "label", where, ["confirmatory", "exploratory"] as const),
    variation: str(o, "variation", where),
    variation_label: str(o, "variation_label", where),
    rule: oneOf(o, "rule", where, ["bayesian", "imitation"] as const),
    q: num(o, "q", where) as number,
    network,
    v: num(o, "v", where) as number,
    n_agents: num(o, "n_agents", where) as number,
    tie_rule: str(o, "tie_rule", where),
    estimate: num(o, "estimate", where) as number,
    ci_low: num(o, "ci_low", where) as number,
    ci_high: num(o, "ci_high", where) as number,
    display: str(o, "display", where),
    interval_display: str(o, "interval_display", where),
    holm_significant: bool(o, "holm_significant", where),
    status: str(o, "status", where),
  };
  if (c.ci_low > c.ci_high) throw new ResultsError(`${where}: ci_low exceeds ci_high`);
  if (c.estimate < c.ci_low || c.estimate > c.ci_high) throw new ResultsError(`${where}: estimate outside its interval`);
  return c;
}

function arm(v: unknown, where: string): Arm {
  const o = obj(v, where);
  const edges = arr(o, "edges", where).map((x, i) => num({ x }, "x", `${where}.edges[${i}]`) as number);
  const counts = arr(o, "counts", where).map((x, i) => {
    const n = num({ x }, "x", `${where}.counts[${i}]`) as number;
    if (!Number.isInteger(n) || n < 0) throw new ResultsError(`${where}.counts[${i}]: expected a count`);
    return n;
  });
  const n_episodes = num(o, "n_episodes", where) as number;
  if (edges.length !== counts.length + 1 || counts.length === 0) throw new ResultsError(`${where}: edges and counts do not match`);
  for (let i = 1; i < edges.length; i++) if (!(edges[i] > edges[i - 1])) throw new ResultsError(`${where}.edges: not increasing`);
  if (counts.reduce((a, b) => a + b, 0) !== n_episodes) throw new ResultsError(`${where}: counts do not sum to n_episodes`);
  const rule = oneOf(o, "rule", where, ["independent", "bayesian", "imitation"] as const);
  const sb = o.share_below_baseline;
  if ((rule === "independent") !== (sb === null)) throw new ResultsError(`${where}.share_below_baseline: expected only for social rules`);
  return {
    rule,
    n_episodes,
    edges,
    counts,
    accuracy: displayed(estimate(o.accuracy, `${where}.accuracy`), `${where}.accuracy`),
    wrong_cascade: displayed(estimate(o.wrong_cascade, `${where}.wrong_cascade`), `${where}.wrong_cascade`),
    longest_wrong_run: displayed(estimate(o.longest_wrong_run, `${where}.longest_wrong_run`), `${where}.longest_wrong_run`),
    share_below_baseline: sb === null ? null : displayed(estimate(sb, `${where}.share_below_baseline`), `${where}.share_below_baseline`),
  };
}

function cell(v: unknown, where: string): Cell {
  const o = obj(v, where);
  const arms = arr(o, "arms", where).map((x, i) => arm(x, `${where}.arms[${i}]`));
  const rules = arms.map((a) => a.rule).join(",");
  if (rules !== "independent,bayesian,imitation") throw new ResultsError(`${where}.arms: expected independent, bayesian, imitation`);
  const network = str(o, "network", where);
  if (!NETWORK.test(network)) throw new ResultsError(`${where}.network: unknown network`);
  return { q: num(o, "q", where) as number, network, v: num(o, "v", where) as number, n_agents: num(o, "n_agents", where) as number, arms };
}

function extensions(o: Obj) {
  const run_revisions = arr(o, "run_revisions", "results").map((v, i) => {
    const w = `run_revisions[${i}]`;
    const r = obj(v, w);
    const rev = str(r, "code_revision", w);
    if (!/^[0-9a-f]{40}$/.test(rev)) throw new ResultsError(`${w}.code_revision: not a git revision`);
    return { run_id: str(r, "run_id", w), exp_id: str(r, "exp_id", w), label: str(r, "label", w), code_revision: rev, result_path: str(r, "result_path", w) };
  });
  const contrast_map = arr(o, "contrast_map", "results").map((v, i) => contrast(v, `contrast_map[${i}]`));
  const cells = arr(o, "cells", "results").map((v, i) => cell(v, `cells[${i}]`));
  if (contrast_map.length === 0) throw new ResultsError("results.contrast_map: empty");
  if (cells.length === 0) throw new ResultsError("results.cells: empty");
  if (run_revisions.length === 0) throw new ResultsError("results.run_revisions: empty");
  return { title: str(o, "title", "results"), run_revisions, contrast_map, cells };
}

export async function loadResults(url = "./data/results.json"): Promise<Results> {
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new ResultsError(`could not load ${url} (HTTP ${res.status})`);
  let raw: unknown;
  try {
    raw = await res.json();
  } catch {
    throw new ResultsError(`${url} is not valid JSON`);
  }
  return validateResults(raw);
}

/** Formats a number for display without inventing precision. */
export function fmt(x: number, digits = 3): string {
  if (Number.isInteger(x)) return x.toString();
  return Number(x.toPrecision(digits)).toString();
}

export function fmtEstimate(e: Estimate, digits = 3): string {
  return e.display ?? `${fmt(e.estimate, digits)}${e.unit ? " " + e.unit : ""}`;
}

export function fmtInterval(e: Estimate, digits = 3): string {
  if (e.interval_display !== null) return e.interval_display;
  if (e.ci_low === null || e.ci_high === null) return "no interval";
  const level = e.ci_level === null ? "" : `${Math.round(e.ci_level * 100)}% `;
  return `${level}[${fmt(e.ci_low, digits)}, ${fmt(e.ci_high, digits)}]`;
}
