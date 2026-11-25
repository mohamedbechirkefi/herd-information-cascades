// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { ResultsError, validateResults } from "./results";

const good = () => JSON.parse(readFileSync("public/data/results.json", "utf8"));

describe("validateResults", () => {
  it("accepts the exported results file", () => {
    expect(validateResults(good()).experiments.length).toBeGreaterThan(0);
  });
  it("rejects a wrong schema name", () => {
    expect(() => validateResults({ ...good(), schema: "other" })).toThrow(ResultsError);
  });
  it("rejects an unsupported major version", () => {
    expect(() => validateResults({ ...good(), schema_version: "2.0.0" })).toThrow(ResultsError);
  });
  it("rejects a missing estimate", () => {
    const r = good();
    delete r.experiments[0].estimates?.[0]?.estimate;
    if (r.experiments[0].estimates.length === 0) r.experiments[0].title = 7;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a non-finite number", () => {
    const r = good();
    r.experiments[0].estimates = [{ label: "x", estimate: "NaN", ci_low: null, ci_high: null, ci_level: null, unit: "" }];
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a half-open interval", () => {
    const r = good();
    r.experiments[0].estimates = [{ label: "x", estimate: 1, ci_low: 0, ci_high: null, ci_level: 0.95, unit: "" }];
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a malformed source hash", () => {
    expect(() => validateResults({ ...good(), sources: [{ path: "a", sha256: "zz" }] })).toThrow(ResultsError);
  });

  it("rejects a missing extension key", () => {
    const r = good();
    delete r.contrast_map;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a contrast whose estimate lies outside its interval", () => {
    const r = good();
    r.contrast_map[0].estimate = r.contrast_map[0].ci_high + 1;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a contrast without display text", () => {
    const r = good();
    delete r.contrast_map[0].interval_display;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a histogram whose counts do not sum to the episodes", () => {
    const r = good();
    r.cells[0].arms[0].counts[0] += 1;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a cell arm estimate without display text", () => {
    const r = good();
    r.cells[0].arms[1].wrong_cascade.display = null;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a malformed run revision", () => {
    const r = good();
    r.run_revisions[0].code_revision = "50fbdb1";
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("labels every contrast as confirmatory or exploratory", () => {
    const r = good();
    r.contrast_map[0].label = "sandbox";
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
});
