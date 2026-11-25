// SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
// Web Worker wrapper around simulate() (simulate.ts): runs off the main thread and can be cancelled.
import { type WorkerReply, type WorkerRequest, simulate } from "./simulate";

let cancelled = false;

onmessage = async (ev: MessageEvent<WorkerRequest>) => {
  const m = ev.data;
  if (m.type === "cancel") {
    cancelled = true;
    return;
  }
  cancelled = false;
  try {
    const summary = await simulate(m.settings, (fraction) => postMessage({ type: "progress", fraction } satisfies WorkerReply), () => cancelled);
    postMessage((summary === null ? { type: "cancelled" } : { type: "done", summary }) satisfies WorkerReply);
  } catch (e) {
    postMessage({ type: "error", message: e instanceof Error ? e.message : String(e) } satisfies WorkerReply);
  }
};
