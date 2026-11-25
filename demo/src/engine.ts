// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
// Port of the HERD decision rules and metrics (src/herd/rules.py, src/herd/metrics.py,
// src/herd/stats.py mean_interval) to TypeScript, one episode at a time.
// The rules are a line-by-line port and are tested against the Python engine on a
// fixture (engine.test.ts). The random draws are NOT the research engine's: Python uses
// numpy PCG64 streams derived with SeedSequence, the sandbox uses mulberry32 streams, so a
// sandbox seed never reproduces a research episode.

export type Rule = "independent" | "bayesian" | "imitation";
export type TieRule = "own" | "coin";

export interface CellSpec {
  q: number; // P(signal = state), 0.5 <= q < 1
  network: string; // "complete" or "window-k"
  v: number; // P(action publicly visible), 0 <= v <= 1
  n: number; // agents per episode
  tie: TieRule;
}

export interface Episode {
  theta: number;
  signals: number[];
  visible: boolean[];
  coins: number[];
}

export interface RuleOut {
  actions: number[];
  cascade: boolean[];
}

export const TIE = -1;
export const TIE_TOL = 1e-9;
export const NEAR_TIE_BAND = 1e-6;
export const Z95 = 1.959963984540054;

export class EngineError extends Error {}

export function windowOf(network: string): number | null {
  if (network === "complete") return null;
  const m = /^window-([1-9][0-9]*)$/.exec(network);
  if (!m) throw new EngineError(`unknown network ${network}`);
  const k = Number(m[1]);
  if (k > 16) throw new EngineError("window recursion limited to k <= 16");
  return k;
}

export function checkCell(c: CellSpec): void {
  if (!(Number.isFinite(c.q) && c.q >= 0.5 && c.q < 1)) throw new EngineError("q must satisfy 0.5 <= q < 1");
  if (!(Number.isFinite(c.v) && c.v >= 0 && c.v <= 1)) throw new EngineError("v must satisfy 0 <= v <= 1");
  if (!(Number.isInteger(c.n) && c.n >= 1)) throw new EngineError("n must be an integer >= 1");
  if (c.tie !== "own" && c.tie !== "coin") throw new EngineError("tie rule must be own or coin");
  windowOf(c.network);
}

/** Decision code for posterior weights a = P(s|1)L1 and b = P(s|0)L0 (rules.compare). */
export function compare(a: number, b: number): number {
  const scale = Math.max(a, b);
  const gap = Math.abs(a - b);
  if (gap <= TIE_TOL * scale) return TIE;
  return a > b ? 1 : 0;
}

function resolve(code: number, s: number, coin: number, tie: TieRule): number {
  return code === TIE ? (tie === "own" ? s : coin) : code;
}

function probActionOne(code: number, s: number, tie: TieRule): number {
  return code === 1 ? 1 : code === 0 ? 0 : tie === "own" ? s : 0.5;
}

function isCascade(code0: number, code1: number): boolean {
  return code0 === code1 && code0 !== TIE;
}

export function independent(ep: Episode): RuleOut {
  return { actions: ep.signals.slice(), cascade: ep.signals.map(() => false) };
}

export function imitation(ep: Episode, c: CellSpec): RuleOut {
  const n = ep.signals.length;
  const k = windowOf(c.network);
  const actions: number[] = new Array(n);
  const cascade: boolean[] = new Array(n);
  const contrib: number[] = new Array(n).fill(0);
  const code = (x: number) => (x === 0 ? TIE : x > 0 ? 1 : 0);
  for (let i = 0; i < n; i++) {
    const lo = k === null ? 0 : Math.max(0, i - k);
    let lead = 0;
    for (let j = lo; j < i; j++) lead += contrib[j];
    const code0 = code(lead - 1);
    const code1 = code(lead + 1);
    const s = ep.signals[i];
    const a = resolve(s === 1 ? code1 : code0, s, ep.coins[i], c.tie);
    actions[i] = a;
    cascade[i] = isCascade(code0, code1);
    contrib[i] = ep.visible[i] ? 2 * a - 1 : 0;
  }
  return { actions, cascade };
}

export function bayesianComplete(ep: Episode, c: CellSpec): RuleOut {
  const n = ep.signals.length;
  const q = c.q;
  const p01 = 1.0 - q, p00 = q, p11 = q, p10 = 1.0 - q; // pXY = P(s = X | theta = Y)
  let pub1 = 0.5, pub0 = 0.5;
  const actions: number[] = new Array(n);
  const cascade: boolean[] = new Array(n);
  for (let i = 0; i < n; i++) {
    const code0 = compare(p01 * pub1, p00 * pub0);
    const code1 = compare(p11 * pub1, p10 * pub0);
    const s = ep.signals[i];
    const a = resolve(s === 1 ? code1 : code0, s, ep.coins[i], c.tie);
    actions[i] = a;
    cascade[i] = isCascade(code0, code1);
    const pa0 = probActionOne(code0, 0, c.tie), pa1 = probActionOne(code1, 1, c.tie);
    const p1t1 = p01 * pa0 + p11 * pa1;
    const p1t0 = p00 * pa0 + p10 * pa1;
    const like1 = a === 1 ? p1t1 : 1.0 - p1t1;
    const like0 = a === 1 ? p1t0 : 1.0 - p1t0;
    const new1 = ep.visible[i] ? pub1 * like1 : pub1;
    const new0 = ep.visible[i] ? pub0 * like0 : pub0;
    const total = new1 + new0;
    if (!(total > 0)) throw new EngineError("public belief collapsed to zero mass");
    pub1 = new1 / total;
    pub0 = new0 / total;
  }
  return { actions, cascade };
}

/** Forward recursion over the joint law of the last k actions given theta (rules.bayesian_window).
 * State x: bit j is the action at position i - k + j (bit 0 the oldest); padding is hidden zeros. */
export function bayesianWindow(ep: Episode, c: CellSpec, k: number): RuleOut {
  const n = ep.signals.length;
  const q = c.q;
  const p01 = 1.0 - q, p00 = q, p11 = q, p10 = 1.0 - q;
  const size = 1 << k;
  let joint = [new Float64Array(size), new Float64Array(size)];
  joint[0][0] = 1.0;
  joint[1][0] = 1.0;
  const visPad = [...new Array(k).fill(false), ...ep.visible];
  const actPad: number[] = new Array(n + k).fill(0);
  const actions: number[] = new Array(n);
  const cascade: boolean[] = new Array(n);
  const code0 = new Int8Array(size), code1 = new Int8Array(size);
  for (let i = 0; i < n; i++) {
    const marg = [Float64Array.from(joint[0]), Float64Array.from(joint[1])];
    for (let j = 0; j < k; j++) {
      if (visPad[i + j]) continue;
      const bit = 1 << j;
      for (const m of marg) {
        for (let x = 0; x < size; x++) {
          if (x & bit) continue;
          const sum = m[x] + m[x | bit];
          m[x] = sum;
          m[x | bit] = sum;
        }
      }
    }
    for (let x = 0; x < size; x++) {
      const l1 = marg[1][x], l0 = marg[0][x];
      code0[x] = compare(p01 * l1, p00 * l0);
      code1[x] = compare(p11 * l1, p10 * l0);
    }
    let x = 0;
    for (let j = 0; j < k; j++) x |= actPad[i + j] << j;
    const c0 = code0[x], c1 = code1[x];
    const s = ep.signals[i];
    const a = resolve(s === 1 ? c1 : c0, s, ep.coins[i], c.tie);
    actions[i] = a;
    cascade[i] = isCascade(c0, c1);
    actPad[i + k] = a;
    const half = size >> 1;
    const next = [new Float64Array(size), new Float64Array(size)];
    for (let t = 0; t < 2; t++) {
      const p1 = (y: number) => {
        const pa0 = probActionOne(code0[y], 0, c.tie), pa1 = probActionOne(code1[y], 1, c.tie);
        return t === 0 ? p00 * pa0 + p10 * pa1 : p01 * pa0 + p11 * pa1;
      };
      for (let m = 0; m < half; m++) {
        const xa = 2 * m, xb = 2 * m + 1;
        const pa = p1(xa), pb = p1(xb);
        next[t][m] = joint[t][xa] * (1.0 - pa) + joint[t][xb] * (1.0 - pb);
        next[t][m + half] = joint[t][xa] * pa + joint[t][xb] * pb;
      }
    }
    joint = next;
  }
  return { actions, cascade };
}

export function runRule(rule: Rule, ep: Episode, c: CellSpec): RuleOut {
  if (rule === "independent") return independent(ep);
  if (rule === "imitation") return imitation(ep, c);
  const k = windowOf(c.network);
  return k === null ? bayesianComplete(ep, c) : bayesianWindow(ep, c, k);
}

export interface EpisodeMetrics {
  accuracy: number;
  cascade_any: number;
  wrong_cascade_any: number;
  longest_wrong_run: number;
  informative_share: number;
  action_entropy_bits: number;
  last_agent_accuracy: number;
}

export function episodeMetrics(theta: number, out: RuleOut): EpisodeMetrics {
  const n = out.actions.length;
  let correct = 0, casc = 0, run = 0, best = 0, ones = 0;
  let anyCasc = false, wrongCasc = false;
  for (let i = 0; i < n; i++) {
    const ok = out.actions[i] === theta;
    if (ok) correct++;
    if (out.actions[i] === 1) ones++;
    if (out.cascade[i]) {
      casc++;
      anyCasc = true;
      if (!ok) wrongCasc = true;
    }
    run = ok ? 0 : run + 1;
    if (run > best) best = run;
  }
  const p = ones / n;
  const h = p === 0 || p === 1 ? 0 : -(p * Math.log2(p) + (1 - p) * Math.log2(1 - p));
  return {
    accuracy: correct / n,
    cascade_any: anyCasc ? 1 : 0,
    wrong_cascade_any: wrongCasc ? 1 : 0,
    longest_wrong_run: best,
    informative_share: 1.0 - casc / n,
    action_entropy_bits: h,
    last_agent_accuracy: out.actions[n - 1] === theta ? 1 : 0,
  };
}

/** Mean with a normal 95% interval, sample standard deviation (stats.mean_interval). */
export function meanInterval(x: number[]): { mean: number; ci_low: number; ci_high: number } {
  if (x.length < 2) throw new EngineError("need a sample of size >= 2");
  const m = x.reduce((s, v) => s + v, 0) / x.length;
  const ss = x.reduce((s, v) => s + (v - m) * (v - m), 0);
  const se = Math.sqrt(ss / (x.length - 1)) / Math.sqrt(x.length);
  return { mean: m, ci_low: m - Z95 * se, ci_high: m + Z95 * se };
}

/** mulberry32: a small 32-bit generator for the sandbox (not the research engine's PCG64). */
export function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Sandbox episode generator with separate streams for state, signals, visibility and coins,
 * so every rule sees the same draws (common random numbers, as in herd.generate). */
export function makeGenerator(seed: number) {
  const streams = [1, 2, 3, 4].map((s) => mulberry32(Math.imul(seed >>> 0, 0x9e3779b1) ^ Math.imul(s, 0x85ebca6b)));
  const [gTheta, gSig, gVis, gCoin] = streams;
  return (c: CellSpec): Episode => {
    const theta = gTheta() < 0.5 ? 1 : 0;
    const signals: number[] = [], visible: boolean[] = [], coins: number[] = [];
    for (let i = 0; i < c.n; i++) signals.push(gSig() < c.q ? theta : 1 - theta);
    for (let i = 0; i < c.n; i++) visible.push(gVis() < c.v);
    for (let i = 0; i < c.n; i++) coins.push(gCoin() < 0.5 ? 1 : 0);
    return { theta, signals, visible, coins };
  };
}
