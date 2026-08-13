---
INPUT ARTEFACT — ADR-0011 input set
Source: operator's draft of 2026-08-10 (Gmail); the original draft is no longer
locatable in the operator's Gmail drafts as of 2026-08-13; this text was
preserved by the coordinator's read of the draft earlier on 2026-08-13 and
supplied via file. Provenance is therefore COORDINATOR-TRANSCRIBED,
OPERATOR-CONFIRMED — the operator's confirmation at the PR review is the
fidelity attestation for this input.
Fidelity-pin caveat, stated because the label would otherwise overclaim: the
fidelity pin below hashes the text AS SUPPLIED. It cannot be checked against an
original that no longer exists. It fixes this text against later drift; it does
not evidence faithfulness to the lost draft. That evidence is the operator's
confirmation, and nothing else.
Status: CANDIDATE INPUT. Ruled ACCEPTED as the structural spine of the Agentic
Topology ADR at ITEM 18(a), rulings record 2026-08-10.
Numbering correction: the body writes "ADR 0012" (with a space, not a hyphen)
as its target number. That is STALE SELF-NUMBERING. The live register anchor of
2026-08-13 reserves ADR 0011 for Agentic Topology; 0011 remains RESERVED, NOT
CONSUMED. All "ADR 0012" strings in the body are read as 0011.
Superseded question: the body's §2a leaves the credential broker's home open
(standalone DEC versus a section of the topology ADR). That question was RULED
2026-08-10 at ITEM 18(b): ADR SECTION now, with promotion to a standalone DEC
only if the broker's design decisions later outgrow the ADR (register economy).
Collision note: the body writes "DEC 0016" (with a space) as a hypothetical
home for the broker. That is a 2026-08-10 CANDIDATE number and is UNRELATED to
the actual DEC-0016 (test-database separation, ruled 2026-08-12). The rulings
record §4 confirms it was "a hypothetical citation, not a claim".
Pin method (ruled 2026-08-13): Circulation pin: sha256 over the complete
committed file with the single line beginning 'Circulation pin' excluded;
canonicalised as the file's raw bytes minus that line including its newline.
Fidelity pin: sha256 over the verbatim body exactly as received.
Fidelity pin (body sha256): 9254420e12978ef14fb56a2f7169a21eb5efba7d119b0d8b2af5f89bdcbe93ed
Circulation pin (file sha256): 7755a5076f7c03886d7279fabce8673962d2d2fb6563a0f9fccb8bc58f480161
---

ARCAAI ARCHITECTURE PRINCIPLE (CANDIDATE)
Brain/Hands Decoupling of the Agentic Runtime

Status: DRAFT v0.2 — candidate input to the Agentic Topology ADR (next in sequence: ADR 0012)
Origin: Adapted from Anthropic Managed Agents architecture (Code w/ Claude 2026 workshop, "Ship your first Managed Agent", Isabella He). Principle ported; hosting model explicitly NOT adopted — all inference and orchestration remain inside the bank's security perimeter per ArcaAI core proposition.
v0.2 (10 Aug 2026): three panel pre-answers folded in — seam latency budget (Rationale 1a), credential broker trust posture (Rationale 2a), and Next Actions resequenced to join the owed architecture-review consolidation rather than precede it.

---

STATEMENT

The agent orchestration loop ("brain") and tool/task execution ("hands") are separate services with distinct lifecycles. The brain is a durable, long-lived orchestration service that holds session state, conversation context, and the reasoning loop, but holds no execution credentials and performs no side-effecting work. Hands are execution environments (sandboxes, workers) provisioned on demand, only when a tool invocation actually requires one, receiving credentials scoped to the single task at the moment of use, and destroyed or reset afterwards.

---

RATIONALE

1. Latency. The hot path (fraud scoring, currently 33ms P99 via BentoML) never touches sandbox provisioning. Sandbox-on-demand applies only to the investigative/agentic path, where seconds of spin-up are acceptable. Decoupling keeps orchestration P95 low because the loop is not blocked by, or co-located with, heavyweight execution.

1a. Seam cost, stated honestly. The brain/hands crossing adds a hop inside the agentic path itself: event serialisation, broker round-trip, sandbox dispatch. This cost is accepted, not assumed away. A P95 budget for the seam (orchestration decision to hands execution start) is to be stated in ADR 0012 and measured at the Domain-1 pilot — placeholder until measured, not a claim. Where a tool call is trivial and stateless, the ADR may define a light-worker class that reuses a warm environment; that trade (warmth vs isolation) is a named design decision, not a default.

2. Security / credential isolation. Secrets never sit in the reasoning process. The brain requests capability; a broker injects scoped, short-lived credentials into the hands at execution time. This aligns directly with the RAT-02 governance trio (request wrapper, execution metadata, audit logging) and materially strengthens the PRA story: a compromised or misbehaving agent loop cannot exfiltrate credentials it never held.

2a. The broker is a new trust root, and is treated as one. Moving credential risk out of the loop concentrates it in the broker; the design owns that consequence rather than hiding it. Minimum posture: the broker is its own isolated service (not co-resident with brain or hands), holds a policy table mapping agent + session + tool to a scoped credential and TTL, emits a typed audit event for every issuance and denial, supports immediate revocation, and is itself subject to the same admission/hash-pin discipline as any platform artefact. The broker never accepts capability requests originating from hands — issuance requests flow from the brain only, so a compromised sandbox cannot mint its own credentials. Whether this warrants a standalone decision record (DEC 0016 candidate) or a section of ADR 0012 is for ruling at consolidation.

3. Resilience. Session state lives in the brain's durable store, not in an execution process. A crashed sandbox loses only the in-flight task, not the investigation. Sessions survive restarts; retries are an orchestration concern, not a tool concern.

4. Scalability. One orchestration service multiplexes many sessions; execution capacity scales independently and elastically with actual tool demand rather than session count.

5. Auditability. The seam between brain and hands is a natural audit boundary. Every crossing is a typed event, giving a complete, ordered record of what the agent decided versus what was actually executed — the regulatory narrative writes itself.

---

DESIGN VOCABULARY (adopted primitives)

- Agent: model + system prompt + tools/skills — the persona and capabilities. Declarative, versioned in the corpus.
- Environment: where hands run — sandbox image, packages, network egress rules. Declarative, versioned.
- Session: a running binding of agent + environment, owned by the brain, durable across execution failures.
- Event: the sole communication protocol between brain, hands, and clients (e.g. user.message, agent.tool_use, tool.result, session.status). No request/response coupling; the event stream IS the audit log.

---

IMPLICATIONS FOR ARCAAI

- B6 LangGraph agent v0 currently runs loop and tool execution in-process. This principle implies a Phase 1 refactor: extract the loop into an orchestration service; move tool execution behind a worker/sandbox interface.
- The scoring path (BentoML) is explicitly OUT of scope — it remains a synchronous, hot, non-agentic service. The firebreak between scoring and agentic paths is preserved.
- Credential broker becomes a named platform component with the trust posture at 2a (standalone DEC 0016 vs ADR 0012 section: for ruling at consolidation).
- Event schema becomes a governed artefact in the corpus (candidate B-series doc).
- Deployment remains entirely within the bank's perimeter: brain, hands, and inference (Llama 3.1 8B or successor) are all bank-hosted. External managed-agent platforms are a reference architecture, not a dependency.

RELATIONSHIP TO STANDING PRINCIPLES

- Complements hierarchical agentic orchestration (the brain is the natural home of the hierarchy).
- Complements contextual memory management and the dreaming/consolidation loop (durable session state in the brain is the substrate both operate on).
- Does not reopen the parked separation/firebreak complex; the scoring/agentic firebreak stated above is the existing ADR-0009 platform/vertical boundary applied, not a new ruling.

NEXT ACTIONS (resequenced v0.2 — respects the ruled queue and the one-arc rule)

1. This principle enters the ADR 0012 input set. It does NOT take its own governance session: panel review happens as part of the owed architecture-review consolidation (Grok interrogation + Gemini assessment of the orchestration/memory/dreaming document, recorded as owed in PR #83), which must complete before ADR 0012 opens. This document circulates with that consolidation pack.
2. Nothing here displaces the ruled next arc (DEC-0015 + D2.0 commissioning frame) or the test-capability sequence; ADR 0012 work follows in its own turn.
3. At consolidation, rule: (a) accept/amend this principle as ADR 0012's structural spine; (b) broker as DEC 0016 vs ADR 0012 section; (c) the seam latency budget's measurement point (Domain-1 pilot per S17-F).
