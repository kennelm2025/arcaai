# CL-21 — Data protection and record retention position for decision records, prompts and outcomes

*Raised: 2026-07-25, WS-D session, arising from the B7 corpus licensing
work (DEC-0011). Class: document currency / architecture gap — not a
build defect. Reviewed by ChatGPT and Grok, both concur; dispositions at
the foot. Ledger entry: `GOVERNANCE_REVIEW_CHANGELOG.md`, Workstream D.*

---

## Framing — architecture default versus bank policy

This distinction governs every paragraph below and should be stated
explicitly in the Banking Architecture revision, because without it a
reviewer will read the platform as prescribing compliance policy, which
it must not do:

| The architecture states | The deploying bank decides |
|---|---|
| The platform supports configurable retention schedules | The bank sets the period, e.g. seven years for fraud records |
| The platform supports crypto-shredding of identifiers | The bank determines when it is invoked |
| The platform records the basis on which a decision was reached | The bank determines its lawful basis for processing |
| The platform can retrieve every record relating to one subject | The bank operates its DSAR and erasure process |

ArcaAI's job is to state a defensible default and demonstrate the
mechanism. It is not to rule on the bank's legal position.

## Finding

The suite states no data protection or retention position. The Banking
Architecture describes an append-only audit trail and, following
DEC-0010, an append-only `outcome_event` table. In any real deployment
both hold transaction records, which will be personal data under UK
GDPR — pseudonymisation does not remove them from scope, and
transaction records are difficult to anonymise because the spending
pattern is itself identifying. Nothing in the suite says who the
controller is, what is retained, for what purpose, for how long, or how
erasure is handled against records designed never to be altered.

Six gaps.

### 1. Immutability versus erasure, across competing obligations

"Append-only and never overwritten" and the right to erasure pull in
opposite directions, and the resolution is not purely a data protection
question: AML and fraud retention duties, audit evidence retention, and
model-risk evidence retention are separate obligations owned by
different functions in a bank, and they can require the opposite of what
a minimisation argument would suggest.

The architecture should state the *mechanism* — retention schedules,
crypto-shredding of identifiers while preserving the decision record,
competing legal duty as a ground for retention — and not invent a novel
solution. Where an obligation already has a home in the suite
(model-risk evidence under RAT-07 and SS1/23), point at it rather than
restate it.

### 2. Subject retrieval as an architectural requirement

An append-only store satisfies immutability but says nothing about
*findability*. Both a subject access request and any erasure or
crypto-shred operation require retrieving every record relating to one
individual across the audit trail, the outcome table and the agent
state. That is an indexing requirement on the decision record, and it is
cheap if designed in and expensive if retrofitted.

Not raised by either reviewer; recorded here because it is the one item
in this CL with a build consequence, and it lands in B9.

### 3. Prompt content — proposed as a platform principle

No rule currently governs what reaches the LLM. Proposed principle:

> **LLMs consume the minimum information required to perform the
> reasoning asked of them.**

Concretely: only derived signals — risk scores, feature contributions,
retrieved chunk identifiers — and a non-identifying reference identifier
may enter a prompt. Names, account numbers, sort codes, addresses, and
free-text narrative containing personal data do not. Presidio at B8 is
the backstop, not the primary control.

This is not a compliance concession. It improves privacy, prompt
security, token cost, portability and auditability simultaneously, which
is why it belongs in the principles set rather than in a data protection
paragraph.

**Note for the revision: adding to the Architecture Principles is a
larger change than the paragraph-level edits elsewhere in this CL.** The
principles set is a defined list and an addition needs the same scrutiny
as the original entries.

### 4. Purpose limitation

Retention duration is the question the suite fails to answer; retention
*purpose* is the question it fails to ask. Proposed default text:

> Decision records are retained solely to support auditability, model
> governance, regulatory obligations, fraud investigation and authorised
> operational review. They are not retained for unrestricted analytics
> or future model training unless separately governed.

The final clause matters disproportionately for an AI platform and
pre-empts the obvious question from a bank's DPO.

### 5. Controller/processor default, and the DPIA

In an on-premises or bank-tenancy deployment the bank is the controller
and ArcaAI or the implementation partner is the processor. The
architecture should state this as the default for its deployment model
so that a DPIA does not have to invent it.

It should also say plainly that a DPIA will be required — systematic
automated evaluation with significant effects at scale is squarely the
trigger — and identify what the platform supplies to it: the decision
record schema, the nondeterminism register, the audit replay, and the
guardrail decision log. Neither reviewer raised the DPIA; it is the
concrete artefact a DPO will ask for first.

### 6. Automated decision-making — an argument the architecture does not make

On 5 February 2026 the Data (Use and Access) Act 2025 replaced UK GDPR
Article 22 with Articles 22A–22D. The former default was prohibition of
solely automated significant decisions; the new default is permission
subject to mandatory safeguards — transparency before the decision, a
right to human review, and a right to contest. Special category data
remains restricted under 22B. Fraud prevention decisions may constitute
significant decisions depending on their effect on the individual; where
they do, the 22C safeguards apply.

This favours the platform, and the safeguards map onto artefacts already
planned: the right to contest is unusable without an explanation of
*why* a decision was reached, which is the B9 audit-trail replay and
worked trace; human review is the human-in-the-loop work under RAT-12.
The architecture should make this claim explicitly. It currently
presents the audit trail as governance discipline, when it is also the
Article 22C evidence.

## Proposed resolution

Paragraph-level additions to the next Banking Architecture revision —
not a new document — covering: the architecture-default versus
bank-policy framing; controller and processor split in the deployment
model; what constitutes personal data across the pipeline; the retention
and erasure mechanism across competing obligations; purpose limitation;
the DPIA position and the platform's inputs to it; and the Article
22A–22D safeguards mapping. Plus one addition to the Architecture
Principles set (gap 3), which carries more weight than the rest and
should be reviewed as such.

## Sizing and trigger

Bundle with CL-17/19/20 at the next Banking Architecture revision; hard
trigger post-B8 per RAT-11. One earlier pressure: the first client pilot
conversation will raise this and a bank's DPO will ask before a DPIA is
signed. If a pilot is scheduled before the B8 trigger, this CL is pulled
forward ahead of the rest of the bundle.

## Not a B7 blocker

The reference build is synthetic throughout; there is no personal data
in it. No change to B7 entry criteria, no new gate item. Gap 2 (subject
retrieval) is the single item with a build consequence and it lands in
B9, not B7.

## Limitation

Coordinator's reading, not legal advice. The retention and erasure
position in particular is the sort of thing a bank's own DPO and counsel
will own; the architecture's job is to state a defensible default and
show the mechanism, not to give a ruling.

## Review disposition

- **Retitle to "Information Governance" (ChatGPT) — MODIFIED.** The
  observation is right that "data protection" undersold a finding that
  also covers retention obligations owned by other functions. But
  "Information Governance" oversells in the other direction and invites
  the CL to absorb model-risk evidence and explainability, which already
  have homes in RAT-07, SS1/23 and B9. A CL that grows to fit its title
  is the same failure as a finding placed in the wrong container. Title
  widened to name retention explicitly; gap 1 names the competing
  obligations and points at their existing homes rather than claiming
  them.
- **Architecture default vs bank policy (ChatGPT) — ADOPTED and
  elevated.** The strongest point in either review. Moved to the head of
  the CL as a framing table, because it governs how every other
  paragraph should be read.
- **Prompt minimisation as a platform principle (ChatGPT), with explicit
  field-level text (Grok) — ADOPTED, both.** Principle plus concrete
  rule. Flagged that a principles-set addition is a heavier change than
  the paragraph edits.
- **Purpose limitation omission (ChatGPT) — ADOPTED.** Correct gap,
  proposed text taken close to as offered.
- **Soften "very likely a significant decision" (ChatGPT) — ADOPTED.**
  Significance is context-dependent and the CL should not be making that
  call.
- **State the mechanism, do not invent a solution (Grok) — ADOPTED**
  into gap 1.
- **Controller/processor default (Grok) — ADOPTED**, qualified to the
  deployment model rather than stated absolutely.
- **File both CLs in one pass (Grok) — ADOPTED.** CL-22 (board-level
  KPIs unanchored) filed in the same changelog entry.
- **Additions neither review made:** subject retrieval as an indexing
  requirement (gap 2, the only build consequence in this CL), and the
  DPIA position with the platform's inputs to it (gap 5).
