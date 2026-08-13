---
INPUT ARTEFACT — ADR-0011 input set
Source: panel consolidation of the architecture review (orchestration / memory /
dreaming), dated 2026-08-10; supplied from the operator's disk 2026-08-13.
Original resides outside the repository.
Status note: the body reads "ITEMS FOR RULING - nothing below is effective until
ruled" ON ITS FACE. That status is superseded: the operator RULED all twenty
items on 2026-08-10, together with a supplementary ITEM 21 (canonical vocabulary).
The body is preserved uncorrected for fidelity; this header is the correction.
Rulings record: located 2026-08-13 at the operator's
D:\Downloads\RULINGS_RECORD_2026-08-10_arch-review.md, sha256
78b9e3d26f00a1c7b866b069c72d49dfb4619816bb2decc91ccda690e2acf4f5. It carries
ITEM 21 and the verbatim dissent record. NOT YET PINNED INTO THIS REPOSITORY —
pinning awaits operator instruction; until then, citations to the ruled WORDING
remain pending while citations to the ITEMS below are live.
Numbering correction: the body refers throughout to "ADR-0012" as the Agentic
Topology ADR. That is STALE SELF-NUMBERING. The live register anchor of
2026-08-13 reserves ADR 0011 for Agentic Topology, and 0011 remains RESERVED,
NOT CONSUMED. All "ADR-0012" strings in the body are read as 0011.
Collision note: the body's ITEM 18(b) offers "standalone DEC-0016" as a possible
home for the credential broker. That DEC-0016 is a CANDIDATE NUMBER proposed on
2026-08-10 and is UNRELATED to the actual DEC-0016 (test-database separation,
ruled 2026-08-12). The broker question was ruled: ADR section, not a DEC.
Pin method (ruled 2026-08-13): Circulation pin: sha256 over the complete
committed file with the single line beginning 'Circulation pin' excluded;
canonicalised as the file's raw bytes minus that line including its newline.
Fidelity pin: sha256 over the verbatim body exactly as received.
Fidelity pin (body sha256): cc0f805c7ae1eae170cb57b518e389879ff36ca73917b81f6f6beb6f201bdebc
Circulation pin (file sha256): 6d7a188c111c73b59dd469785b108222dafe500021a221342e1c2b04b0611f40
---

# Panel Consolidation - Architecture Review: Orchestration / Memory / Dreaming Principles

Date of consolidation: 2026-08-10
Document under review: "Adopting the Orchestration / Memory / Dreaming Principles into the ArcaAI Runtime" (2026-08-09)
Additional input: "Brain/Hands Decoupling of the Agentic Runtime" candidate principle v0.2 (2026-08-10) - enters as ADR-0012 input per its own next-actions, mapped below where it answers findings.
Consolidator: Claude (coordinator). All rulings are the operator's; reviewer content is concurrence, challenge and recommendation only.
Status: ITEMS FOR RULING - nothing below is effective until ruled.

## 1. Panel composition and provenance notes

Four reviews received in one return (Gmail draft "arch review drafts", 2026-08-09 16:44 UTC):

- Grok - Interrogator Assessment (structural critic role, per primer).
- ChatGPT (GPT) - twelve numbered findings. NOTE: this review went untracked between 9 and 10 Aug; recorded here so the bench count is correct.
- Gemini - Strategic Architecture Alignment Analysis. Substantially concurring/synthesising in character rather than interrogating. Gemini also produced a second artefact (the structured assessment tabled 2026-08-10 with the TOR returns: principle summary, insertion map, build-plan sequencing, firebreak table). One reviewer, two passes - WS-E 36 annotation applies; the two artefacts are consistent and are treated as one concurrence.
- DeepSeek - Interrogator's Response: ten numbered findings, each with a required amendment, closing with a verbatim dissent. "Accepted in principle, but with material gaps and one fatal flaw."

Attribution correction for the record: the dissent and ten-amendment table were initially misattributed to Gemini in coordinator session notes on 2026-08-10; they are DeepSeek's. Corrected before any ruling was taken.

## 2. Convergence map

Where three or more reviewers land together (references: G=Grok challenge, P=GPT finding, D=DeepSeek finding, GM=Gemini):

- C-A. The three principles transfer; the stack supports them; the document is high-quality ADR input but NOT settled architecture. (All four. Grok verdict; P1, P12; GM alignment; DeepSeek "accepted in principle".)
- C-B. Mandate/admission machinery maturity is overstated; it is the single most important new control surface and must be specified before code. (G1; P1, P3; D4.)
- C-C. Policy fast lane is necessary and correct but currently an assertion; it must become a first-class release class with defined bounds, ownership, versioning and audit. (G6; P5; D2.)
- C-D. Two-zone Domain 1 (Frontier vs Bank-Data Training) should be adopted into ADR v0.2. (G7; P11; D3 accepts the zoning but hardens it.)
- C-E. Tenant isolation is a hard sequencing dependency and belongs as a named gate criterion preceding AWS infrastructure - and it is a correctness precondition for tenant-scoped memory, not merely infrastructure. (G2; P9; GM build-plan.)
- C-F. S16 Domain-1 rehearsal is production-critical-path: skipping it removes both the evidence base and the fine-tuning data. Its pending rulings gate the consolidator. (G4; P10; GM.)
- C-G. Firebreak verification story is the strongest section but is aspirational until the artefacts exist; "specified and verifiable in principle" must be distinguished from "presently evidenced". (G5; P12; D dissent radicalises this - see divergence V-1.)
- C-H. The standing canary is among the strongest controls proposed but needs tightening. (P7 widens scope; D7 restructures - see divergence V-2.)

## 3. Divergences requiring a chair position

- V-1. Severity of the verification gap. Grok/GPT/Gemini: viable subject to gates, staged evidencing acceptable. DeepSeek: procedural controls are not equivalent to cryptographic guarantees; without hardware-rooted attestation, transactional rollback and an independently verified canary, "the architecture is a prototype, not a production system" (dissent, verbatim). This is the consolidation's central ruling.
- V-2. Canary placement. Original design + GPT (P7): production-resident, positive live evidence of containment, scope widened to all execution routes including credential-bearing and indirect-dependency paths. DeepSeek (D7): dedicated isolated test environment, separate alerting channel, independent second-process verification, missed-report-window treated as suspected breach. These are genuinely different designs, not the same design at different strengths.

## 4. Brain/Hands v0.2 mapping (input, not reviewer)

- The credential-broker posture (isolated service, brain-only issuance, scoped TTL credentials, typed issuance/denial events, revocation, hash-pin discipline) directly serves D10 (least privilege) and part of D4 (no ambient capability at the execution layer).
- "The event stream IS the audit log" plus typed brain/hands crossings gives P4 its vehicle: the decision record can state which memory/context was actually LOADED into the session, not merely available.
- The single audited loader demanded by D10 and the platform-level refusal demanded by D4 sit naturally in the hands/loader layer of this principle.
- The seam P95 budget (placeholder-until-measured at the Domain-1 pilot) is the same evidencing discipline Grok demands in G5 applied to latency claims.

## 5. Items for ruling

Each item: consolidated finding, then RECOMMENDATION. House format - rule accept / accept as amended / decline per item.

ITEM 1 - Standing of the reviewed document. All four reviewers: treat as high-quality input to the Agentic Topology ADR (ADR-0012) and the memory-pattern DEC, not settled architecture. RECOMMENDATION: ACCEPT.

ITEM 2 - Mandate/admission machinery (C-B). Before any platform code: mandate artefact schema, versioning, revocation path, and three-way hash reconciliation specified in ADR-0012 (or a dedicated design note it references). Enforcement at PLATFORM level per D4: loader/orchestrator modules refuse any unmandated artefact regardless of caller; a MANDATE_ENFORCEMENT interpreter-startup flag failing hard when unset; CI negative test proving an unmandated artefact hard-fails. RECOMMENDATION: ACCEPT with D4's platform-level enforcement adopted in full; composition-root checks remain as defence in depth, not the enforcement point.

ITEM 3 - Attestation (V-1 core; D1). Options: (a) adopt hardware-rooted attestation now as a blocking requirement; (b) staged adoption - ADR states signed component attestation chained to a hardware root (AWS Nitro named) as the PRODUCTION requirement, landing with the AWS migration workstream; procedural controls (logs, reconciliation, canary) are explicitly labelled INTERIM evidence, never represented as equivalent; (c) decline. RECOMMENDATION: (b) staged. It concedes the dissent's substance (procedural != cryptographic; the ADR must say so on its face) without blocking all pre-AWS work on hardware that does not exist locally. The dissent is then partially discharged by ruling, with the discharge conditions named (attestation at migration; Items 11 and 12 for the other two dissent legs).

ITEM 4 - Policy fast lane (C-C). Elevate to first-class release class in ADR-0012 with, per D2 + P5: a fixed list of allowable change types; pre-approved ranges per type; automatic re-review of every fast-lane change at the next standard cadence; the bounds themselves mandated artefacts under slow governance; named owner and versioning for the bounds; audit trail distinguishing fast-lane deployments. RECOMMENDATION: ACCEPT.

ITEM 5 - Two-zone Domain 1 (C-D + D3 hardening). Adopt the Frontier / Bank-Data Training zone split into ADR v0.2, with: data minimisation applied by a separate non-AI redaction pipeline before anything crosses to the frontier zone; the redaction pipeline itself a mandated, separately audited artefact; cross-zone flows logged and subject to production-grade egress controls. RECOMMENDATION: ACCEPT.

ITEM 6 - Tenant isolation (C-E). Elevate from "named candidate action" to a formal gate criterion: tenant-isolation design precedes AWS infrastructure build, recorded in the build tracker as a gate, with the memory system's tenant-scoping named as the reason it is a correctness precondition. RECOMMENDATION: ACCEPT.

ITEM 7 - Context-window economics (G3). ADR-0012 states per-tier context size budgets and a summarisation discipline BEFORE context assembly is built; silent degradation of case content under load is named as the failure mode being excluded. RECOMMENDATION: ACCEPT.

ITEM 8 - Memory authority boundary (P2 + P3). ADR-0012 defines: who is authoritative when memory tiers conflict; staleness rules when a lower-tier artefact is newer than a higher-tier one; and states plainly that context assembly is an AUTHORISATION boundary (what an agent may see and act on), not a content loader - the ACL matrix and release-boundary semantics are designed to that standard. RECOMMENDATION: ACCEPT.

ITEM 9 - Decision-record semantics (P4). The audit record distinguishes memory LOADED into the session from memory merely available or authorised; the record establishes what context governed the decision. Vehicle: the Brain/Hands typed event stream (session assembly events). RECOMMENDATION: ACCEPT, implemented via the Brain/Hands event schema.

ITEM 10 - Admission-check failure semantics (P6). ADR-0012 specifies behaviour when: a running component's mandate is revoked mid-flight; the mandate store is unavailable (fail-closed vs degraded mode, stated explicitly). RECOMMENDATION: ACCEPT; default posture fail-closed unless the ADR argues a specific degraded mode with evidence.

ITEM 11 - Transactional rollback (D6; second dissent leg). Rollback is transactional across the release unit (model + thresholds + dependent artefacts revert together); rollback is itself a mandated, logged, auditable event; rollback targets are hash-pinned and deployable without rebuild. RECOMMENDATION: ACCEPT.

ITEM 12 - Canary design (V-2; D7 + P7; third dissent leg). Ruling needed between production-resident and isolated-environment designs. RECOMMENDATION: HYBRID - retain the production-resident canary (its value is positive evidence of LIVE containment, which an isolated environment cannot give), adopting DeepSeek's hardening in full: separate alerting channel; independent second-process verification of the canary's own logs; missed-report-window treated as suspected breach triggering incident response; PLUS the CI negative test from Item 2 covering the pre-production route, and P7's scope widening (all execution routes including credential-bearing and indirect-dependency paths). The isolation concern is met by the canary being attempt-only with no live-traffic interaction, stated in the ADR.

ITEM 13 - Consolidation cost cap (D5). ADR-0012 carries a maximum allowable cost per consolidation run per tenant and an enforcement mechanism (token budget, model-size cap, fallback to smaller model); the number is set from Domain-1 pilot measurement, held as a placeholder until measured (same discipline as the seam budget). If the pilot exceeds the bound, the task narrows before production commitment. RECOMMENDATION: ACCEPT.

ITEM 14 - Parity defined statistically (D8). ADR defines acceptable divergence per model type; a statistical parity test (e.g. bootstrap CI) runs as part of the promotion gate; parity failure rejects the promotion and logs the incident. NOTE: interacts with TOR rulings-record amendment 3 (per-scenario migration-diff comparison semantics) - one definition of statistical comparison should serve both, stated once and referenced. RECOMMENDATION: ACCEPT, with the cross-reference to the test-capability schema recorded.

ITEM 15 - Operational burden (D9). Build plan includes a minimum-viable operations manual (checklist a non-expert can follow) and a mock-bank trial measuring time-to-competence, with a stated ceiling (DeepSeek suggests 2 person-days setup) above which the architecture simplifies or automates further. RECOMMENDATION: ACCEPT - this is the turnkey thesis made testable, and it feeds the discovery-phase skills-gap quantification already owed.

ITEM 16 - Least privilege (D10). Production workloads: no outbound internet beyond the explicit allow-list; all model loading through a single audited mandate-checking loader (no direct path loads); developer workstations excluded from production data/artefacts except within the bank-data training zone under separate credentials and logging. RECOMMENDATION: ACCEPT; the Brain/Hands credential broker and hands-cannot-mint rule implement the credential half.

ITEM 17 - S16 rulings elevated (C-F). The pending S16 chair rulings are recorded as production-critical-path (evidence base + fine-tuning data for the consolidator), stated in the build tracker; Grok's recommended first act. RECOMMENDATION: ACCEPT the elevation; the rulings themselves remain a separate act for the chair.

ITEM 18 - Brain/Hands candidate principle. Rule: (a) accepted (or amended) as the structural spine of ADR-0012; (b) credential broker home - standalone DEC-0016 vs ADR-0012 section; (c) seam P95 budget measurement point confirmed as the Domain-1 pilot. RECOMMENDATION: (a) ACCEPT as spine; (b) ADR-0012 section now, promotion to DEC only if the broker's design decisions outgrow the ADR (register economy); (c) CONFIRM.

ITEM 19 - Register and sequencing. Per Grok's placement table and Gemini's build plan, unopposed: draft ADR-0012 now that consolidation is ruled (including mandate schema outline, ACL matrix, per-tier budgets, fast lane, two-zone Domain 1, and the Item 2-16 requirements above); draft the small memory-pattern DEC (DEC-0014 generalised to memory artefacts) alongside; no corpus placement yet (register first; corpus only when a later SG document is deliberately scoped to agent-memory governance); scaffold platform/memory/ and platform/consolidation/ with interfaces and fencing tests only AFTER the papers. NOTE: none of this displaces the ruled next Claude Code arc (DEC-0015 + D2.0) or the test-capability sequence; ADR-0012 takes its own session in turn. RECOMMENDATION: ACCEPT.

ITEM 20 - Dissent disposition. DeepSeek's dissent is recorded verbatim in the rulings record. Its three named requirements map to Items 3 (attestation), 11 (transactional rollback) and 12 (canary verification); the ruling on each states whether and how the dissent leg is discharged. If Item 3 is ruled staged, the record states explicitly that the dissent is PARTIALLY sustained: the interim/production distinction exists because the dissent is right that procedural and cryptographic assurance are not equivalent. RECOMMENDATION: record as stated.

## 6. Observed, not raised

- Gemini's two artefacts are consistent with each other; no contradiction requiring ruling. WS-E 36 annotation carries.
- GPT P8 (outbound controls appropriately evidence-oriented) is pure concurrence; no ruling needed.
- The reviewed document's own recommended next acts and Grok's are aligned; no sequencing dispute among reviewers.

End of consolidation. Twenty items await the chair.
