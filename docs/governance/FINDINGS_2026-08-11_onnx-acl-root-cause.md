# Findings — ONNX cache ACL fault: root cause, and what it constrains

Authored 2026-08-11. Record of a diagnosis, not a governed decision: nothing here
rules anything and no register number is claimed by this note. The implementing
artefact for the pre-flight remains at D2.2a, where its CL number is claimed.

Occasioned by the pre-flight precondition attached to the operator's conditional
ruling on `docs/governance/D2.0_COMMISSIONING_FRAME_2026-08-11.md`. The fault had
stood parked in the `CLAUDE.md` queue across several arcs as two separate items — an
ONNX cache ACL fault and an elevated-harness-shell breach. This note records that
they are one incident, cause and effect, and states the design constraints the
diagnosis places on the D2.2a pre-flight artefact.

Methods below are described in prose. This record carries no live reproductions.

## 1. Causal chain

The chromadb pinned embedding function stores its model under a per-model cache
directory in the user profile, holding the downloaded archive `onnx.tar.gz` alongside
an `onnx` directory extracted from it. `arcaai/platform/retrieval/chroma_store.py`
warms that function at adapter construction, so any live retrieval act must read the
extracted directory.

The extraction was performed by an elevated process. The consequences were asymmetric
and that asymmetry is the whole finding:

- The **parent** cache directory was left owned by `BUILTIN\Administrators`, but
  carried an explicit access entry granting the normal user full control. It listed
  and traversed normally.
- The **extracted child** directory received an administrators-only discretionary
  access list with no entry for the normal user and no effective inheritance. Under
  the normal identity it denied not merely read but the reading of its own security
  descriptor — an attempt to retrieve its access list failed with the exact text
  `Attempted to perform an unauthorized operation.`, and traversal failed as
  `UnauthorizedAccessException`.

So the parent listed the child's name while the child denied everything about itself.
Any check that stopped at listing the parent would see a well-formed cache.

The same elevated interlude created the corpus index directory used by
`scripts/b7_run.py`, two seconds after the archive, and left it owned by
`BUILTIN\Administrators` as well. That directory remained usable only because its
inherited access list grants `Authenticated Users` modify rights. Same cause,
different blast radius: one artefact was bricked for the normal user, the other kept
working, so nothing failed loudly enough to be noticed.

Repair was by deletion of the extracted directory from an elevated terminal by the
operator, followed by re-extraction triggered from the ordinary harness shell. The
re-extraction was local: the archive's size, modification time and SHA256 were
identical before and after, so no network fetch replaced it. The re-created directory
is owned by the normal user, and access flows through an `OWNER RIGHTS` entry rather
than a named user entry — which means access here is contingent on ownership not
changing, and a future ownership change would silently reintroduce the fault.

## 2. The false-green mechanism

An elevated process bypasses the discretionary access list that caused this fault.
The traversal check therefore returned green exactly when it was run under the
condition that created the fault, and red only under the condition in which the
system is actually used. The check did not merely fail to detect the fault; its
green was strongest precisely where it was least meaningful.

This is the failure class WS-E 63 records — a green read as meaning something it
cannot mean — and it is the reason TOR Section 5A's Regime 1 bars commissioning
results from ever becoming gate evidence.

Two further instances of the family were live in the queue when this note was
written: the lint invocation that exits zero without running the linter, and
`scripts/corpus_edges_check.py` reporting that authored-document checks pass when no
authored document was read. A check whose success message claims more than it
verified is the recurring shape, not an accident of any one check.

## 3. Corroborated-elevation method

Non-elevation must be established by two independent methods that agree, because a
single method silently degraded during this diagnosis.

The first method evaluates whether the current security principal holds the
built-in administrator role. The second reads the process token's mandatory
integrity label, expecting the medium level, and separately confirms that the
administrators group appears in the token marked for deny only — the signature of a
filtered token under User Account Control.

The degradation worth recording: an initial attempt to read the integrity label by
filtering the token's groups for the integrity SID range returned an empty string
rather than an error. Had that been the only method, the assertion would have
produced neither a green nor a red but a blank, and a check written to compare
against an expected value would have treated the blank as a mismatch or, worse, as
absence of a problem. The second method was introduced for exactly that reason and
returned an unambiguous medium integrity level.

## 4. Design constraint for the D2.2a pre-flight artefact: red is not the opposite of green

The pre-flight must distinguish **three** outcomes per assertion, not two:

- **GREEN** — the assertion was evaluated and positively evidenced.
- **RED** — the assertion was evaluated and positively falsified.
- **UNKNOWN** — the assertion could not be evaluated.

UNKNOWN must exit non-zero and must never be reported as, or collapse into, green.
Every false green catalogued above is an UNKNOWN that was rendered as a GREEN.

Two structural rules follow:

1. **Assertion ordering is load-bearing.** Non-elevation must be asserted first, and
   if it fails the artefact must refuse to report on the remaining assertions at all
   rather than report them as passing. Cache traversal, service availability and
   environment identity are all read through the token whose privilege level
   assertion one establishes; evaluated under an elevated token their results are not
   merely unreliable, they are meaningless.
2. **A check must evidence what it claims, and claim only what it evidenced.** The
   success message must name the assertions actually evaluated. Where an assertion
   was skipped, the artefact says so and exits non-zero.

## 5. Check-method defect: exit codes and unreachable handlers

Two method defects were observed this session, both of which would silently weaken
the pre-flight if carried into it.

**Unreachable failure handler around a native command.** The service-availability
check was first written wrapping the container-listing command in a structured
exception handler. Native executables in this shell do not raise terminating errors
on failure; they write to the error stream and set an exit code. The handler is
therefore unreachable for the failure it was written to catch. There is no exception
text to record for it, and that absence *is* the defect: had the container runtime
been down, no exception would have been raised, the handler would not have fired, and
the check would have fallen through with nothing to report — an UNKNOWN presented as
a pass. The corrected method inspects the exit code explicitly, and was used for the
re-verification recorded here.

**Exit codes from early-terminated pipelines.** A git invocation whose output was
piped into a first-item selector returned exit status 255 while succeeding
completely, because closing the pipe early causes the command to fail on a broken
pipe. Read literally, a non-zero exit would have been recorded as a failed act that
in fact fully succeeded.

Together these bound the rule already recorded in the queue for the lint defect: an
exit code alone evidences neither success nor failure. The pre-flight must assert on
the substance of what a check returns, and where it does rely on an exit code it must
invoke the command in a form that lets the exit code mean what it appears to mean.

## 6. Vector-store persistence gap

The commissioning frame's entry criteria require service availability for the vector
store. The store is a local persistent directory resolved from a constant in
`scripts/b7_run.py`, not a network service, and it is deliberately outside version
control — so it is absent from a fresh checkout and cannot be assumed present.

The gap is that availability for this store is not a reachability question. Three
distinct conditions must hold and each fails differently: the directory must exist;
its database must be readable; and it must be **writable**, because the underlying
database engine requires write access to serve reads. A check that confirms only
existence, or only readability, reports green on a store that will fail at the first
query. All three were evidenced during this diagnosis, and the pre-flight artefact
must evidence all three rather than inheriting a reachability idiom from the
container and database checks.

A related latent hazard is recorded rather than repaired: this directory is still
owned by `BUILTIN\Administrators` from the same elevated interlude, and remains
usable to the normal identity only through an inherited grant to authenticated users.
It is not currently faulty and is not repaired here.

## 7. Standing rule recorded

The harness never elevates. Any repair requiring elevation is the operator's, at
their own terminal, and the assertion it repairs is re-verified afterwards from a
non-elevated shell — because, per section 2, a verification run under elevation
cannot evidence the condition it claims to establish.

End of findings.
