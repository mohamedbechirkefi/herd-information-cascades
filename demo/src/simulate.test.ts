// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
import { describe, expect, it } from "vitest";
import { MAX_EPISODES, type SandboxSettings, simulate } from "./simulate";

const base: SandboxSettings = { rule: "bayesian", q: 0.55, network: "complete", v: 1, n: 20, tie: "own", episodes: 400, seed: 3 };

describe("sandbox simulation", () => {
  it("is deterministic in the seed and bounded in its outputs", async () => {
    const a = await simulate(base);
    const b = await simulate(base);
    expect(a).toEqual(b);
    expect(a!.socialHist.reduce((x, y) => x + y, 0)).toBe(400);
    expect(a!.delta.ci_low).toBeLessThanOrEqual(a!.delta.mean);
    expect(a!.delta.mean).toBeLessThanOrEqual(a!.delta.ci_high);
    expect(a!.wrongCascade).toBeGreaterThanOrEqual(0);
    expect(a!.shareBelow).toBeLessThanOrEqual(1);
  });
  it("gives zero difference when nothing is visible", async () => {
    const r = await simulate({ ...base, v: 0, rule: "imitation" });
    expect(r!.delta.mean).toBe(0);
  });
  it("can be cancelled", async () => {
    const r = await simulate({ ...base, episodes: MAX_EPISODES }, undefined, () => true);
    expect(r).toBeNull();
  });
  it("rejects runs beyond the bounds", async () => {
    await expect(simulate({ ...base, episodes: MAX_EPISODES + 1 })).rejects.toThrow();
    await expect(simulate({ ...base, n: 101 })).rejects.toThrow();
    await expect(simulate({ ...base, network: "window-4" })).rejects.toThrow();
    await expect(simulate({ ...base, q: 1 })).rejects.toThrow();
    await expect(simulate({ ...base, seed: -1 })).rejects.toThrow();
  });
});
