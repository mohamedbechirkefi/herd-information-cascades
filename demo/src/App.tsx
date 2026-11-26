// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
import { type ReactNode, useEffect, useMemo, useState } from "react";
import { ForestPlot, Histogram, RULE_LABEL } from "./charts";
import { type Estimate, type Results, ResultsError, fmtEstimate, fmtInterval, loadResults } from "./results";
import { Sandbox } from "./Sandbox";

type State = { kind: "loading" } | { kind: "error"; message: string } | { kind: "ready"; results: Results };

export function App() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    loadResults()
      .then((results) => setState({ kind: "ready", results }))
      .catch((e: unknown) =>
        setState({ kind: "error", message: e instanceof ResultsError ? e.message : "results could not be loaded" }),
      );
  }, []);

  return (
    <>
      <a className="skip" href="#main">Skip to content</a>
      <header className="site">
        <div className="wrap">
          <p className="kicker">HERD · a simulation study of social learning</p>
          <h1>When does watching others help a group decide, and when does it lock the group into an error?</h1>
          <nav aria-label="Sections">
            <a href="#overview">Overview</a>
            <a href="#results">Results</a>
            <a href="#distribution">Distribution</a>
            <a href="#assumptions">Assumptions</a>
            <a href="#method">Method and limitations</a>
            <a href="#sandbox">Sandbox</a>
          </nav>
        </div>
      </header>
      <main id="main" className="wrap">
        {state.kind === "loading" && <p role="status">Loading the published results.</p>}
        {state.kind === "error" && (
          <div role="alert" className="panel error">
            <h2>Results unavailable</h2>
            <p>The published results file failed validation, so no numbers are shown.</p>
            <p><code>{state.message}</code></p>
          </div>
        )}
        {state.kind === "ready" && <Published r={state.results} />}
        <Sandbox />
      </main>
      <footer className="site">
        <div className="wrap">
          <p>
            Mohamed Bechir Kefi, independent researcher. Runs offline after the first load. No data about visitors is
            collected, stored or sent anywhere. Repository:{" "}
            <a href="https://github.com/mohamedbechirkefi/herd-information-cascades">github.com/mohamedbechirkefi/herd-information-cascades</a>. Demo:{" "}
            <a href="https://herd-information-cascades.kefimohamedbechir.workers.dev">herd-information-cascades.kefimohamedbechir.workers.dev</a>.
          </p>
        </div>
      </footer>
    </>
  );
}

function Label({ kind }: { kind: "confirmatory" | "exploratory" | "assumption" }) {
  const text = { confirmatory: "Measured · confirmatory", exploratory: "Measured · exploratory", assumption: "Assumption or design setting" }[kind];
  return <span className={`badge ${kind}`}>{text}</span>;
}

function expKind(status: string): "confirmatory" | "exploratory" {
  return status.startsWith("confirmatory") ? "confirmatory" : "exploratory";
}

const SOURCES = [
  { id: "main", name: "EXP-002, confirmatory (own-signal ties, N = 50)" },
  { id: "EXP-003|V1", name: "EXP-003 V1, confirmatory (coin-flip ties, N = 50)" },
  { id: "EXP-003|V2", name: "EXP-003 V2, confirmatory (own ties, N = 10)" },
  { id: "EXP-003|V3", name: "EXP-003 V3, confirmatory (own ties, N = 200)" },
  { id: "EXP-004|V1", name: "EXP-004 V1, exploratory (coin-flip ties, N = 50)" },
  { id: "EXP-004|V2", name: "EXP-004 V2, exploratory (own ties, N = 10)" },
  { id: "EXP-004|V3", name: "EXP-004 V3, exploratory (own ties, N = 200)" },
];

function Published({ r }: { r: Results }) {
  const [source, setSource] = useState("main");
  const lo = Math.min(-0.02, ...r.contrast_map.map((c) => c.ci_low));
  const hi = Math.max(0.16, ...r.contrast_map.map((c) => c.ci_high));
  const rows = useMemo(
    () => r.contrast_map.filter((c) => (source === "main" ? c.variation === "main" : `${c.exp_id}|${c.variation}` === source)),
    [r, source],
  );
  const main = r.contrast_map.filter((c) => c.variation === "main");
  const smallest = main.reduce((a, b) => (b.estimate < a.estimate ? b : a));
  const largest = main.reduce((a, b) => (b.estimate > a.estimate ? b : a));
  const nonRobust = rows.filter((c) => c.status !== "robust" && c.status !== "Holm-significant").length;
  const sourceLabel = rows[0]?.label ?? "confirmatory";

  return (
    <>
      <section id="overview" aria-labelledby="h-overview">
        <h2 id="h-overview">Overview</h2>
        <p className="paper-title">{r.title}</p>
        <p className="status-label">{r.status_label}</p>
        <p className="lede">{r.question}</p>
        <p>
          Agents decide one after another whether a hidden binary state is 0 or 1. Each has a private signal that is right with
          probability q and sees some of the earlier choices. The study compares exact Bayesian learners and naive vote counters
          with agents who ignore everyone else, on the same signals. The confirmatory study found every one of its {main.length}{" "}
          contrasts positive, from {smallest.display} {smallest.interval_display} to {largest.display} {largest.interval_display} on the
          proportion scale, while the same rules often locked whole groups into the wrong answer. Nothing here concerns real people.
        </p>
      </section>

      <section id="results" aria-labelledby="h-results">
        <h2 id="h-results">Published results</h2>
        <p className="note">
          Numbers in this section come from the committed results (confirmatory runs at code revision <code>{r.code_revision.slice(0, 7)}</code>;
          other revisions under Method). They are printed exactly as in the manuscript and are separate from anything the
          sandbox produces.
        </p>
        <figure className="panel chart" aria-labelledby="fig-forest-cap">
          <div className="chart-head">
            <h3 id="fig-forest-title">Gain in episode accuracy from observing others</h3>
            <Label kind={sourceLabel} />
          </div>
          <label className="inline">
            Data
            <select id="forest-source" value={source} onChange={(e) => setSource(e.target.value)}>
              {SOURCES.map((s) => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </label>
          <p id="fig-forest-cap" className="caption">
            Each row is one cell (signal precision q, network, visibility v). The circle is the Bayesian rule and the square the
            imitation rule; the horizontal line is the unadjusted 95% interval of the mean paired difference against independent
            agents on the same episodes (proportion scale, 0.01 is one accuracy point). The solid vertical line is zero and the
            dashed line the protocol's practical threshold of 0.01. Hollow marks, drawn at the same size, are contrasts that are
            not Holm-significant{source === "main" ? "" : " in this variation (by the frozen EXP-003 rule: lost significance)"}.
            {" "}{rows.length} contrasts shown; {nonRobust} hollow. The exact values are printed beside each row.
          </p>
          <ForestPlot rows={rows} lo={lo} hi={hi} idPrefix="forest" />
        </figure>

        {r.experiments.map((e) => (
          <article key={e.id} className={`panel exp ${expKind(e.status)}`} aria-labelledby={`h-${e.id}`}>
            <h3 id={`h-${e.id}`}>
              {e.id}: {e.title}
            </h3>
            <p>
              <Label kind={expKind(e.status)} /> <span className="meta">{e.status}</span>
            </p>
            <p>
              <strong>Verdict under the frozen rule:</strong> {e.verdict}
            </p>
            {e.estimates.length > 0 && <EstimateTable id={e.id} estimates={e.estimates} />}
            {e.notes.map((n, i) => (
              <p key={i} className="note">{n}</p>
            ))}
            <p className="meta">
              Report: <code>{e.report_path}</code>
              {e.claim_ids.length > 0 && <> · Claims: {e.claim_ids.join(", ")}</>}
            </p>
          </article>
        ))}
      </section>

      <Distribution r={r} />

      <section id="assumptions" aria-labelledby="h-assumptions">
        <h2 id="h-assumptions">Assumptions</h2>
        <p className="note">
          <Label kind="assumption" /> These are the model's settings and the protocol's analysis choices. They are inputs, not
          findings; every result above holds only under them.
        </p>
        <dl className="assumptions">
          {r.assumptions.map((a) => (
            <div key={a.name}>
              <dt>{a.name}</dt>
              <dd>
                {a.value} <span className="meta">({a.source})</span>
              </dd>
            </div>
          ))}
        </dl>
      </section>

      <section id="method" aria-labelledby="h-method">
        <h2 id="h-method">Method and limitations</h2>
        <p>
          The engine is written in Python with numpy. Bayesian posteriors are exact: a public-belief recursion for the complete
          history and a forward recursion over the possible observed windows for window-k networks. An independent exact rational
          oracle, a closed-form cascade probability and a zero-information case check it. EXP-002 and EXP-003 follow protocols
          frozen with the owner's approval before they ran; each ran once. Contrasts are paired on common random numbers, with
          normal 95% intervals at the episode level, a bootstrap check and Holm-adjusted p-values. EXP-001 (verification) and
          EXP-004 (post hoc) are exploratory.
        </p>
        <h3>Limitations</h3>
        <ol className="limits">
          {r.limitations.map((l, i) => (
            <li key={i}>{l}</li>
          ))}
        </ol>
        <details>
          <summary id="sum-revisions">Runs and code revisions</summary>
          <ul className="meta">
            {r.run_revisions.map((x) => (
              <li key={x.run_id}>
                {x.run_id} ({x.label}): <code>{x.code_revision.slice(0, 7)}</code>, <code>{x.result_path}</code>
              </li>
            ))}
          </ul>
        </details>
        <details>
          <summary id="sum-sources">Source files and hashes</summary>
          <ul className="meta">
            {r.sources.map((s) => (
              <li key={s.path}>
                <code>{s.path}</code> <code>{s.sha256.slice(0, 12)}</code>
              </li>
            ))}
          </ul>
        </details>
      </section>
    </>
  );
}

function EstimateTable({ id, estimates }: { id: string; estimates: Estimate[] }) {
  const table = (
    <div className="table-scroll" role="region" aria-label={`${id} estimates`} tabIndex={0} id={`tbl-${id}`}>
      <table>
        <thead>
          <tr>
            <th scope="col">Quantity</th>
            <th scope="col">Estimate</th>
            <th scope="col">Interval</th>
          </tr>
        </thead>
        <tbody>
          {estimates.map((x) => (
            <tr key={x.label}>
              <th scope="row">{x.label}</th>
              <td className="num">{fmtEstimate(x)}</td>
              <td className="num">{x.interval_display ?? (x.ci_low === null ? "none (exact or descriptive)" : fmtInterval(x))}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  if (estimates.length <= 12) return table;
  return (
    <LazyDetails id={`sum-${id}`} summary={`All ${estimates.length} estimates with their intervals`}>
      {table}
    </LazyDetails>
  );
}

/** A details element whose content is rendered only while open, so closed content is never in the tab order. */
function LazyDetails({ id, summary, children }: { id: string; summary: string; children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <details onToggle={(e) => setOpen((e.currentTarget as HTMLDetailsElement).open)}>
      <summary id={id}>{summary}</summary>
      {open && children}
    </details>
  );
}

function Distribution({ r }: { r: Results }) {
  const qs = [...new Set(r.cells.map((c) => c.q))];
  const nets = [...new Set(r.cells.map((c) => c.network))];
  const vs = [...new Set(r.cells.map((c) => c.v))];
  const [q, setQ] = useState(qs[0]);
  const [net, setNet] = useState(nets[0]);
  const [v, setV] = useState(vs[0]);
  const cell = r.cells.find((c) => c.q === q && c.network === net && c.v === v);
  return (
    <section id="distribution" aria-labelledby="h-distribution">
      <h2 id="h-distribution">Accuracy distribution: a positive mean, a split outcome</h2>
      <p>
        A mean gain does not mean that every group gains. Under social learning the distribution of episode accuracy is bimodal
        (limitation 10): groups tend to end mostly right or mostly wrong. In the complete network, once the visible lead reaches
        two, later agents follow it whatever their own signal says, so the group stops learning. Choose a cell to see the
        distribution of episode accuracy for each rule in EXP-002.
      </p>
      <div className="controls">
        <label>
          Signal precision q
          <select id="dist-q" value={q} onChange={(e) => setQ(Number(e.target.value))}>
            {qs.map((x) => (
              <option key={x} value={x}>{x.toFixed(2)}</option>
            ))}
          </select>
        </label>
        <label>
          Network
          <select id="dist-net" value={net} onChange={(e) => setNet(e.target.value)}>
            {nets.map((x) => (
              <option key={x} value={x}>{x}</option>
            ))}
          </select>
        </label>
        <label>
          Visibility v
          <select id="dist-v" value={v} onChange={(e) => setV(Number(e.target.value))}>
            {vs.map((x) => (
              <option key={x} value={x}>{x}</option>
            ))}
          </select>
        </label>
      </div>
      {cell && (
        <figure className="panel chart">
          <div className="chart-head">
            <h3>
              EXP-002, q {cell.q.toFixed(2)}, {cell.network}, v {cell.v}
            </h3>
            <Label kind="confirmatory" />
          </div>
          <p className="caption">
            Bars: share of the {cell.arms[0].n_episodes.toLocaleString("en")} episodes (N = {cell.n_agents} agents each) whose
            accuracy falls in each band of width 0.05, from 0 (everyone wrong) to 1 (everyone right). Vertical axis from 0 to 1.
            Source: the accuracy histograms in <code>results/EXP-002/EXP-002-R001/result.json</code>.
          </p>
          <div className="hists">
            {cell.arms.map((a) => (
              <div key={a.rule} className="hist-col">
                <Histogram counts={a.counts} total={a.n_episodes} title={RULE_LABEL[a.rule]} tone={a.rule} />
                <dl className="stats">
                  <dt>Mean accuracy</dt>
                  <dd>{a.accuracy.display} {a.accuracy.interval_display}</dd>
                  <dt>Wrong-cascade probability</dt>
                  <dd>{a.wrong_cascade.display} {a.wrong_cascade.interval_display}</dd>
                  <dt>Mean longest wrong run (agents)</dt>
                  <dd>{a.longest_wrong_run.display} {a.longest_wrong_run.interval_display}</dd>
                  {a.share_below_baseline && (
                    <>
                      <dt>Episodes below the independent group <Label kind="exploratory" /></dt>
                      <dd>{a.share_below_baseline.display} (descriptive, no interval computed)</dd>
                    </>
                  )}
                </dl>
              </div>
            ))}
          </div>
          <LazyDetails id="sum-counts" summary="Episode counts per accuracy band (text version of the chart)">
            <div className="table-scroll" role="region" aria-label="Episode counts per accuracy band" tabIndex={0} id="tbl-counts">
              <table>
                <thead>
                  <tr>
                    <th scope="col">Accuracy band</th>
                    {cell.arms.map((a) => (
                      <th key={a.rule} scope="col">{RULE_LABEL[a.rule]}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {cell.arms[0].counts.map((_, i) => (
                    <tr key={i}>
                      <th scope="row">
                        {cell.arms[0].edges[i].toFixed(2)} to {cell.arms[0].edges[i + 1].toFixed(2)}
                      </th>
                      {cell.arms.map((a) => (
                        <td key={a.rule} className="num">{a.counts[i]}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </LazyDetails>
          <p className="note">
            Intervals are 95% normal intervals over episodes, as printed in the supplementary table TAB-S04. The wrong-cascade
            probability counts an episode once even if the cascade is later broken.
          </p>
        </figure>
      )}
    </section>
  );
}
