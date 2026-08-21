# M13 STANDARDS REGISTER — WORKING DOCUMENT

**Status: WORKING DOCUMENT. The register itself lives in `DECISIONS.md`.**

**The authoritative register is the "Standards register (STD series)" section of
`DECISIONS.md`.** This file is the working that produced it: it carries the
column definitions, the two lifecycle vocabularies, the derivation rules and
the findings, none of which belong in a ledger line. Where this document and
the register differ, **the register is authoritative.**

That relationship is the one `docs/governance/SS1-23_PRINCIPLE_MAPPING.md` §7
describes for itself — a working input that produced obligations recorded
elsewhere — and it is the relationship the Chair ruling of 2026-08-21 directed.

Authorised as ENV-T1-3 by `docs/governance/DEC-0018_CANDIDATE_2026-08-17.md`
Part II, whose scope line reads *"M13 Standards Register. Scope: register
artefact from rider transport file (CC PROMPT 21 rider, 2026-08-14). Artefact:
declared control baseline. STOP SP-2."* Drafted at PROMPT 128; ID scheme ruled
at PROMPT 128R; restructured under that ruling in the same attended block.

**NOTHING IN THE REGISTER IS RATIFIED.** All ten entries carry `mapping_state`
`proposed`. Ratification is a Chair act which the 2026-08-21 ruling expressly
did not perform, so the register may not yet be cited as a declared control
baseline. That is a status, not a defect: the register was designed to hold
unratified rows, which is what `proposed` is for.

**Rider transport note, stated rather than glossed.** The authorising scope
names a rider transport file (CC PROMPT 21 rider, 2026-08-14) as this
register's source. That file is **not in this repository** — a repo-wide search
found no artefact of that description. This register is therefore built from
ratified in-tree artefacts only, which is what the authoring prompt directed,
and the rider's content is **not** incorporated. If the rider carries entries
the register lacks, the difference is a finding and not a merge conflict. This
is a live instance of the `CLAUDE.md` queue item 34 M2 gap — the deliberative
trail sitting outside the evidence perimeter.

**No control-mapping line is carried on this document.** Queue item 34 M11(d)
requires per-class mapping content to be defined once in the control framework,
and that framework does not exist yet. `docs/governance/ARC_REGISTER.md` omits
its line for the same reason and states so. That M13 — the standards register —
cannot yet carry a standards-mapping line is an ordering consequence, not an
oversight.

---

## 1. What this register is, and the claim it must never make

The register records, per external obligation, **which ArcaAI artefact provides
evidence supporting it** — and nothing stronger.

That wording is inherited, not chosen. `docs/governance/SS1-23_PRINCIPLE_MAPPING.md`
§3 was ratified 2026-07-25 with the governing sentence: *"The mapping identifies
which platform artefacts provide evidence supporting a firm's compliance with
the SS1/23 principles. It does not claim that producing those artefacts alone
satisfies the principles, because governance responsibilities remain with the
deploying firm."* An artefact **provides evidence supporting** an obligation.
It never **satisfies** one. Principles and duties attach to firms; evidence is
what a platform can supply.

**Forbidden words, mechanically.** Per queue item 34 M11(a), the words
*compliant*, *certified* and *conformant* may not appear in a mapping line
absent an actual certificate, and `scripts/check_docs.py` is to gain an
assertion enforcing both the line format and the forbidden-words rule. That
assertion does not exist yet. Until it does, this rule is a convention in a
document, which is precisely the enforcement gap M11(a) names — *"a convention
against overclaiming is exactly the kind that erodes under sales pressure."*

**The one-time-input tension is NOT resolved, and is flagged rather than
buried.** `docs/governance/SS1-23_PRINCIPLE_MAPPING.md` §7 declares itself a
one-time input, superseded once its obligations fold into the B8 and B9 gate
documents, on the reasoning that a standing matrix maintained alongside the
build is exactly the parallel document that drifts. Neither gate document
exists, so that mapping is not yet superseded; and if the STD register becomes
standing, §7's objection applies to it by its own logic. The 2026-08-21 ruling
settled where the register lives, not whether a standing register is the right
instrument. Owed.

## 2. Columns

Eleven columns. The two-axis split at columns 8 and 9 is the load-bearing
design property and is explained below the table.

| # | Column | Content |
|---|---|---|
| 1 | `id` | `STD-NNNN`. Assignment rule at section 4. |
| 2 | `framework` | One token from the closed vocabulary at section 3. |
| 3 | `reference` | The clause, principle or article identifier inside that framework. |
| 4 | `obligation` | What the external instrument expects, in one line, in the instrument's own terms. |
| 5 | `applicability` | Whether and when the obligation binds — firm scope, jurisdiction, deployment context. |
| 6 | `ownership` | `platform-supplies`, `bank-owns`, or `shared`. |
| 7 | `evidence_artefacts` | Named artefacts, by repo-relative path where one exists. |
| 8 | `mapping_state` | Lifecycle state of the **mapping row**. Section 3. |
| 9 | `evidence_status` | Whether the evidence **exists**. Section 3. |
| 10 | `basis` | Provenance quality of the row: `RATIFIED-DIRECT`, `RATIFIED-DERIVED`, or `UNPLACEABLE`. |
| 11 | `limits` | What the row does not cover, stated affirmatively. |

**Why columns 8 and 9 are separate, and why collapsing them would be a
defect.** A mapping can be ratified while the evidence it points at does not
exist. SS1/23 Principle 1 is the live case: its mapping was ratified
2026-07-25 and the model inventory it names is a B8-exit artefact, while the
build is at B7. A single-status register would show that row as *ratified* and
a reader would take the evidence as existing. That is the check-method family's
core failure shape — a green whose subject is narrower than the subject it
appears to name — tracked at `CLAUDE.md` queue item 8 across more instances
than any other item in the queue. Two axes, so the register cannot make that
claim by construction.

**Column 10 follows `docs/governance/ARC_REGISTER.md`**, which marks provenance
quality per cell rather than averaging measured and derived values into one
claim. `RATIFIED-DIRECT` means the ratified source states the mapping itself.
`RATIFIED-DERIVED` means the mapping follows from ratified text that was
written for another purpose. `UNPLACEABLE` is section 6.

## 3. Controlled vocabularies

### 3.1 Framework vocabulary — CLOSED, and inherited rather than authored

Per queue item 34 M11: `SS1/23`, `ISO42001`, `ISO27001`, `SOC2`,
`NIST-AI-RMF`, `EU-AI-Act`. Closed, meaning no token outside the six.

**This closure has consequences that section 6 records rather than works
around.** Three obligations derivable from ratified decisions have no token
available to them. Widening the vocabulary is a ruling, expressly **not** taken
at PROMPT 128R, and it is not taken here.

### 3.2 `mapping_state` — five states

Derived from ratified precedent rather than invented. DEC-0014 gives corpus
eligibility as `included`, `pending_review`, `withdrawn`, `deprecated`; DEC-0012
Gap 1 gives the model inventory `active`, `deprecated`, `retired`, `withdrawn`,
`archived`.

- `proposed` — drafted from a ratified source; the mapping is not yet ruled.
- `ratified` — the mapping is chair-ruled.
- `deprecated` — still true, scheduled for replacement; a successor is expected.
- `superseded` — replaced by a named later row. **The pointer is mandatory.**
- `withdrawn` — ruled not applicable, or ruled wrong.

**Every entry is `proposed`.** Nothing has been ruled.

### 3.3 `evidence_status` — five outcomes, and UNKNOWN never collapses into green

- `EVIDENCED` — the named artefact exists in the tree and is cited by path.
- `PARTIAL` — some named artefacts exist and some do not. **A `PARTIAL` row
  must enumerate both sides.** A partial identity that does not name its
  missing parts reads as a complete one.
- `OWED` — the artefact is specified by a ratified decision and is not built.
- `NONE` — no artefact exists and none is specified.
- `UNKNOWN` — could not be determined. **Never green, never red.**

The three-outcome discipline is the repository's standing rule for checks and
is applied here to evidence claims for the same reason.

### 3.4 Transitions, not overwrites — normative

A state that changes is recorded as a dated transition with a reason. A mutable
state field is **prohibited**. This is DEC-0014's corpus-eligibility discipline
and DEC-0012 Gap 1's lifecycle discipline, both ratified, applied unchanged:
*"a state that changes must be recorded as a transition, not overwritten."*
An obligation whose mapping is withdrawn is the event a standards register
exists to record, and a register that overwrites it loses exactly the fact a
reviewer will ask for.

## 4. ID scheme — RULED 2026-08-21, Option C

**Ruling, Chair, 2026-08-21, delivered at PROMPT 128R.** M13 standards take
their own dedicated `STD-NNNN` series, **hosted as ledger lines inside
`DECISIONS.md`** and not as numbered files under `decisions/`.

- **Lifecycle basis.** Standards are external, continuing obligations whose
  state changes on external events; an append-only decision log holds that
  poorly. Option B — recording standards as a class within the existing DEC/ADR
  numbering — was rejected on that ground, as collapsing two kinds of artefact
  into one ledger.
- **Mechanical basis.** Hosting as ledger lines clears the
  `scripts/repo_manifest.py` scanner constraint by construction: no leading
  four-digit filenames under `decisions/`, no ADR numbers consumed — including
  the 0011 reserved for Agentic Topology — and no scanner change required.
  Option A, a dedicated series as numbered files, was rejected on that ground.
- **Reader-navigation.** The STD section of `DECISIONS.md` is the authoritative
  register; this file remains the navigable working document pointing at it.
  The queue item 41 enumeration concern was acknowledged by the Chair and ruled
  not to outweigh the scanner hazard or the lifecycle mismatch.

**The scanner limit this creates, stated because it is the cost of the
mechanical basis.** `scripts/repo_manifest.py` does not parse the STD series
either, so it will not report an STD numbering divergence the way it reports
DEC, ADR, CL and WS-E ones. Whether it is extended to read the series is a
separate act, not performed here. The register section header in `DECISIONS.md`
states this before its first number is consumed, as the ruling required.

### 4.1 Numbering order — stated so it is reproducible

Numbers are assigned in the order of the closed framework vocabulary at
`CLAUDE.md` queue item 34 M11 — SS1/23, ISO42001, ISO27001, SOC2, NIST-AI-RMF,
EU-AI-Act — and, within a framework, by the instrument's own reference order.

**Ordering by evidence strength was considered and rejected.** Evidence status
changes as the build advances while a number is permanent, so an
evidence-ordered series would encode a judgement that expires inside an
identifier that does not. Recorded because it is the intuitive ordering — the
PROMPT 128 draft's summary table used it — and will be proposed again.

**Sequence-hold (WS-E 58) applies unchanged:** next number is highest plus one,
only. Ten numbers are consumed; the next free number is **next 0011**, cited as
"next" and never bare.

## 5. Entries — derived from ratified artefacts only

Ten entries, `STD-0001` through `STD-0010`, all `proposed`. **The register
text is in `DECISIONS.md`;** what follows is the working index and the
derivation record.

**Derivation rule applied throughout:** an entry appears only where a
**ratified** artefact establishes it. `docs/governance/CL-21_data-protection.md`
is reviewed and concurred but sits open in the CL ledger, and
`docs/governance/CL-23_policy-as-code.md` states its own status as DRAFT, not
yet panel-reviewed. Neither is used as authority. Where their content is
reached, it is reached through DEC-0012, which is closed, and they are cited as
related reading only.

### Index

| id | framework | reference | mapping_state | evidence_status | basis |
|---|---|---|---|---|---|
| STD-0001 | SS1/23 | Principle 1 — model identification and risk classification | proposed | OWED | RATIFIED-DIRECT |
| STD-0002 | SS1/23 | Principle 2 — governance | proposed | PARTIAL | RATIFIED-DIRECT |
| STD-0003 | SS1/23 | Principle 3 — development, implementation and use | proposed | PARTIAL | RATIFIED-DIRECT |
| STD-0004 | SS1/23 | Principle 4 — independent model validation | proposed | NONE | RATIFIED-DIRECT |
| STD-0005 | SS1/23 | Principle 5 — model risk mitigants | proposed | PARTIAL | RATIFIED-DIRECT |
| STD-0006 | ISO42001 | Clause structure — declared primary map | proposed | NONE | RATIFIED-DERIVED |
| STD-0007 | ISO27001 | Declared secondary map | proposed | NONE | RATIFIED-DERIVED |
| STD-0008 | SOC2 | Trust criteria — declared secondary map, staged target | proposed | NONE | RATIFIED-DERIVED |
| STD-0009 | NIST-AI-RMF | *(none — token in vocabulary, no ratified reference)* | proposed | NONE | RATIFIED-DERIVED |
| STD-0010 | EU-AI-Act | High-risk credit-decision obligations | proposed | NONE | RATIFIED-DIRECT |

### Derivation record

- **STD-0001 to STD-0005** derive from `docs/governance/SS1-23_PRINCIPLE_MAPPING.md`
  §4, RATIFIED 2026-07-25, with STD-0001 and STD-0005 additionally carrying the
  two gaps adopted at DEC-0012, closed July 2026. STD-0005 also carries
  DEC-0010's `outcome_event`, made non-deferrable on SS1/23 monitoring grounds.
  All five are `RATIFIED-DIRECT`: the ratified source states the mapping itself.
- **STD-0004 is the entry that cannot improve.** Its `evidence_status` is
  `NONE` structurally rather than pending, because independence is an
  organisational property and no artefact changes that. The permanent claim
  discipline — the platform is never described as satisfying Principle 4 —
  is ratified text, not drafting caution.
- **STD-0006 to STD-0009** derive from queue item 34's 2026-08-13 amendment
  naming the mapping targets: primarily SS1/23 and the ISO/IEC 42001 clause
  structure, with ISO 27001 and SOC 2 trust criteria secondary. `RATIFIED-DERIVED`,
  and thin — no clause-level mapping exists anywhere. **STD-0009 is thinner
  still: the `NIST-AI-RMF` token sits in the closed vocabulary and no ratified
  artefact references the framework at all.** It is carried as an empty token
  rather than dropped, because a vocabulary member with no referent is a
  finding about the vocabulary. **These four exist to be visibly empty** —
  omitting them would let a reader infer the register had been drawn against
  six frameworks when it has been drawn against two.
- **STD-0010** derives from ruling R11 in `DECISIONS.md`, approved June 2026.
  `RATIFIED-DIRECT`. It is **the only entry carrying a standing currency
  obligation**: R11 requires re-verification at first client use and its
  verification is dated June 2026, fourteen months old at the date of this
  document. The age is stated rather than the date alone, because a dated
  verification presented without its age is the shape of a stale check.

## 6. Derivable, but UNPLACEABLE — the vocabulary is closed and these do not fit

Three obligations follow from **closed, ratified** decisions and have no token
available in the section 3.1 vocabulary. **They take no STD number.** They are
recorded in full rather than forced into an ill-fitting framework, because a
misfiled obligation is harder to find than an unfiled one.

**This is finding F-1, carried forward unchanged by the 2026-08-21 ruling,
which expressly did not decide it.** It needs its own ruling. It arrived from
three independent directions in one drafting pass, which is the argument for
treating it as a vocabulary defect rather than three special cases.

### UK GDPR Article 22C — right to human review of significant automated decisions

- **Derived from** DEC-0012 Gap 2, closed July 2026, which names Article 22C
  explicitly as one of three things the `adjustment_event` artefact closes.
- **Evidence** — the same `adjustment_event` contract and table. `OWED`.
- **Related reading, not authority** — `docs/governance/CL-21_data-protection.md`
  is the fuller treatment and sits **open** in the CL ledger. Its framing is
  the governing one: the architecture states the mechanism, the deploying bank
  decides the policy.

### SM&CR — accountability attaches to a named individual in a named role

- **Derived from** DEC-0012, closed, whose `actor_role` reasoning is explicitly
  SM&CR: *"under SM&CR accountability attaches to a named individual in a named
  role."*
- **Evidence** — the `actor_role` controlled vocabulary. `OWED`.

### FCA Handbook and JMLSG licensing terms — corpus content prohibition

- **Derived from** DEC-0011, closed July 2026. The B7 RAG corpus will not
  contain FCA Handbook, JMLSG, UK Finance or other restrictively licensed
  third-party text, in the repo or in any local vector index; a ChromaDB index
  is a private electronic retrieval system on the plain reading.
- **Evidence** — `EVIDENCED`, and it is **the only fully evidenced control
  reachable from this register**. `verticals/fraud/corpus/MANIFEST.yaml`
  carries a licence column whose vocabulary is two values only,
  `synthetic-arcaai` and `OGL-v3.0`, and DEC-0014 item 5 enforces manifest
  change mechanically at load.
- **limits** — the ratified source states its own limit: coordinator's reading
  of published terms, not legal advice.
- **Note the shape.** The one obligation with complete evidence is the one the
  vocabulary cannot hold. A register drawn only from the closed six would show
  no fully evidenced control at all.

## 7. Named in a RETIRED artefact only — NOT derivable, recorded to prevent mining

`docs/specs/05-security-and-compliance/README.md` lists regulatory mapping
targets including DORA, FCA Handbook sections (SYSC, SUP, GENPRU), GDPR and the
EU AI Act. **That document is RETIRED** — tombstoned under DEC-0007, which
retired the pre-lockdown eight-spec regime — and its own status line reads
*"Version 0.0 (placeholder) / Status: Not started"*.

Nothing in it is a ratified source and nothing has been drawn from it. It is
named here because it is the most inviting document in the tree for someone
populating a standards register, and a retired placeholder read as a
requirements list would put unratified obligations into a control baseline.

**DORA in particular appears nowhere else**, so its absence from the register
is a real gap in coverage rather than an oversight in drafting, and closing it
needs a ratified decision and not a copy-paste. This is finding F-2, carried
forward unchanged by the 2026-08-21 ruling.

## 8. What this document and its register do NOT do

1. **Nothing is ratified.** All ten entries are `proposed`; the register may
   not be cited as a declared control baseline.
2. **F-1 is not resolved** — the framework vocabulary stays closed and the
   three obligations at section 6 stay UNPLACEABLE, per the ruling.
3. **F-2 is not resolved** — DORA remains underivable and unregistered.
4. **F-3 is not resolved** — the EU AI Act currency verification at STD-0010
   remains stale and re-verification is owed.
5. **The rider transport file is not incorporated**, not being in the
   repository.
6. **The one-time-input tension at section 1 is not resolved** — whether a
   standing standards register is the parallel-document failure
   `docs/governance/SS1-23_PRINCIPLE_MAPPING.md` §7 warns against was not
   before the Chair on 2026-08-21.
7. **`scripts/repo_manifest.py` is not extended** to parse the STD series, so
   STD numbering divergences are not mechanically reported.
8. **No control-mapping line is carried**, the control framework that would
   define per-class mapping content not existing yet.
9. **This filename retains its DRAFT token deliberately.** The document is now
   a working document rather than a draft register, and renaming it would
   break every citation of the path — the sweep obligation recorded at
   `CLAUDE.md` queue item 37 for the Rev C Test Plan. The rename belongs with
   the register's ratification, as one deliberate act with its citation sweep,
   not as a tidy-up here.
