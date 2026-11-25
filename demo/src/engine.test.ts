// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
// The TypeScript port against the Python engine (fixture written by
// scripts/export_sandbox_fixture.py from herd.generate, herd.rules, herd.metrics, herd.stats).
// Tolerance: actions and cascade flags must be identical; per-episode metrics and the paired
// contrast (mean and normal 95% interval) must agree within 1e-12 (floating-point summation
// order and log2 may differ in the last bits).
import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { type CellSpec, type Episode, type Rule, EngineError, checkCell, episodeMetrics, makeGenerator, meanInterval, runRule } from "./engine";

const TOL = 1e-12;
const fx = JSON.parse(readFileSync("src/fixtures/engine_fixture.json", "utf8"));
const bits = (s: string) => [...s].map(Number);

describe("engine port matches the Python engine", () => {
  it("covers every network, visibility and tie rule in the fixture", () => {
    expect(fx.cells.length).toBe(48);
  });
  for (const cell of fx.cells) {
    const spec: CellSpec = { q: cell.q, network: cell.network, v: cell.v, n: cell.n_agents, tie: cell.tie_rule };
    it(`q=${cell.q} ${cell.network} v=${cell.v} ${cell.tie_rule}`, () => {
      const acc: Record<string, number[]> = {};
      for (const rule of ["independent", "bayesian", "imitation"] as Rule[]) {
        const exp = cell.rules[rule];
        acc[rule] = [];
        cell.theta.forEach((theta: number, e: number) => {
          const ep: Episode = { theta, signals: bits(cell.signals[e]), visible: bits(cell.visible[e]).map(Boolean), coins: bits(cell.coins[e]) };
          const out = runRule(rule, ep, spec);
          expect(out.actions.join(""), `${rule} actions, episode ${e}`).toBe(exp.actions[e]);
          expect(out.cascade.map(Number).join(""), `${rule} cascade, episode ${e}`).toBe(exp.cascade[e]);
          const m = episodeMetrics(theta, out);
          for (const [k, v] of Object.entries(m)) expect(Math.abs(v - exp.metrics[k][e]), `${rule} ${k}`).toBeLessThanOrEqual(TOL);
          acc[rule].push(m.accuracy);
        });
      }
      for (const rule of ["bayesian", "imitation"]) {
        const d = meanInterval(acc[rule].map((a, i) => a - acc.independent[i]));
        const ref = cell.contrasts[rule];
        expect(Math.abs(d.mean - ref.mean)).toBeLessThanOrEqual(TOL);
        expect(Math.abs(d.ci_low - ref.ci_low)).toBeLessThanOrEqual(TOL);
        expect(Math.abs(d.ci_high - ref.ci_high)).toBeLessThanOrEqual(TOL);
      }
    });
  }
});

describe("engine inputs and sandbox generator", () => {
  it("rejects invalid cells", () => {
    expect(() => checkCell({ q: 1, network: "complete", v: 1, n: 5, tie: "own" })).toThrow(EngineError);
    expect(() => checkCell({ q: 0.6, network: "ring", v: 1, n: 5, tie: "own" })).toThrow(EngineError);
    expect(() => checkCell({ q: 0.6, network: "complete", v: 1.5, n: 5, tie: "own" })).toThrow(EngineError);
    expect(() => checkCell({ q: 0.6, network: "complete", v: 1, n: 0, tie: "own" })).toThrow(EngineError);
  });
  it("is deterministic in the seed", () => {
    const c: CellSpec = { q: 0.7, network: "window-2", v: 0.5, n: 20, tie: "own" };
    const a = makeGenerator(42), b = makeGenerator(42), d = makeGenerator(43);
    const ea = a(c), eb = b(c), ed = d(c);
    expect(ea).toEqual(eb);
    expect(JSON.stringify(ea)).not.toEqual(JSON.stringify(ed));
  });
});
