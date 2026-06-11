# SME Review Panel

The ArcaAI design phase uses a panel of AI engines as Subject Matter Experts, each with a specific review role. This document defines who is on the panel, what each does, and when each is used.

## Honest framing

AI SMEs are well-read amateurs, not domain specialists. They catch structural gaps, logical inconsistencies, and shallow errors brilliantly. They do not give legal opinions, predict regulator behaviour, or replace a Big Four compliance review when one is eventually needed. **The panel is a quality filter, not a fitness-for-purpose certificate.**

The human SME for bank-side fitness-for-purpose is Mike — 35 years of banking architecture, Imperial College London AI professional graduate. Mike has the final say on every specification.

## Panel composition

| Role | Who | Frequency | Used for |
|---|---|---|---|
| Bank CTO/CDAO/architect — **final say** | Mike Kennelly | Every change | All specifications and ADRs |
| AI engineering critique (primary) | DeepSeek | Every round | Technical depth on ML/AI specifics |
| AI engineering critique (secondary) | ChatGPT | Every round | Breadth, alternative perspectives |
| Structural critique | Grok | Rounds 1 and 3 | Catching sloppy thinking, weak arguments |
| Regulatory reviewer | Mistral Le Chat (Mistral Large) | Every round on Security/Operations/Integration; spot reviews on others | EU AI Act, GDPR, PRA SS1/23, FCA, DORA framing |
| Regulatory currency check | Perplexity Pro | As-needed research tool | Verifying current state of specific regulations |
| Cross-document consistency | NotebookLM | End of each round, with all in-flight specs loaded | Surfacing contradictions across specs |
| Fresh-eyes pass | Claude (clean session) | Round 3 only | Catching accumulated drift in this Claude's work |
| Day-to-day production partner | Claude (this working session) | Daily | Drafting, challenging, integrating, repo hygiene |

## When each SME is used

### Every round

- **DeepSeek + ChatGPT** — primary engineering review
- **Mistral Le Chat** — regulatory review (heavier weighting on Security and Compliance, Operations, Integration specs)
- **Mike** — final adjudication

### Round 1 specifically — Structural review

- **Grok** — strongest structural critique; less polite, catches things others soften
- DeepSeek + ChatGPT for technical structure
- Mistral for regulatory framework fit

### Round 2 specifically — Content review

- DeepSeek for technical depth
- ChatGPT for breadth and alternative views
- Mistral for regulatory content correctness
- **NotebookLM** — cross-spec consistency check with all in-flight specs loaded as sources

### Round 3 specifically — Adversarial review

- Grok as "skeptical Director of InfoSec"
- ChatGPT as "hostile Model Risk reviewer"
- **Claude (clean session)** — fresh-eyes pass with no context from prior rounds
- Mistral for final regulatory sign-off

## When to add or change panel members

The panel composition is itself subject to review. Add or change panel members when:

- A new AI engine becomes meaningfully better at a specific role
- An existing panel member's quality demonstrably declines (track this over time)
- A new specialty is needed (e.g. a specific banking-vertical reviewer)

Changes to the panel are made through an RFC.

## Cost and access

All current panel members are accessible at free or low-cost tiers (Mistral Le Chat free or Pro, Perplexity Pro, ChatGPT Plus, DeepSeek free, Grok via X subscription, NotebookLM free, Claude via this subscription). No enterprise procurement required.

If panel needs grow (e.g. dedicated legal AI like Harvey), enterprise procurement may be considered in a future phase.

## Prompt primers

Each SME has a standardised prompt primer in `sme-prompt-primers/`. The primer goes at the top of every review request to that SME. The primer:

- Establishes project context
- States the SME's specific role
- Frames what to focus on and what to ignore
- Defines the output format expected

Prompt primers are themselves under version control and are reviewed when SME quality changes.
