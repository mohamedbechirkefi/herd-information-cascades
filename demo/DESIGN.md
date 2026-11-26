<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# HERD demo: design plan (owner request, 2026-11-26)

## Subject, audience, job

- **Subject.** Agents decide one after another whether a hidden state is 0 or 1, each with a private signal and a view of earlier choices. Watching others raises average accuracy, yet the same rules often lock whole groups into the wrong answer.
- **Audience.** A curious technical reader, an admissions committee, a researcher checking the numbers.
- **Primary job.** Show the two-sided answer in one sentence, make the lock-in visible as a line of people, then give the evidence (gains with intervals, the split outcome distribution) and a sandbox that replays a cascade.

## Direction: the queue and the signal card

A line of people seen from the side, each holding up a card with their choice. The look borrows from crowd signage and public information posters: a saturated signal-yellow field, heavy wide letters, flat colour, no texture. The line runs left to right, the way a cascade runs. Two outcome colours do all the semantic work: teal for a correct choice, magenta for a wrong one; the rule colours (indigo for the Bayesian rule, ochre for imitation) appear only in charts that compare rules.

## Colour (6 named values, plus one support)

| Name | Hex | Role |
|---|---|---|
| Signal yellow | `#F5CF3A` | hero field, the Run button label, the sandbox title |
| Queue ink | `#1B1D2A` | text, rules, figures |
| Chalk | `#F3F4F7` | page background (cool, not cream) |
| Right teal | `#0E6B66` | a correct choice |
| Locked magenta | `#B0195C` | a wrong choice, the wrong cascade |
| Bayes indigo | `#2B3FA8` | the Bayesian rule in charts, links |
| Imitation ochre (support) | `#8F5200` | the imitation rule in charts |

Light only: the yellow field and the flat poster colours lose their meaning on a dark page. `color-scheme: light`.

## Type

- **Anybody** (variable weight and width, OFL-1.1): display. Set wide (`font-stretch` 130 to 150%) and heavy for the headline, like poster lettering; the width axis lets section titles sit narrower than the hero.
- **Atkinson Hyperlegible Next** (variable, OFL-1.1): text, labels and figures. Designed for legibility, with clearly distinct numerals, which suits a page full of intervals. Tabular figures for numbers; no monospace face.

Scale (rem): 0.8125 / 0.9375 / 1.0625 body / 1.375 / 2.25 / clamp(2.4, 6vw, 4.6) hero. Body leading 1.6, measure 68ch.

## Layout

```
+-------------------------------------------------------------+
| [H] HERD    Answer  Evidence  Split outcomes  Sandbox  Method|  sticky, sliding marker
+-------------------------------------------------------------+
| SIGNAL YELLOW                                               |
|  When does watching others help a group decide,             |
|  and when does it lock the group into an error?             |
|  one-sentence answer                                        |
|                                                             |
|  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o      |  the queue: people with cards
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |      |
|        [=========== locked in (magenta) ================]  |
|  Illustration, not study data                               |
+-------------------------------------------------------------+
| CHALK                                                       |
|  Overview: paper title, status, the contrasts in one line   |
|  Evidence: gain plot (forest) + one ledger entry per exp.   |
|  Split outcomes: three histograms side by side (key picture)|
|  Sandbox: the same queue, run by the visitor                |
|  Assumptions, method, limitations, footer                   |
+-------------------------------------------------------------+
```

Left-aligned text; the queue spans the full width of the content column.

## Motion

- **Hero moment (once, about 2.2 s).** The people step into line left to right (60 ms stagger); each raises a card. The first two cards come up magenta on unlucky signals; from the third person on every card is magenta although some private signals (the small dot on each body) are teal. A magenta bracket then draws under the locked-in part. Labelled "Illustration, not study data"; no number.
- **Answers to actions.** The nav marker slides to the section in view. The forest plot draws once when scrolled into view (intervals grow from their estimate, 40 ms stagger). Distribution bars grow from the baseline when a cell is chosen. In the sandbox, each agent's card settles into place as the replay reaches it (180 ms, already paced by the replay), and the result panel enters with `@starting-style`.
- **Reduced motion.** The queue is drawn in its final state, charts appear without growth, the replay switch defaults to off (as before). Hover motion only inside `(hover: hover) and (pointer: fine)`; no `transition: all`.

## The one memorable thing

The queue of people with their cards and the magenta "locked in" bracket under them. Everything else is quiet.

## Review against the frontend-design tells and the other demos

- *First draft* kept the old editorial look (warm paper, serif headings): that is tell 1. **Changed** to a cool chalk page and a signal-yellow hero, with a wide grotesque instead of a serif.
- *First draft* coloured right and wrong with the usual green and red. **Changed** to teal and magenta, which keeps the two apart for red-green colour blindness and is not a traffic light; every coloured cell also carries text.
- *First draft* had pill badges with tracked capitals for status. **Changed** to sentence-case labels with distinct border styles (solid for confirmatory, dashed for exploratory, dotted for assumptions), so status is never told by colour alone.
- *First draft* drew the queue as numbered boxes 01, 02, 03. The order is a real sequence here, but the numbers looked like data; **changed** to unnumbered people, with the order carried by position.
- *Against the other demos.* PARADOX owns ballots and chalk tallies, MATCH owns cards in decks, VIRAL owns network graphs; HERD avoids all three by keeping one straight line of people and one bracket. No other demo uses a yellow field.
