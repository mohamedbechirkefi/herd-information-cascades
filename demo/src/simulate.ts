// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
// Sandbox simulation shared by the Web Worker and the tests: bounded runs of the ported
// HERD rules (engine.ts).
// Work is capped at MAX_EPISODES episodes of at most MAX_AGENTS agents and window k <= 3.
import { type CellSpec, type Rule, checkCell, episodeMetrics, makeGenerator, meanInterval, runRule, windowOf } from "./engine";

export const MAX_EPISODES = 2000;
export const MAX_AGENTS = 100;

export interface SandboxSettings extends CellSpec {
  rule: Exclude<Rule, "independent">;
  episodes: number;
  seed: number;
}

export interface Trace {
  theta: number;
  signals: number[];
  visible: boolean[];
  social: number[];
  cascade: boolean[];
  baseline: number[];
}

export interface SandboxSummary {
  settings: SandboxSettings;
  delta: { mean: number; ci_low: number; ci_high: number };
  wrongCascade: number;
  shareBelow: number;
  socialHist: number[];
  baselineHist: number[];
  trace: Trace;
}

export type WorkerRequest = { type: "run"; settings: SandboxSettings } | { type: "cancel" };
export type WorkerReply =
  | { type: "progress"; fraction: number }
  | { type: "done"; summary: SandboxSummary }
  | { type: "cancelled" }
  | { type: "error"; message: string };

export const BINS = 20;

function bin(acc: number): number {
  return Math.min(BINS - 1, Math.floor(acc * BINS + 1e-9));
}

export async function simulate(s: SandboxSettings, onProgress?: (f: number) => void, isCancelled = () => false): Promise<SandboxSummary | null> {
  checkCell(s);
  const k = windowOf(s.network);
  if (k !== null && k > 3) throw new Error("the sandbox allows windows of at most 3 predecessors");
  if (!(Number.isInteger(s.episodes) && s.episodes >= 2 && s.episodes <= MAX_EPISODES)) throw new Error(`episodes must be 2 to ${MAX_EPISODES}`);
  if (s.n > MAX_AGENTS) throw new Error(`at most ${MAX_AGENTS} agents`);
  if (!(Number.isInteger(s.seed) && s.seed >= 0)) throw new Error("seed must be a non-negative integer");
  const gen = makeGenerator(s.seed);
  const diffs: number[] = [];
  const socialHist = new Array(BINS).fill(0), baselineHist = new Array(BINS).fill(0);
  let wrong = 0, below = 0;
  let trace: Trace | null = null;
  for (let e = 0; e < s.episodes; e++) {
    const ep = gen(s);
    const base = runRule("independent", ep, s);
    const soc = runRule(s.rule, ep, s);
    const mb = episodeMetrics(ep.theta, base), ms = episodeMetrics(ep.theta, soc);
    diffs.push(ms.accuracy - mb.accuracy);
    socialHist[bin(ms.accuracy)]++;
    baselineHist[bin(mb.accuracy)]++;
    wrong += ms.wrong_cascade_any;
    if (ms.accuracy < mb.accuracy) below++;
    if (trace === null) trace = { theta: ep.theta, signals: ep.signals, visible: ep.visible, social: soc.actions, cascade: soc.cascade, baseline: base.actions };
    if (e % 200 === 199) {
      await new Promise((r) => setTimeout(r, 0)); // let a cancel message in
      if (isCancelled()) return null;
      onProgress?.((e + 1) / s.episodes);
    }
  }
  return { settings: s, delta: meanInterval(diffs), wrongCascade: wrong / s.episodes, shareBelow: below / s.episodes, socialHist, baselineHist, trace: trace! };
}

