// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
// Brand mark, hero illustration and small motion helpers. The hero queue is a fixed drawing,
// labelled "Illustration, not study data"; it prints no number.
import { useEffect, useRef, useState, type RefObject } from "react";

// The mark: an H made of two people sharing one bar (public/brand/herd-mark-*.svg).
const MARK_D =
  "M40 62 A32 32 0 1 0 104 62 A32 32 0 1 0 40 62 Z M152 62 A32 32 0 1 0 216 62 A32 32 0 1 0 152 62 Z M44 232 V140 A28 28 0 0 1 72 112 H72 A28 28 0 0 1 100 140 V232 Z M156 232 V140 A28 28 0 0 1 184 112 H184 A28 28 0 0 1 212 140 V232 Z M100 150 H156 V186 H100 Z";

export function Mark({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 256 256" aria-hidden="true" focusable="false">
      <path d={MARK_D} fill="currentColor" />
    </svg>
  );
}

export const reducedMotion = () => {
  try {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch {
    return true;
  }
};

/** Adds the class "is-in" once, the first time the element scrolls into view. Under reduced
 * motion, without IntersectionObserver, or when already on screen, nothing is hidden. */
export function useRevealOnce<T extends Element>(): [RefObject<T | null>, string] {
  const ref = useRef<T | null>(null);
  const [state, setState] = useState("");
  useEffect(() => {
    const el = ref.current;
    if (!el || reducedMotion() || typeof IntersectionObserver === "undefined") return;
    const r = el.getBoundingClientRect();
    if (r.top < window.innerHeight && r.bottom > 0) return;
    setState("reveal-armed");
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setState("reveal-armed is-in");
          io.disconnect();
        }
      },
      { rootMargin: "0px 0px -12% 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return [ref, state];
}

// ------------------------------------------------------------------ hero queue (illustration)

// Private signals of a fixed line of people (true = points to the right answer). The first two
// draw misleading signals; from the third person on, everyone copies the visible lead.
const SIGNALS = [false, false, true, false, true, true, false, true, true, true, false, true, true, false, true, true, true, false, true, true];
const LOCK_FROM = 2;
const CELL = 48;

export function HeroQueue() {
  const n = SIGNALS.length;
  const W = n * CELL;
  const x0 = LOCK_FROM * CELL + 6;
  const x1 = W - 6;
  return (
    <svg className="queue-svg" viewBox={`0 0 ${W} 150`} aria-hidden="true" focusable="false">
      {SIGNALS.map((sig, i) => {
        const cx = i * CELL + CELL / 2;
        return (
          <g key={i} className="person" style={{ animationDelay: `${200 + i * 60}ms` }}>
            <line x1={cx + 7} y1={70} x2={cx + 7} y2={34} className="arm" />
            <rect
              x={cx - 6}
              y={6}
              width={26}
              height={30}
              rx={3}
              className="card wrong"
              style={{ animationDelay: `${330 + i * 60}ms` }}
            />
            <circle cx={cx} cy={56} r={10} className="body-ink" />
            <path d={`M${cx - 13} 118 V82 a13 13 0 0 1 26 0 V118 Z`} className="body-ink" />
            <circle cx={cx} cy={92} r={5.5} className={`signal ${sig ? "right" : "wrong"}`} />
          </g>
        );
      })}
      <path d={`M${x0} 128 V138 H${x1} V128`} className="lock-bracket" />
    </svg>
  );
}

// ------------------------------------------------------------------ sticky navigation

export const SECTIONS = [
  { id: "overview", label: "Answer" },
  { id: "results", label: "Evidence" },
  { id: "distribution", label: "Split outcomes" },
  { id: "sandbox", label: "Sandbox" },
  { id: "method", label: "Method" },
];

export function QueueNav() {
  const list = useRef<HTMLUListElement | null>(null);
  const bar = useRef<HTMLSpanElement | null>(null);
  const [active, setActive] = useState<string | null>(null);

  useEffect(() => {
    if (typeof IntersectionObserver === "undefined") return;
    const seen = new Map<string, boolean>();
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) seen.set(e.target.id, e.isIntersecting);
        const first = SECTIONS.find((s) => seen.get(s.id));
        setActive(first ? first.id : null);
      },
      { rootMargin: "-30% 0px -60% 0px" },
    );
    const observe = () => SECTIONS.forEach((s) => { const el = document.getElementById(s.id); if (el) io.observe(el); });
    observe();
    const t = window.setTimeout(observe, 800);
    return () => { io.disconnect(); window.clearTimeout(t); };
  }, []);

  useEffect(() => {
    const track = list.current?.parentElement;
    const b = bar.current;
    if (!track || !b) return;
    const a = active ? track.querySelector<HTMLAnchorElement>(`a[href="#${active}"]`) : null;
    if (!a) { b.style.opacity = "0"; return; }
    b.style.opacity = "1";
    b.style.transform = `translateX(${a.offsetLeft}px) scaleX(${a.offsetWidth})`;
  }, [active]);

  return (
    <nav className="queuebar" aria-label="Sections">
      <div className="wrap queuebar-in">
        <a className="brand" href="#top" aria-label="HERD, back to top">
          <Mark className="brand-mark" />
          <img className="brand-word" src="brand/herd-wordmark-ink.svg" alt="" width="411" height="150" />
        </a>
        <div className="nav-track">
          <ul ref={list}>
            {SECTIONS.map((s) => (
              <li key={s.id}>
                <a href={`#${s.id}`} aria-current={active === s.id ? "true" : undefined}>
                  {s.label}
                </a>
              </li>
            ))}
          </ul>
          <span ref={bar} className="nav-ind" aria-hidden="true" />
        </div>
      </div>
    </nav>
  );
}
