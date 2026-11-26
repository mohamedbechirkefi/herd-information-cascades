// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
// Visitor sandbox: runs the ported HERD rules in a Web Worker. Its output is labelled as
// sandbox output and never mixed with the published results.
import { useEffect, useRef, useState } from "react";
import { Histogram, RULE_LABEL } from "./charts";
import { MAX_AGENTS, MAX_EPISODES, type SandboxSettings, type SandboxSummary, type WorkerReply, type WorkerRequest } from "./simulate";

const DEFAULTS: SandboxSettings = { rule: "bayesian", q: 0.55, network: "complete", v: 1, n: 30, tie: "own", episodes: 500, seed: 1 };

const SCENARIOS: { id: string; name: string; set: Partial<SandboxSettings> }[] = [
  { id: "fragile", name: "Weak signals, full history (q 0.55, complete, v 1)", set: { q: 0.55, network: "complete", v: 1 } },
  { id: "partial", name: "Weak signals, short memory, half visible (q 0.55, window-2, v 0.5)", set: { q: 0.55, network: "window-2", v: 0.5 } },
  { id: "strong", name: "Strong signals, three predecessors (q 0.8, window-3, v 1)", set: { q: 0.8, network: "window-3", v: 1 } },
  { id: "noinfo", name: "No information (q 0.5): every Bayesian comparison is a tie", set: { q: 0.5, network: "complete", v: 1 } },
];

const prefersReduced = () => {
  try {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch {
    return false;
  }
};

const f4 = (x: number) => (x >= 0 ? "+" : "") + x.toFixed(4);

export function Sandbox() {
  const worker = useRef<Worker | null>(null);
  const [s, setS] = useState<SandboxSettings>(DEFAULTS);
  const [scenario, setScenario] = useState("fragile");
  const [running, setRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [result, setResult] = useState<SandboxSummary | null>(null);
  const [animate, setAnimate] = useState(() => !prefersReduced());
  const [shown, setShown] = useState(0);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    const w = new Worker(new URL("./sandbox.worker.ts", import.meta.url), { type: "module" });
    w.onmessage = (ev: MessageEvent<WorkerReply>) => {
      const m = ev.data;
      if (m.type === "progress") {
        setProgress(m.fraction);
        return;
      }
      setRunning(false);
      if (m.type === "done") {
        const r = m.summary;
        setResult(r);
        const sign = r.delta.mean >= 0 ? "+" : "";
        setStatus(
          `Sandbox run complete (seed ${r.settings.seed}, ${r.settings.episodes} episodes of ${r.settings.n} agents): ` +
            `${RULE_LABEL[r.settings.rule]} minus independent, mean paired accuracy difference ${sign}${r.delta.mean.toFixed(4)} ` +
            `[${r.delta.ci_low.toFixed(4)}, ${r.delta.ci_high.toFixed(4)}] (normal 95% interval).`,
        );
      }
      if (m.type === "error") setStatus(`Sandbox run failed: ${m.message}`);
      if (m.type === "cancelled") setStatus("Sandbox run cancelled.");
    };
    worker.current = w;
    return () => w.terminate();
  }, []);

  // Replay of the first episode, one agent per tick, when animation is on.
  useEffect(() => {
    if (!result) return;
    if (!animate) {
      setShown(result.settings.n);
      setPlaying(false);
      return;
    }
    setShown(0);
    setPlaying(true);
  }, [result, animate]);
  useEffect(() => {
    if (!playing || !result) return;
    if (shown >= result.settings.n) {
      setPlaying(false);
      return;
    }
    const t = setTimeout(() => setShown((x) => x + 1), 180);
    return () => clearTimeout(t);
  }, [playing, shown, result]);

  const update = (patch: Partial<SandboxSettings>) => {
    setS((x) => ({ ...x, ...patch }));
    setScenario("custom");
  };
  const pickScenario = (id: string) => {
    setScenario(id);
    const sc = SCENARIOS.find((x) => x.id === id);
    if (sc) setS((x) => ({ ...x, ...sc.set }));
  };
  const run = () => {
    setRunning(true);
    setProgress(0);
    setStatus("");
    setResult(null);
    worker.current?.postMessage({ type: "run", settings: s } satisfies WorkerRequest);
  };
  const cancel = () => worker.current?.postMessage({ type: "cancel" } satisfies WorkerRequest);
  const reset = () => {
    if (running) cancel();
    setS(DEFAULTS);
    setScenario("fragile");
    setResult(null);
    setStatus("Sandbox reset to the default settings.");
    setShown(0);
    setPlaying(false);
  };
  const clampInt = (v: string, lo: number, hi: number, dflt: number) => {
    const n = Math.round(Number(v));
    return Number.isFinite(n) ? Math.min(hi, Math.max(lo, n)) : dflt;
  };

  return (
    <section id="sandbox" aria-labelledby="h-sandbox" className="sandbox">
      <div className="sandbox-band">
        <h2 id="h-sandbox">Sandbox: watch a cascade form</h2>
        <p className="stamp">Sandbox output, not a research result</p>
      </div>
      <p className="note">
        The sandbox runs a TypeScript port of the study's decision rules in your browser. The rules match the Python
        engine on a test fixture (identical actions and cascade flags, metrics within 1e-12), but the random draws come
        from a different generator, so no sandbox seed reproduces a research episode. Sandbox numbers are not comparable
        to the published results above and are not stored or sent anywhere.
      </p>
      <div className="controls">
        <label className="wide">
          Scenario
          <select id="sb-scenario" value={scenario} onChange={(e) => pickScenario(e.target.value)}>
            {SCENARIOS.map((x) => (
              <option key={x.id} value={x.id}>{x.name}</option>
            ))}
            <option value="custom">Custom settings</option>
          </select>
        </label>
        <label>
          Social rule
          <select id="sb-rule" value={s.rule} onChange={(e) => update({ rule: e.target.value as SandboxSettings["rule"] })}>
            <option value="bayesian">Bayesian</option>
            <option value="imitation">Imitation (vote counting)</option>
          </select>
        </label>
        <label>
          Signal precision q
          <select id="sb-q" value={s.q} onChange={(e) => update({ q: Number(e.target.value) })}>
            {[0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9].map((q) => (
              <option key={q} value={q}>{q.toFixed(2)}</option>
            ))}
          </select>
        </label>
        <label>
          Network
          <select id="sb-network" value={s.network} onChange={(e) => update({ network: e.target.value })}>
            <option value="complete">complete history</option>
            <option value="window-1">last 1 (window-1)</option>
            <option value="window-2">last 2 (window-2)</option>
            <option value="window-3">last 3 (window-3)</option>
          </select>
        </label>
        <label>
          Visibility v
          <select id="sb-v" value={s.v} onChange={(e) => update({ v: Number(e.target.value) })}>
            {[1, 0.75, 0.5, 0.25, 0].map((v) => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
        </label>
        <label>
          Ties
          <select id="sb-tie" value={s.tie} onChange={(e) => update({ tie: e.target.value as SandboxSettings["tie"] })}>
            <option value="own">follow own signal</option>
            <option value="coin">coin flip</option>
          </select>
        </label>
        <label>
          Agents N
          <input id="sb-n" type="number" min={2} max={MAX_AGENTS} value={s.n} onChange={(e) => update({ n: clampInt(e.target.value, 2, MAX_AGENTS, 30) })} />
        </label>
        <label>
          Episodes
          <input id="sb-episodes" type="number" min={2} max={MAX_EPISODES} step={100} value={s.episodes} onChange={(e) => update({ episodes: clampInt(e.target.value, 2, MAX_EPISODES, 500) })} />
        </label>
        <label>
          Seed
          <input id="sb-seed" type="number" min={0} max={1_000_000} value={s.seed} onChange={(e) => setS((x) => ({ ...x, seed: clampInt(e.target.value, 0, 1_000_000, 1) }))} />
        </label>
      </div>
      <div className="controls buttons">
        <button id="sb-run" type="button" onClick={run} disabled={running}>Run</button>
        <button id="sb-cancel" type="button" onClick={cancel} disabled={!running}>Cancel</button>
        <button id="sb-reset" type="button" onClick={reset}>Reset</button>
        <label className="check">
          <input id="sb-animate" type="checkbox" checked={animate} onChange={(e) => setAnimate(e.target.checked)} /> Animate the cascade (off when
          your system asks for reduced motion)
        </label>
        {running && <progress value={progress} max={1} aria-label="Sandbox progress" />}
      </div>
      <p aria-live="polite" className="sandbox-out">{status}</p>
      {result && <SandboxResult r={result} shown={shown} playing={playing} onReplay={() => { setShown(0); setPlaying(true); }} onShowAll={() => { setPlaying(false); setShown(result.settings.n); }} />}
    </section>
  );
}

function SandboxResult({ r, shown, playing, onReplay, onShowAll }: { r: SandboxSummary; shown: number; playing: boolean; onReplay: () => void; onShowAll: () => void }) {
  const t = r.trace;
  const n = r.settings.n;
  const casc = t.cascade.slice(0, shown).filter(Boolean).length;
  return (
    <div className="sandbox-result" key={`${r.settings.seed}-${r.settings.rule}-${r.settings.q}-${r.settings.network}-${r.settings.v}-${r.settings.n}-${r.settings.episodes}-${r.settings.tie}`}>
      <h3>First episode of this run</h3>
      <p className="note">
        Hidden state: <strong>{t.theta}</strong>. Each column is one agent, in order. Top: its private signal. Middle: the{" "}
        {RULE_LABEL[r.settings.rule].toLowerCase()} agent's action. Bottom: what an independent agent with the same signal does.
        Teal cells are correct, magenta cells are wrong; a dashed outline marks an action nobody can see; a bar under the
        middle cell marks an agent in a cascade (its action would be the same whatever its signal).
      </p>
      <div className="controls buttons">
        <button id="sb-replay" type="button" onClick={onReplay} disabled={playing}>Replay</button>
        <button id="sb-showall" type="button" onClick={onShowAll} disabled={shown >= n}>Show all agents</button>
        <span className="meta" aria-live="off">{Math.min(shown, n)} of {n} agents shown; {casc} in a cascade so far</span>
      </div>
      <ol className="strip" aria-label="Agents of the first sandbox episode">
        {t.signals.map((sig, i) => {
          const on = i < shown;
          const a = t.social[i], b = t.baseline[i];
          return (
            <li key={i} className={on ? "agent on" : "agent"} aria-hidden={!on}>
              <span className={`tok sig ${sig === t.theta ? "ok" : "bad"}`}>{on ? sig : ""}</span>
              <span className={`tok act ${on ? (a === t.theta ? "ok" : "bad") : ""} ${t.visible[i] ? "" : "hidden"} ${on && t.cascade[i] ? "casc" : ""}`}>{on ? a : ""}</span>
              <span className={`tok base ${on ? (b === t.theta ? "ok" : "bad") : ""}`}>{on ? b : ""}</span>
              {on && (
                <span className="sr">
                  Agent {i + 1}: signal {sig}, {RULE_LABEL[r.settings.rule]} action {a}
                  {t.cascade[i] ? " in a cascade" : ""}
                  {t.visible[i] ? "" : ", not visible"}, independent action {b}.
                </span>
              )}
            </li>
          );
        })}
      </ol>
      <h3>Accuracy distribution of this run</h3>
      <p className="note">
        Share of the {r.settings.episodes} sandbox episodes at each level of episode accuracy (proportion of agents correct).
        Wrong cascade in {r.wrongCascade.toFixed(3)} of episodes; the {RULE_LABEL[r.settings.rule].toLowerCase()} group ended below the
        independent group on the same signals in {r.shareBelow.toFixed(3)} of episodes. Mean paired difference {f4(r.delta.mean)} [
        {r.delta.ci_low.toFixed(4)}, {r.delta.ci_high.toFixed(4)}].
      </p>
      <div className="hists">
        <Histogram counts={r.baselineHist} total={r.settings.episodes} title="Independent (sandbox)" tone="independent" />
        <Histogram counts={r.socialHist} total={r.settings.episodes} title={`${RULE_LABEL[r.settings.rule]} (sandbox)`} tone={r.settings.rule} />
      </div>
    </div>
  );
}
