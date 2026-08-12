---
name: check-method
description: How to write and report checks, gates, verification steps, and success/failure lines in ArcaAI. Consult this skill whenever writing a script that verifies anything, reporting the result of a check or gate, wording a "success" or "PASS" line, handling a failed check, or recording a defect. Also applies to CI step summaries, pre-flight artefacts, and gate review evidence. If a message is about to claim something "worked", "passed", or "is green", this skill governs how that claim is worded.
---

# Check Method Family

Standing rules (ruled by Mike; six recorded instances in the check-method
family; provenance: WS-E register and D2.2a pre-flight root-cause finding).

## Rule 1 — The success line states what it actually checked

A success line is a claim of evidence, not a mood. It must name the concrete
condition that was evaluated, so a reader can judge whether the check proves
what the gate needs.

Bad:  `Setup complete ✔`
Bad:  `All good — corpus verified`
Good: `PASS: manifest hash a3f9…e2 matches committed manifest (54 entries compared)`
Good: `PASS: bentoml serve responded 200 on /healthz within 5s from non-elevated shell`

If the script only checked that a file exists, the line says the file exists.
It does not say the file is *valid*, *loaded*, or *working* — those are
different checks and must be run to be claimed.

## Rule 2 — Three failure modes, always distinguished

Every check must be able to report which of these occurred, because they demand
different responses:

1. **Condition false** — the check ran, evaluated cleanly, and the condition
   is genuinely not met. This is a real red. Respond by fixing the condition.
2. **Check could not evaluate** — the check itself failed to run (missing
   dependency, unreachable service, permission error). This is *not* evidence
   the condition is false. Respond by repairing the check's preconditions,
   then re-running. Never report this as a plain FAIL of the condition.
3. **False-red** — the check ran but its logic is wrong, flagging a met
   condition as unmet. Suspect this when the red contradicts direct
   observation. Respond by fixing the check, recording the defect, and
   re-running.

A check whose failure output cannot distinguish mode 1 from mode 2 is itself
defective and should be reworked before its results are relied upon.

## Rule 3 — Defects are recorded as prose descriptions, never live reproductions

When recording a defect (in WS-E, a CL entry, a PR description, or a session
note), describe it in prose: what was expected, what occurred, under what
conditions, and the distinguishing evidence. Do **not** embed the failing
command, payload, or input in a form that could be executed or that
re-triggers the fault when the document is processed. Registers are records,
not fixtures.

## Rule 4 — Verify the actual artefact, never the report about it

Ruled into working practices 11 Aug 2026 after a week in which every caught
error shared one cause: trusting a summary, write-up, or related prompt
instead of reading the committed text or running the specified test. A
verification claim must name the exact test that ran and the exact artefact
inspected. "Saw something that looks like it" is not evidence. This applies
to humans and agents equally — it caught its own author within hours of
being adopted.

## Rule 5 — Green is only green under representative conditions

A check passed under elevation, under the commissioning regime, or with
non-production credentials is reported with that qualifier attached, and does
not satisfy a Formal Execution gate (see D2.0 two-regime model:
commissioning results are permanently inadmissible).
