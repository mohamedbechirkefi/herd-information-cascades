<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Literature review (M0, initial and non-systematic)

This is a targeted, non-systematic search made on 2026-11-24 with web search and fetch tools. "Verified" means the bibliographic record and abstract (or an abstract summary) were opened at the URL given on the access date. No full text was read in this session unless stated, so the review relies on abstracts and the standard results they state. Statements about details beyond the abstract are labelled unverified.

## 1. Verified sources

| Key | Reference | Opened (2026-11-24) | What was verified |
|---|---|---|---|
| BHW1992 | Bikhchandani, S., Hirshleifer, D. and Welch, I. (1992). A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades. *Journal of Political Economy*, 100(5), 992-1026. DOI 10.1086/261849 | https://ideas.repec.org/a/ucp/jpolec/v100y1992i5p992-1026.html (the publisher page at doi.org returned HTTP 403) | Metadata and DOI; the record read in this session rendered the title ending "in Informational Cascades", while the commonly cited title ends "as Informational Cascades": to be checked against the publisher record. Abstract: an informational cascade occurs when it is optimal to follow predecessors regardless of one's own information; explains localised conformity and fragility of mass behaviour. |
| Banerjee1992 | Banerjee, A. V. (1992). A Simple Model of Herd Behavior. *Quarterly Journal of Economics*, 107(3), 797-817. DOI 10.2307/2118364 | https://ideas.repec.org/a/oup/qjecon/v107y1992i3p797-817..html | Metadata; abstract: optimising agents who observe predecessors herd, and the equilibrium is inefficient. |
| AH1997 | Anderson, L. R. and Holt, C. A. (1997). Information Cascades in the Laboratory. *American Economic Review*, 87(5), 847-862. | https://ideas.repec.org/a/aea/aecrev/v87y1997i5p847-62.html | Metadata; abstract: laboratory urn experiment with paid predictions; rational cascades formed in most periods with an early imbalance. |
| SS2000 | Smith, L. and Sorensen, P. (2000). Pathological Outcomes of Observational Learning. *Econometrica*, 68(2), 371-398. | https://ideas.repec.org/a/ecm/emetrp/v68y2000i2p371-398.html | Metadata; abstract: with heterogeneous preferences, besides herds, "confounded learning" can arise; Markov-martingale belief analysis. DOI 10.1111/1468-0262.00113 appeared only in a search snippet: unverified. |
| CK2004 | Celen, B. and Kariv, S. (2004). Observational learning under imperfect information. *Games and Economic Behavior*, 47(1), 72-86. | https://ideas.repec.org/a/eee/gamebe/v47y2004i1p72-86.html | Metadata only (the page has no abstract). The description that each agent observes only the immediate predecessor and that behaviour cycles comes from a search snippet: unverified until the paper is opened. |
| GJ2010 | Golub, B. and Jackson, M. O. (2010). Naive Learning in Social Networks and the Wisdom of Crowds. *American Economic Journal: Microeconomics*, 2(1), 112-149. DOI 10.1257/mic.2.1.112 | https://ideas.repec.org/a/aea/aejmic/v2y2010i1p112-49.html | Metadata; abstract: under repeated averaging (DeGroot) beliefs converge to the truth in large societies if and only if the most influential agent's influence vanishes. |
| ER2010 | Eyster, E. and Rabin, M. (2010). Naive Herding in Rich-Information Settings. *American Economic Journal: Microeconomics*, 2(4), 221-243. DOI 10.1257/mic.2.4.221 | https://econpapers.repec.org/RePEc:aea:aejmic:v:2:y:2010:i:4:p:221-43 | Metadata; abstract: naive agents treat predecessors' actions as reflecting only private information, over-weight early movers ("social confirmation bias"), herd on wrong actions with positive probability, and can be worse off from observing others. |
| ADLO2011 | Acemoglu, D., Dahleh, M. A., Lobel, I. and Ozdaglar, A. (2011). Bayesian Learning in Social Networks. *Review of Economic Studies*, 78(4), 1201-1236. DOI 10.1093/restud/rdr004 | https://econpapers.repec.org/RePEc:oup:restud:v:78:y:2011:i:4:p:1201-1236 | Metadata; abstract: sequential learning over a stochastic observation network; with unbounded private beliefs, learning occurs given "expansion in observations"; conditions for bounded beliefs also given. |
| W2008wp | Weizsacker, G. (2008). Do we follow others when we should? A simple test of rational expectations. Working paper, ESRC Centre for Economic Learning and Social Evolution, UCL. | https://researchonline.lse.ac.uk/id/eprint/4945 | Record and abstract: meta data set of 13 laboratory social-learning experiments; where following others is empirically optimal, subjects earn about 53% of the available payoff; they contradict their own signal only at roughly 2:1 empirical odds. The published AER 2010 version (100(5), 2340-2360) was seen only in search snippets: unverified. |

## 2. How the sources position HERD

- The binary-state, binary-signal sequential model with a complete public history is the BHW1992 / Banerjee1992 setting. HERD's `complete` network with $v = 1$ and Bayesian agents is a replication of that model, used as an analytic anchor.
- Partial observation of predecessors is the setting of ADLO2011 (general stochastic networks) and CK2004 (single predecessor). HERD restricts itself to deterministic recent-window networks where exact Bayesian posteriors can be computed by a small forward recursion.
- The imitation rule operationalises the naive inference of ER2010 in its simplest form (count observed actions as independent signals). This is a simplified variant, not a replication of their model.
- GJ2010 concerns repeated averaging rather than one-shot sequential actions; it is related work, not a model HERD implements.
- AH1997 and W2008wp concern human subjects. HERD makes no claim about human behaviour (claims boundary).

## 3. Candidate contribution (narrow, not a novelty claim)

A reproducible, matched-seed simulation map of when Bayesian and naive social learning raise or lower mean decision accuracy relative to independent decisions, jointly over signal quality, a small family of observation networks and action visibility, with cascade, error-persistence and diversity metrics and a pre-registered sensitivity analysis. Whether this specific combination has been reported before has not been established by this non-systematic search; no novelty is claimed.

## 4. Open items

- Open the full texts (or author versions) of BHW1992, CK2004 and ER2010 before M1 closes, to check model details used in the protocol (tie-breaking convention, the single-predecessor results, the naive inference rule).
- Search for prior simulation studies that cross visibility with network structure.
