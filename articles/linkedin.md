<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
<!-- Draft for LinkedIn (M5, 2026-11-25). Not published; publication is the owner's decision. Numbers copied from research/paper/manuscript.md v1.0. -->

Can a group become confidently wrong because everyone watches everyone else?

I built HERD, a simulation study of sequential decisions: each agent has a private noisy signal and sees some earlier choices. I compared exact Bayesian learners and naive vote counters with agents who ignore others, on identical episodes, under a protocol frozen before the main run.

One defensible finding: in the confirmatory study, observing others raised mean accuracy in all 48 contrasts, from +0.0059 (95% CI 0.0048 to 0.0070) to +0.1439 (0.1375 to 0.1504) on the proportion scale. Yet the same rules produced wrong cascades in up to 0.87 of episodes. A higher average can hide many groups locked into the wrong answer.

Caveat: these are synthetic agents in a stylised model, not people. The size of the gain depends strongly on how ties are broken, and my own prediction that naive imitation would hurt accuracy was contradicted. Not peer-reviewed.

Repository: https://github.com/mohamedbechirkefi/herd-information-cascades
Interactive demo: https://herd-information-cascades.kefimohamedbechir.workers.dev

An AI system was used as a research and development assistant.

Mohamed Bechir Kefi, independent researcher
