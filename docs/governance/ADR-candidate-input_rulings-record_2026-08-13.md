---
INPUT ARTEFACT — ADR-0011 input set
Source: rulings record of the 2026-08-10 consolidation session, retained on the
operator's machine; supplied from disk 2026-08-13. NEVER PREVIOUSLY COMMITTED —
parked 2026-08-10 to ride this ADR's PR, per that session's own plan. This
pinning act discharges the parking.
Status: THE OPERATIVE RECORD. Where the pinned consolidation states
RECOMMENDATIONS, this document states the RULINGS. On any divergence between
them, THIS RECORD GOVERNS.
Numbering note: "ADR-0012" in the body is STALE SELF-NUMBERING and is read as
the reserved ADR 0011 per the live register anchor of 2026-08-13; 0011 remains
RESERVED, NOT CONSUMED. ITEM 18(b)'s "standalone DEC-0016" is a 2026-08-10
CANDIDATE number and is UNRELATED to the actual DEC-0016 (test-database
separation, ruled 2026-08-12).
Pin method (ruled 2026-08-13): Circulation pin: sha256 over the complete
committed file with the single line beginning 'Circulation pin' excluded;
canonicalised as the file's raw bytes minus that line including its newline.
Fidelity pin: sha256 over the verbatim body exactly as received.
Fidelity pin (body sha256): 78b9e3d26f00a1c7b866b069c72d49dfb4619816bb2decc91ccda690e2acf4f5
Circulation pin (file sha256): a25963414ddc4bfc45e11213fb4193414f22358849731c28e242cb6dac02e327
---

# Rulings Record - Architecture Review Consolidation (Orchestration / Memory / Dreaming + Brain/Hands)

Date of rulings: 2026-08-10
Documents: "Adopting the Orchestration / Memory / Dreaming Principles into the ArcaAI Runtime" (2026-08-09); "Brain/Hands Decoupling of the Agentic Runtime" candidate principle v0.2 (2026-08-10, input).
Consolidation: PANEL_CONSOLIDATION_2026-08-10_arch-review.md (twenty items).
Ruling authority: operator (Mike). Rulings taken in five blocks, same day as consolidation. Reviewer content is concurrence, challenge and recommendation only.

## 1. Panel composition

Four reviews, one return (2026-08-09 16:44 UTC):

- Grok - Interrogator Assessment. Prior-familiarity annotation carried (multiple prior ArcaAI reviews).
- ChatGPT (GPT) - twelve findings. Untracked between 9 and 10 Aug; restored to the bench at consolidation.
- Gemini - Strategic Architecture Alignment Analysis, plus a second artefact (structured assessment tabled 2026-08-10). One reviewer, two passes (WS-E 36 class); treated as one concurrence.
- DeepSeek - Interrogator's Response: ten findings with required amendments and a verbatim closing dissent.

Coordinator correction on the record: the dissent and ten-amendment table were briefly misattributed to Gemini in session notes on 2026-08-10; corrected to DeepSeek before any ruling was taken.

## 2. Rulings

All twenty items ruled. Summary dispositions; full text of each recommendation is in the consolidation document, which these rulings adopt except where amendment is stated.

- ITEM 1 - Document standing: ACCEPT. High-quality input to ADR-0012 and the memory-pattern DEC; not settled architecture.
- ITEM 2 - Mandate/admission machinery: ACCEPT. Schema, versioning, revocation and three-way hash reconciliation specified before any platform code. Enforcement at platform level: loader/orchestrator refuse unmandated artefacts regardless of caller; MANDATE_ENFORCEMENT startup flag fails hard when unset; CI negative test proves an unmandated artefact hard-fails. Composition-root checks are defence in depth only.
- ITEM 3 - Attestation (dissent leg 1): ACCEPT AS RECOMMENDED - STAGED. The ADR states on its face that procedural controls are not equivalent to cryptographic/hardware-rooted assurance. Signed component attestation chained to a hardware root (AWS Nitro named) is the production requirement, landing with the AWS migration workstream. Until then, logs/reconciliation/canary are explicitly labelled interim evidence and are never represented as equivalent. Operator rationale: discharges the substance of the dissent without blocking pre-AWS work on hardware that does not yet exist locally; the "trust us" charge is answered by the explicit interim/production distinction.
- ITEM 4 - Policy fast lane: ACCEPT. First-class release class in ADR-0012: fixed list of allowable change types; pre-approved ranges per type; automatic re-review of every fast-lane change at the next standard cadence; bounds are mandated artefacts under slow governance; named owner and versioning; audit trail distinguishing fast-lane deployments.
- ITEM 5 - Two-zone Domain 1: ACCEPT with DeepSeek hardening. Frontier / Bank-Data Training split adopted into ADR v0.2; data minimisation by a separate non-AI redaction pipeline before any frontier-zone crossing; the pipeline is a mandated, separately audited artefact; cross-zone flows logged under production-grade egress controls.
- ITEM 6 - Tenant isolation: ACCEPT. Elevated to a formal gate criterion preceding AWS infrastructure build, recorded in the build tracker; memory's tenant-scoping named as the reason it is a correctness precondition, not merely infrastructure.
- ITEM 7 - Context-window economics: ACCEPT. Per-tier context size budgets and a summarisation discipline stated in ADR-0012 before context assembly is built; silent degradation of case content under load named as the excluded failure mode.
- ITEM 8 - Memory authority boundary: ACCEPT. ADR defines authority when tiers conflict and staleness rules when a lower-tier artefact is newer; context assembly is stated to be an authorisation boundary, not a content loader; ACL matrix and release-boundary semantics designed to that standard.
- ITEM 9 - Decision-record semantics: ACCEPT. The audit record distinguishes memory loaded into the session from memory merely available or authorised, establishing what context governed the decision. Vehicle: the Brain/Hands typed event stream (session assembly events).
- ITEM 10 - Admission-check failure semantics: ACCEPT. ADR specifies behaviour for mid-flight mandate revocation and mandate-store unavailability. Default posture fail-closed; any degraded mode must be explicitly argued in the ADR with evidence.
- ITEM 11 - Transactional rollback (dissent leg 2): ACCEPT. Rollback is transactional across the release unit; is itself a mandated, logged, auditable event; targets are hash-pinned and deployable without rebuild. Dissent leg 2 discharged.
- ITEM 12 - Canary design (dissent leg 3, divergence V-2): ACCEPT AS RECOMMENDED - HYBRID. Production-resident canary retained (positive evidence of live containment); DeepSeek hardening adopted in full (separate alerting channel; independent second-process verification of the canary's own logs; missed-report-window treated as suspected breach triggering incident response); Item 2's CI negative test covers the pre-production route; scope widened to all execution routes including credential-bearing and indirect-dependency paths (GPT P7); ADR states the canary is attempt-only with no live-traffic interaction. Dissent leg 3 discharged.
- ITEM 13 - Consolidation cost cap: ACCEPT. Maximum allowable cost per consolidation run per tenant with an enforcement mechanism (token budget, model-size cap, or fallback to smaller model); placeholder until measured at the Domain-1 pilot; if the pilot exceeds the bound, the task narrows before production commitment.
- ITEM 14 - Statistical parity: ACCEPT. Acceptable divergence defined per model type; statistical parity test (e.g. bootstrap CI) in the promotion gate; failure rejects the promotion and logs the incident. One statistical-comparison definition serves both this requirement and the test-capability schema's migration-diff semantics (TOR rulings-record amendment 3), stated once and referenced.
- ITEM 15 - Operational burden: ACCEPT. Minimum-viable operations manual (non-expert checklist) plus a mock-bank trial measuring time-to-competence; DeepSeek's 2 person-days setup adopted as the initial ceiling; above the ceiling the architecture simplifies or automates further.
- ITEM 16 - Least privilege: ACCEPT. Production workloads have no outbound internet beyond the explicit allow-list; all model loading through a single audited mandate-checking loader; developer workstations excluded from production data/artefacts except within the bank-data training zone under separate credentials and logging. The Brain/Hands credential broker and hands-cannot-mint rule implement the credential half.
- ITEM 17 - S16 rulings elevated: ACCEPT. Pending S16 chair rulings recorded as production-critical-path (evidence base and fine-tuning data for the consolidator), stated in the build tracker. The rulings themselves remain a separate act for the chair.
- ITEM 18 - Brain/Hands principle: ACCEPT AS RECOMMENDED. (a) Accepted as the structural spine of ADR-0012. (b) Credential-broker home: ADR-0012 section now; promotion to a standalone DEC only if the design decisions later outgrow the ADR (register economy). (c) Seam P95 budget measurement point confirmed as the Domain-1 pilot.
- ITEM 19 - Register and sequencing: ACCEPT. ADR-0012 drafted now that consolidation is ruled, carrying the mandate schema outline, ACL matrix, per-tier budgets, fast lane, two-zone Domain 1, and the Items 2-16 requirements; the small memory-pattern DEC drafted alongside; no corpus placement yet; platform/memory/ and platform/consolidation/ scaffolds with interfaces and fencing tests only after the papers. Explicitly: none of this displaces the already-ruled DEC-0015 + D2.0 arc; ADR-0012 takes its own session in turn.
- ITEM 20 - Dissent disposition: ACCEPT AS STATED. DeepSeek's dissent recorded verbatim below; legs mapped to Items 3, 11, 12. Because Item 3 is ruled staged, the dissent is PARTIALLY SUSTAINED: the interim/production distinction exists precisely because procedural and cryptographic assurance are not equivalent.

## 2a. Supplementary ruling - ITEM 21, canonical vocabulary for ADR-0012 (ruled 2026-08-10, same day)

RULED: the three principles take clean canonical names in ADR-0012, retiring the working terminology:

- "Agentic Orchestration" (hierarchical agentic orchestration) becomes ORCHESTRATOR-WORKER SEPARATION - execution and shared-memory proposal authority are structurally separated: workers execute; workers have read-only access to shared memory; the orchestrator is the sole proposer of shared-memory changes; proposals cannot self-apply. ("Single-Proposer Topology" is declined as the primary name: it describes one control property but loses the worker/orchestrator relationship.)
- "Contextual Memory Management" becomes TIERED VERSIONED MEMORY - shared context is held in authoritative, versioned memory tiers (PLATFORM, TENANT/PROJECT, CASE) with hash-pinning, authority semantics and explicit release boundaries. ("Governed Memory Tiers" is declined: governance is a property; tiering + versioning are the mechanism.)
- "Dreaming" becomes GOVERNED MEMORY CONSOLIDATION - memory changes are produced out-of-band from bounded evidence as proposed, validated and gated diffs (bounded transcripts, recurring-pattern evidence, proposed diff, validation, governance gate, versioned commit). Ruled the strongest rename: the metaphor is unsuitable as the formal name of a bank architecture control and misleadingly implies autonomous offline learning.

ADR-0012 title formulation ruled: "ADR-0012 - Orchestrator-Worker Separation, Tiered Versioned Memory, and Governed Memory Consolidation".

"Dreaming" is RETIRED from the formal architecture vocabulary, not retained parenthetically; it may remain in historical discussion and source notes. Historical documents (reviews, this consolidation, S16/S17 material, /dream rehearsal references) stand as written under the immutability convention; the canonical names bind from ADR-0012 forward, with this item as the mapping of record.

Drafting guidance recorded with the ruling: Orchestrator-Worker Separation (shared-memory proposal authority) and the Brain/Hands spine (execution and credential authority, Item 18) are distinct boundaries that compose - the brain is the orchestrator, hands are workers - but govern different properties (who may change shared memory vs who may act on the world). ADR-0012 states both boundaries explicitly and does not conflate them; Brain/Hands is the runtime topology implementing principle 1's authority rule together with the brokered-credential rule.

## 3. Dissent record (verbatim)

"The review concludes the firebreak is viable, but it treats human discipline and procedural controls as equivalent to cryptographic guarantees. They are not. A bank's skilled person would reject this architecture because the controls are all 'trust us' - not 'verify us'. The firebreak must be verifiable by an independent third party without access to ArcaAI's internal operations. That requires hardware-rooted attestation, transactional rollback, and a canary that is itself independently verified. Without these, the architecture is a prototype, not a production system." - DeepSeek, Interrogator's dissent, 2026-08-09.

Disposition: partially sustained per Item 20. Leg 1 (attestation) staged per Item 3; leg 2 (transactional rollback) adopted per Item 11; leg 3 (independently verified canary) adopted per Item 12.

## 4. Register consequences and citation-form note

- No register number is consumed by this record. ADR-0012 is spoken for by these rulings and is consumed at authoring under the sequence-hold rule.
- The memory-pattern DEC (Item 19) and any future broker DEC (Item 18b) take their numbers at authoring. Per the citation-form convention observed 2026-08-10 (owed to CLAUDE.md at its next revision), unconsumed register numbers are cited as "next N", never as bare "N"; the "DEC 0016" label appearing in Brain/Hands v0.2 is a hypothetical citation, not a claim, and the authored DEC takes whatever number is next when it lands.

## 5. Next acts (in ruled order)

1. The ruled next Claude Code arc stands unchanged: DEC-0015 (test-harness register home) + D2.0 commissioning frame.
2. S16 chair rulings (production-critical-path per Item 17) - separate act for the chair, before the consolidator build.
3. ADR-0012 authoring session: Brain/Hands as spine; mandate schema outline; ACL matrix; per-tier budgets; fast lane; two-zone Domain 1; the Items 2-16 requirements; broker section; interim/production attestation distinction on its face.
4. Memory-pattern DEC alongside ADR-0012.
5. Scaffolds and fencing tests only after the papers.
6. This record and the consolidation document enter docs/governance/ via a repo PR at the next appropriate session (hash-pinned transfer per house rule).

End of record. Twenty-one items ruled (twenty consolidation items plus the canonical-vocabulary ruling); dissent partially sustained and fully dispositioned.
