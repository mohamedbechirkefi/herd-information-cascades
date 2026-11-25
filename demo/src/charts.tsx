// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
// Hand-written SVG charts. Every chart has a plain-language description and a text
// equivalent; uncertainty is drawn on the chart itself, never only in a tooltip.
import type { Contrast } from "./results";

const pct = (x: number, lo: number, hi: number) => `${(((x - lo) / (hi - lo)) * 100).toFixed(3)}%`;

export const RULE_LABEL: Record<string, string> = { independent: "Independent", bayesian: "Bayesian", imitation: "Imitation" };

/** Forest plot of paired contrasts: one row per cell, Bayesian (circle) and imitation (square).
 * Filled marks are Holm-significant / robust; hollow marks are not, at the same size. */
export function ForestPlot({ rows, lo, hi, idPrefix }: { rows: Contrast[]; lo: number; hi: number; idPrefix: string }) {
  const cells = new Map<string, Contrast[]>();
  for (const r of rows) {
    const k = `${r.q}|${r.network}|${r.v}`;
    cells.set(k, [...(cells.get(k) ?? []), r]);
  }
  const ticks = [0, 0.05, 0.1, 0.15].filter((t) => t >= lo && t <= hi);
  const positive = (c: Contrast) => c.status === "robust" || c.status === "Holm-significant";
  return (
    <div className="forest">
      <div className="frow faxis" aria-hidden="true">
        <span className="flabel">Cell</span>
        <div className="ftrack-axis">
          {ticks.map((t) => (
            <span key={t} style={{ left: pct(t, lo, hi) }}>{t === 0 ? "0" : t.toFixed(2)}</span>
          ))}
          <span className="thr" style={{ left: pct(0.01, lo, hi) }}>0.01</span>
        </div>
        <span className="fvals">Estimate [95% interval]</span>
      </div>
      <ul className="forest-rows">
        {[...cells.entries()].map(([k, cs]) => {
          const c0 = cs[0];
          return (
            <li key={k} className="frow" id={`${idPrefix}-${k.replace(/[^0-9a-z]+/gi, "-")}`}>
              <span className="flabel">
                q {c0.q.toFixed(2)} · {c0.network} · v {c0.v}
              </span>
              <svg className="ftrack" aria-hidden="true" height="30" width="100%">
                <line x1={pct(0, lo, hi)} x2={pct(0, lo, hi)} y1="0" y2="30" className="zero" />
                <line x1={pct(0.01, lo, hi)} x2={pct(0.01, lo, hi)} y1="0" y2="30" className="threshold" />
                {cs.map((c) => {
                  const y = c.rule === "bayesian" ? 9 : 21;
                  const cls = `${c.rule} ${positive(c) ? "solid" : "hollow"}`;
                  return (
                    <g key={c.rule} className={cls}>
                      <line x1={pct(c.ci_low, lo, hi)} x2={pct(c.ci_high, lo, hi)} y1={y} y2={y} className="ci" />
                      <svg x={pct(c.estimate, lo, hi)} y={y} overflow="visible">
                        {c.rule === "bayesian" ? <circle r="4.5" cx="0" cy="0" className="mark" /> : <rect x="-4.2" y="-4.2" width="8.4" height="8.4" className="mark" />}
                      </svg>
                    </g>
                  );
                })}
              </svg>
              <span className="fvals">
                {cs.map((c) => (
                  <span key={c.rule} className={`fval ${c.rule}`}>
                    <span className="sym" aria-hidden="true">{c.rule === "bayesian" ? "●" : "■"}</span> {RULE_LABEL[c.rule]} {c.display}{" "}
                    {c.interval_display}
                    {!positive(c) && <strong className="flag"> {c.status}</strong>}
                  </span>
                ))}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

/** Histogram of episode accuracy. counts per bin over [0, 1]; heights are shares of episodes, axis 0 to 1. */
export function Histogram({ counts, total, title, tone }: { counts: number[]; total: number; title: string; tone: string }) {
  const w = 100 / counts.length;
  return (
    <figure className={`hist ${tone}`}>
      <figcaption>{title}</figcaption>
      <div className="hist-frame">
        <span className="hist-y" aria-hidden="true"><span>1</span><span>0.5</span><span>0</span></span>
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="hist-svg" aria-hidden="true">
          <line x1="0" x2="100" y1="50" y2="50" className="grid" />
          {counts.map((c, i) => {
            const h = (c / total) * 100;
            return <rect key={i} x={i * w + 0.4} width={w - 0.8} y={100 - h} height={h} className="bar" />;
          })}
        </svg>
      </div>
      <div className="hist-x" aria-hidden="true"><span>0</span><span>0.5</span><span>1</span></div>
    </figure>
  );
}
