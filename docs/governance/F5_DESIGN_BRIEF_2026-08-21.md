# F5 design brief — the envelope-guard structural artefact

**Status: DESIGN BRIEF. This feeds a DEC; it is not one.** No register number is
consumed by this document — no DEC, ADR, CL or WS-E item is claimed, and none is
needed for a brief to stand. Where the ruled record already answers a design
question this document transcribes and cites it; where the record is silent the
gap is marked **OPEN** rather than filled with the author's judgement. Section 8
consolidates every OPEN gap in one list.

**Authority.** Chair ruling R-b of 21 August 2026, recorded at CL-31, which
parked the settings-side `permissions.deny` proposal **into this brief rather
than striking it**. The mechanism this brief designs is specified at
`docs/governance/DEC-0018_A6_CORRECTION_2026-08-19.md` section 3(c) as an
"F5-class amendment", and the build is carried at `CLAUDE.md` queue item 48.

**Authored under PROMPT 139, lane T2**, per the interim practice that every
record states the prompt numbers it consumed. The envelope carried amendments
A–C; pre-step A was discharged earlier in the same session (lane fast-forwarded
`d2203e5..f5709eb`, FF-only held, HEAD and CL anchor verified).

**Sources read this session**, each cited in place: `DECISIONS.md` DEC-0018 and
its 2026-08-21 amendment note, DEC-0019 and its operational-status note;
`docs/governance/DEC-0018_A6_CORRECTION_2026-08-19.md`;
`docs/governance/DEC-0018_RIDER_R1_2026-08-19.md`;
`docs/governance/FINDINGS_2026-08-17_guard-bypass-ADDENDUM_fix-spec.md`;
`docs/governance/PRECEDENCE_DISCRIMINATOR_OUTCOME_2026-08-14.md`;
`docs/governance/GROUP1_FAILURE_route-a-bypass_2026-08-14.md`;
`docs/governance/WS-E_INCIDENTS.md` items 72, 73, 74, 75, 76 and 77;
`docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` CL-31;
`docs/governance/QUEUE_CYCLE_2026-08-21.md`; the guard hook implementation and
the settings file, both **read only**; `scripts/queue_driver.py`.

---

## 1. Problem statement

### 1.1 The question F5 exists to answer

**Inside a valid envelope, how does an ask-tier guard action resolve, without
buying permission at the cost of the observation that made it acceptable?**

Rider R1's amendment A2 states the behaviour wanted, verbatim from
`docs/governance/DEC-0018_RIDER_R1_2026-08-19.md`:

> "(b) ASK tier: within a valid, in-scope envelope, ask-tier actions resolve to
> ALLOW-AND-LOG. The guard does not halt for chair input; it records the row
> (action, tier, envelope ID, timestamp, resolution=ENVELOPE-ALLOW) to the
> ask-tier log."

The reason this is not merely a configuration change is recorded at section 3(c)
of the correction file, and it is the whole of the design constraint:

> "**Layered with the hook, never alternative to it.** That phrasing is the whole
> correction. The drafted mechanism sat *beside* the guard and pre-empted it; the
> corrected one sits *inside* it, so the component that grants is the component
> that records, and no call is permitted by a path that cannot observe it."

### 1.2 Why the guard is the only component positioned to observe

Read from the hook module this session. Its `main()` is the single dispatcher and
its `respond()` the single decision emitter; the `PreToolUse` matcher in the
settings file routes six tools to it — `Bash`, `PowerShell`, `Edit`, `Write`,
`MultiEdit` and `NotebookEdit`. Every gated call in the repository passes through
that one function. Nothing else in the tree sees a tool call before it runs.

That is a **positional** fact rather than a design preference, and it is why the
settings-side allow route was struck: a settings allow rule permits by
pre-empting the hook, and the hook is the only thing that could have written the
row.

### 1.3 What was struck, verbatim, and why it matters here

From the correction file, section 3(a), quoting the settings file's own standing
constraint:

> "(1) A Tier 1 allow rule PRE-EMPTS a Tier 2 guard ask (tested 2026-08-11). The
> two are alternatives, not layers, so never grant here anything the governance
> guard is relied on to gate."

And the consequence drawn there:

> "**Consequence, and it is fatal to the drafted mechanism.** A2's ALLOW-AND-LOG
> requires a call to be permitted *and* observed. A settings allow rule permits by
> pre-empting the guard, which is the only component positioned to log. The
> widening would therefore purchase permission at the exact cost of the
> observation that made it acceptable. **A settings.json widening is struck as the
> mechanism for A2.**"

**This brief inherits that as settled.** No option below reaches ALLOW-AND-LOG by
a settings allow rule, and the question is not reopened.

### 1.4 What F5 must achieve that F1–F4 do not

F1 through F4 were **corrective**: they fixed *what the guard matches*. The fix
spec states F1 and F2 in those terms —

> "**F1 — anchor deny patterns on the subcommand, not on `git <subcommand>`.**
> Match the subcommand **anywhere in the argument vector** rather than immediately
> after the executable."

> "**F2 — stop treating `2>&1` as a write construct.** The `>` inside a stream
> redirection writes no file."

— and F3/F4 closed the long-form branch-deletion ask and the intervening-flags
gap at WS-E 74. All four made an existing decision path see calls it was already
supposed to see. **None of them changed what happens to a call once matched, and
none of them added a record.**

F5 is **constructive**, and it asks for two things the module does not do today.

**(a) A response class the module has never emitted.** The module returns deny or
ask, or falls through to a silent `sys.exit(0)`. Its own comment on the
never-silent set says so and relies on it: the two overlapping responses there are
safe "precisely because this module returns deny or ask and never allow — unlike
the Tier 1 allow versus Tier 2 ask pairing, where the overlap switches the gate
off." `ENVELOPE-ALLOW` is therefore a **new response class**, not a re-labelling
of an existing one. Two implementations are available and they are not equivalent:
emit `permissionDecision: "allow"` explicitly, or fall through to the silent exit.
The silent exit is indistinguishable, from the executor's side, from no rule having
matched at all — which reproduces inside the guard the exact evidential problem the
invariant at section 3 exists to prevent. **OPEN-1: whether the harness honours an
explicit `"allow"` from a `PreToolUse` hook is established nowhere in this
repository.** The module has never emitted one, so no observation of the harness's
response to it exists here.

**(b) A log sink that does not exist.** Read this session: the module imports
`json`, `pathlib`, `re`, `subprocess` and `sys`. There is **no logging import, no
file opened for writing, and no write call anywhere in it**. `subprocess.run`
appears exactly twice — once to read pull-request state through `gh`, once to read
the branch through `git rev-parse` — and both are reads. The module's only outputs
are one JSON object printed to stdout and an exit status.

**So A2's "with the guard itself writing the log row" is a new capability, not a
re-wiring of an existing one.** That is the single most consequential fact this
brief carries into the design, because it converts F5 from a patch into a component
with its own durability, concurrency and failure semantics — and it must be built
inside a file that carries an absolute in-session deny, so every iteration costs an
operator install and a session restart.

### 1.5 The route is fixed by the deny, not by preference

From the correction file, section 3(c):

> "**This amendment is owed as its own governed act and is not started here.** It
> is a `.claude/hooks/` change, which is drafted outside the tree, installed by the
> operator at their own terminal, then branch, PR, merge — the F1 to F4 route. A
> design brief, panel-reviewable, then a chair ruling, then install."

The guard's own comment states the cost in the same terms: there is no in-session
route to those paths "INCLUDING the route that would repair a defect in this guard,
or roll back this very deny." **Design iterations are expensive by construction.**
That argues for settling the questions at section 6 on paper before the first
install, and it is why this brief exists at all.

---

## 2. Parked item 2, absorbed — the settings-side `permissions.deny` proposal

**Framed as a design option under evaluation. No recommendation is attached**,
because a recommendation here would function as the decision CL-31 parked.

### 2.1 The disposition, verbatim from CL-31

> "**Item 2** (settings-side `permissions.deny`) is **PARKED into the F5 design
> brief, not struck**: there is **no DEC-0018 conflict**, the struck mechanism
> having been the *allow* half, but it is blocked on (i) deny-versus-hook firing
> order being unprovable from inside the harness and (ii) **observability
> polarity** — a deny firing before `PreToolUse` may widen the WS-E 75 gap.
> Revisit in F5 with an externally designed probe."

CL-31 also fixes the item's scope: "no `.claude/settings.json` change was made
under this item or is authorised by it."

### 2.2 The clean polarity argument, stated at its strongest

**A deny only ever refuses.** The objection that killed the allow half — that a
settings rule pre-empts the component relied on to gate — cannot apply in the same
form, because pre-empting a gate with a *refusal* leaves the call refused. Where an
allow rule that pre-empts the guard converts a gate into a pass, a deny rule that
pre-empts the guard converts a gate into a stop. The failure direction is toward
refusal, which is the safe direction, and it is the same direction the register has
repeatedly accepted as the tolerable one: WS-E 73 and WS-E 76 are both **false-RED**
findings, obstructive rather than permissive, and both were recorded as safer for it.

The settings file's own second constraint bars allow-listing a family carrying a
deny; it says nothing against *adding* a deny, and there is no rule in the tree
against layering two refusals. The guard's never-silent comment makes the general
point directly: two overlapping **restrictions** are safe to carry together in a way
that a restriction overlapping a permission is not.

### 2.3 One fact from the read that the proposal must start from

**The settings file has no `permissions.deny` key today.** Its `permissions` object
contains `allow` and nothing else. This would therefore be a new key rather than an
edit to an existing list — which matters for the probe design at section 4, because
there is no existing deny behaviour in this repository to reason from, and none has
ever been observed.

### 2.4 Blocker (i) — firing order is unprovable from inside the harness

The internal probe that produced the UNPROVABLE finding is recorded in the settings
file's own Amendment 2, verbatim:

> "The probe series RAN and returned UNPROVABLE, not proven: adding a matching allow
> rule for a denied command, probing, and removing it produced an IDENTICAL refusal
> in all three states. Two hypotheses fit equally - deny beats allow, or
> settings.json does not reload mid-session - and they cannot be separated from
> inside the harness, because the discriminator is whether a PROMPT fired and
> prompts are not observable here."

**A distinction that must not be collapsed, because the two questions look alike and
only one is settled.** The 2026-08-14 discriminator, run at the operator's terminal,
settled **allow-versus-hook-deny** — branch A, DENY WINS — and that outcome is
recorded with its own limits at
`docs/governance/PRECEDENCE_DISCRIMINATOR_OUTCOME_2026-08-14.md`. It says nothing
about **settings-deny-versus-hook**, which is a different pair, on a key that does
not yet exist in the file. Reading the 2026-08-14 proof as covering it would be the
overreach that outcome's own section 6 warns against: "Record this as branch A
specifically, not as 'the guard held'."

### 2.5 Blocker (ii) — observability polarity, and why it is the sharper of the two

If a settings deny fires **before** `PreToolUse`, the hook is never invoked. The
guard's refusal text — which is what makes a deny self-evidencing today, returning
into the transcript where the executor can read it — never appears. What the executor
sees instead is unknown, and may be nothing distinguishable.

**That is the WS-E 69 failure shape arriving from the opposite direction.** The
never-silent set was upgraded from ask to deny precisely because an ask's absence
evidenced nothing:

> "An ask that a MODE can satisfy is a gate whose green is indistinguishable from its
> never having been put - the check-method family."

A settings deny that silences the guard would buy the same kind of unobservable
enforcement, this time on the refusal side. The refusal would still *happen* — which
is why this is a weaker objection than the one that struck the allow half — but the
*record* of it would move outside the component that produces the repository's
evidence. Whether it lands anywhere readable is **OPEN-2** and is exactly what the
probe at section 4 is for.

### 2.6 What the option would and would not buy

**Would buy:** enforcement that does not depend on the hook being invoked at all —
which is the one property the render-route hole makes valuable. At
`docs/governance/GROUP1_FAILURE_route-a-bypass_2026-08-14.md` a skill render line
executed a command carrying an absolute deny "and returned git's own error rather
than the guard's refusal, with no prompt and no deny", the guard never invoked. The
settings file's Amendment 4 records why the rollback did not close it: "allow rules
only ever permit, never block, so removing them does not constrain a render that
bypasses the guard entirely." **A settings deny is the only candidate in this brief
that could bind a path the hook never sees.**

**Would not buy:** anything toward ALLOW-AND-LOG. A deny cannot permit and cannot
log. Item 2 and F5's ask-tier resolution are therefore **complements, not
alternatives** — a point worth stating plainly, because parking item 2 "into" this
brief could be misread as making it a candidate answer to the same question.

---

## 3. The observability invariant — proposed governing standard

**Proposed, for the chair to adopt or reject as the standard against which F5
options are judged:**

> **Every permitted call is observed by the component that permits it, and every
> refusal is observable somewhere.**

### 3.1 Derivation

The first half is a direct generalisation of the correction's own sentence — "the
component that grants is the component that records, and no call is permitted by a
path that cannot observe it." The second half is the register's settled position on
refusals, from the guard's never-silent comment: deny is chosen over ask because it
is "the only response this hook returns that no mode and no approval overrides", and
because a refusal that cannot be observed is not evidence of anything.

### 3.2 Why both halves are needed

A standard carrying only the first half would admit the settings-deny option
unexamined, because a deny permits nothing and so trivially satisfies a rule about
permission. The second half is what makes blocker (ii) a design question rather than
a footnote. Conversely a standard carrying only the second half would admit the
struck allow-widening, which refuses nothing.

### 3.3 The invariant's stated limit — it is about records, not about eyes

WS-E 75 is untouched by any arrangement of this kind, and the brief says so rather
than letting a reader infer otherwise. Verbatim:

> "**Reach.** This bears on every future ASK-class rule, not only on the rows that
> raised it. Any control whose enforcement is an ask inherits the limit, so **an ask
> may never be cited as evidence that a human was consulted** — only that the guard
> classified the call as one a human should see."

The method upgrade recorded at the WS-E 74 discharge narrows the gap without closing
it: guard-side emission is now evidenced by feeding commands to `main()` as a stdin
`PreToolUse` payload, and routing is evidenced by live deny rows, so "everything
upstream of the eye is now evidenced" and "what remains open is **only the final
human-surfacing link**."

**The invariant is satisfiable; WS-E 75 is not closed by satisfying it.** A2.2's
claim that ask-tier resolution "directly discharges the observability concern in
WS-E 75 for the in-envelope case" holds only in the narrow sense that an
envelope-allowed row becomes a reviewed record instead of an unobserved click — and
Rider R1's own in-tree preamble already qualifies it: the claim "holds only under the
corrected mechanism, and WS-E 75's general limit — that human surfacing of an ask is
not provable by any probe — is untouched either way."

---

## 4. External probe design — design only, not execution

**Nothing in this section is executed by this brief.** The envelope grants no probe
execution, and the probe itself requires acts no executor session can perform.

### 4.1 The question, stated so it cannot drift

**When a settings-level `permissions.deny` rule and a `PreToolUse` hook both match
one call, is the hook invoked, and which response reaches the executor?**

Three outcomes are possible and all three must be distinguishable: hook invoked and
its refusal returned; hook invoked but the settings deny's response returned; hook
not invoked at all.

### 4.2 Why the internal probe could not settle it

Restated from section 2.4: the internal probe's three states produced an identical
refusal, and the discriminator — whether a prompt fired — is not observable from
inside the harness. The 2026-08-14 run escaped that by moving the observer: an
operator at their own unhooked terminal watched for the prompt. That works for
allow-versus-deny because a prompt is the discriminator there. **It does not work
here**, because the settings-deny question's discriminator is whether the hook *ran*,
and a human watching a terminal cannot see that either.

### 4.3 The instrument — a witness the hook writes

Since the hook currently writes nothing, the probe needs a build of it that does:
before any decision, the guard appends a **witness row** — timestamp, tool name, and
a hash of the command string — to a file outside the repository. The witness is the
whole instrument: **its presence proves the hook ran; its absence proves it did
not.**

This is deliberately the same capability F5 needs anyway (section 1.4b), so the probe
build is a prototype of the real thing rather than throwaway scaffolding — which is
an argument for sequencing the probe *with* the first F5 design increment rather than
before it.

### 4.4 Probe rows and what each outcome proves

| Row | Command shape | Settings deny | Hook rule | What a witness present proves | What a witness absent proves |
|---|---|---|---|---|---|
| P1 | matches settings deny only | yes | none | hook is invoked even when a settings deny matches — the two are layered | settings deny pre-empts the hook entirely |
| P2 | matches hook deny only | no | deny | control: witness works and the hook runs — expect the guard's refusal text verbatim | the witness or the wiring is broken; the whole run is void |
| P3 | matches both | yes | deny | firing order readable from which refusal text returns | settings deny pre-empts; the hook's refusal is unreachable for this family |
| P4 | matches neither | no | none | control: the hook runs on every routed call, so absence elsewhere is meaningful | the hook is not routed at all; P1 and P3 absences prove nothing |

**P2 and P4 are not optional.** Without P4 an absent witness at P1 is ambiguous
between "settings deny pre-empted the hook" and "the hook never runs on anything",
and the register's standing pairing rule — a deny-shaped probe returning the guard's
own refusal text verbatim, paired with an allow-shaped call that succeeds — exists
for exactly that reason.

### 4.5 Pass conditions are stated per tier, never per table

Carried from the check-method family's 2026-08-19 instance: *"probe-spec expectations
are stated PER TIER, never per table, because one pass condition cannot serve two
response classes whose observable signatures are opposite."* Here the rows differ in
response class, so:

- **Deny rows (P2, P3):** the guard's own refusal text, returned verbatim. Git's own
  error is a **bypass** result, not a pass.
- **Control row (P4):** the command executes normally **and** a witness row exists.
- **Row P1:** there is no expected refusal text at all, and the *only* reading is the
  witness. Applying the deny-row expectation to P1 would fail a correct run.

### 4.6 What execution would require

1. **An operator act at their own terminal.** The probe build is a `.claude/hooks/`
   change carrying an absolute in-session deny, drafted outside the tree and installed
   by the operator — the F1-to-F4 route.
2. **A fresh session, not a mid-session edit.** The 2026-08-14 outcome records why:
   the restart "replaces the 2026-08-13 probe's unevidenced assumption (that
   `settings.json` reloads mid-session) with the documented mechanism (that it loads at
   session start)", and states plainly that this "is still an inference about load
   rather than an observation of it."
3. **Main-loop issuance only.** Every probe command must be issued through the ordinary
   tool path. A probe run through a skill render would reproduce the GROUP1 failure and
   return a false "settings deny pre-empts the hook" reading, because on that route the
   hook is not invoked for reasons that have nothing to do with settings. **This
   constraint belongs in the procedure file, not in a reader's memory.**
4. **Removal with the 2026-08-14 evidence discipline:** re-read of the file as primary
   evidence, empty `git diff --stat` as corroboration, in that order, "an empty diff
   cannot distinguish a removal from an edit that never landed."

### 4.7 What the probe does not settle

It settles firing order and hook invocation. **It settles nothing about human
surfacing** — the witness proves the hook ran, never that a prompt reached a person.
WS-E 75 stands after this probe exactly as before it, and any ruling that cites the
probe should say so.

---

## 5. Option space

Assessed against the section 3 invariant. **No option is recommended.**

### (a) Hook-only — extend the guard

Ask-tier envelope resolution inside `.claude/hooks/governance_guard.py`: consult an
envelope manifest naming the active envelope's scope, resolve an in-envelope ask-tier
call to allow-and-log, and write the row from the guard itself. This is the mechanism
DEC-0018 A6 as corrected already specifies.

- **Observability posture:** satisfies both halves of the invariant by construction —
  the granting component is the recording component, and refusals keep the guard's
  existing self-evidencing refusal text.
- **Provability:** strong, and by an instrument already exercised. Ask-class rows were
  closed at PROMPT 141 by feeding commands to `main()` as a stdin `PreToolUse` payload
  and reading its JSON answer — "the harness's own interface, exercising `main()` and
  its real dispatch order rather than a reimplementation assembled from the module's
  constants." Envelope resolution is testable the same way, without an install per
  iteration.
- **Failure modes:** (i) the new-response-class problem at OPEN-1; (ii) manifest
  freshness — an envelope manifest editable while a run is in flight is a widening
  wearing a different name, and queue item 48 already names this as a design question;
  (iii) log durability and append-only-ness are now the guard's problem, on a path that
  must not wedge the session — the module today deliberately exits 0 on a malformed
  payload rather than fail closed, and a write failure needs a stated policy; (iv) every
  fix costs an operator install and a restart.
- **Closes of WS-E 75:** the in-envelope case becomes a reviewed record; the final
  human-surfacing link is untouched. **Of WS-E 76:** nothing. The write-detection defect
  is orthogonal and stays open.

### (b) Settings deny layered under the hook, conditional on the probe

Item 2 as parked, admitted only if section 4's probe returns "hook is invoked" — that
is, P1 with a witness present.

- **Observability posture:** first half satisfied vacuously (it permits nothing).
  Second half **unknown until probed** — this is blocker (ii) and OPEN-2.
- **Provability:** currently nil from inside the harness; conditional on an external
  probe that has not been designed into a procedure file, let alone run.
- **Failure modes:** if the deny fires first, enforcement becomes silent and the
  repository loses the refusal text it uses as evidence; the settings file is itself a
  never-silent path, so every iteration is an operator install; and a deny list is a
  second enforcement surface that can drift from the guard's patterns — the WS-E 64
  shape, where two half-wired parts each looked complete.
- **Closes of WS-E 75:** nothing; a deny is not an ask. **Of WS-E 76:** nothing.
- **Unique value, and it is real:** the only option here that could bind the
  render-route path the hook never sees.

### (c) Hooks-as-F5 proper — the parked implementation route from the original uplift brief

**OPEN-3: this option's source document is not in the repository and could not be
read.** A repository-wide search this session for "uplift brief", "hooks-as-F5" and
"F5 proper" returned nothing, and CL-31 records that the uplift brief's skeleton was
"discarded as superseded by the live file". The option is therefore listed **by name
only, as the envelope names it**, and is not characterised further. Assessing it
against the invariant would require inventing its content, which is precisely what
this brief is instructed not to do. It is a live instance of the queue item 34 M2 gap:
a decision option whose text sits outside the evidence perimeter.

### (d1) Server-side enforcement — M3 branch protection

Already partly in force and cited in the settings file's own record: "M3 branch
protection blocks main pushes server-side (PR required, non-fast-forward blocked,
empty bypass list), so a stray main-push fails at GitHub rather than at a prompt."

- **Observability posture:** strong on the refusal half — a server-side rejection is
  recorded outside the executor's machine entirely. Silent on the permission half; it
  logs nothing about permitted in-envelope acts.
- **Provability:** the strongest of any option, being independent of harness internals.
- **Failure modes:** covers only what a git server can see. It cannot reach file writes,
  shell commands or ceremony paths, so it is not a candidate answer to A2.
- **Why it belongs in the option space anyway:** WS-E 75's disposition routes the
  ask-tier gap to queue item 34's M-family, and M3 is named there as the natural home
  because "a platform-level control does not depend on a prompt reaching anyone."
  **Any F5 ruling should say which obligations it is deliberately leaving to M3**
  rather than leaving the division implicit.

### (d2) The null option — keep ask-tier halts

Recorded because it must be evaluated rather than assumed away. A2's own rationale
states the cost: "as written the chair would still be pinged on every ask-tier row,
defeating the stated intent." Against that, the null option changes nothing and risks
nothing, and it is the only option with zero install cost.

- **Observability posture:** satisfies the invariant trivially and provides no record —
  an ask leaves nothing behind, which is WS-E 75's complaint about it.
- **Failure mode:** unattended operation is not reachable, and the 60-second loop stays
  withheld for a second, independent reason on top of the queue-driver defect.

### (d3) Instrument-scoped envelopes — suggested by WS-E 76's probe evidence

Not previously named as an option; it falls out of the amendment block at WS-E 76,
finding (d), which is worth quoting because it changes what "scope" can mean:

> "**(d) INSTRUMENT ASYMMETRY, and it is the sharpest single result.** The file-write
> instrument is evaluated by its DECLARED TARGET PATH; shell commands are evaluated by
> a TEXT SCAN of the command. Identical content — the same two protected path strings —
> passes through the file tool and is denied through the shell. **Effective coverage
> therefore differs by INSTRUMENT rather than by ACT.**"

An envelope manifest could therefore scope by instrument as well as by path — for
example admitting file-tool writes within a path scope while leaving shell writes at
the ask. This is **stronger where it applies**, because a declared target path is a
fact the guard can evaluate exactly, whereas a text scan is a heuristic that has
produced three false-REDs. It is also **narrower**, and it does not fit acts whose
instrument is necessarily the shell.

### 5.1 Summary

| Option | Grants? | Records? | Invariant | Provable today | Reaches render route |
|---|---|---|---|---|---|
| (a) hook-only | yes | yes, by design | satisfied both halves | yes, stdin payload against `main()` | no |
| (b) settings deny | no | no | permission half vacuous; refusal half UNKNOWN | no — needs the external probe | **yes, uniquely** |
| (c) hooks-as-F5 proper | unknown | unknown | not assessable — source absent | unknown | unknown |
| (d1) M3 server-side | no | refusals only, off-machine | refusal half strong | yes | n/a — different layer |
| (d2) null | no | no | satisfied trivially, records nothing | n/a | no |
| (d3) instrument-scoped | yes | yes, if built on (a) | satisfied both halves | yes | no |

---

## 6. Decision ask

Numbered questions for the chair, each with the evidence it needs. **This brief does
not answer them.**

**Q-F5-1 — Is the observability invariant at section 3 adopted as the governing
standard for F5?** *Evidence needed:* none beyond this brief; it is a standard-setting
ruling. *Consequence if adopted:* options are judged against it rather than on
convenience, and any option failing it is rejected with a stated reason rather than
weighed.

**Q-F5-2 — Which option, or combination, is F5?** *Evidence needed:* Q-F5-3's answer
for (b); nothing further for (a) or (d3). *Note:* (a) and (b) are complements, not
alternatives — (b) permits nothing and answers no part of A2.

**Q-F5-3 — Is the external probe at section 4 authorised, and when?** *Evidence
needed:* an operator willing to install a witness build and run four rows in a fresh
session. *Note:* the probe build is a prototype of the log sink (a) needs anyway, so
authorising it early buys design evidence rather than only a yes/no.

**Q-F5-4 — What is the envelope manifest's freeze rule?** *Evidence needed:* none;
this is a design ruling. The question is what prevents the manifest being edited while
a run is in flight, and what an unreadable or absent manifest resolves to. Queue item
48 already proposes the conservative answer — UNKNOWN-and-refuse, on the three-outcome
discipline — and it needs ruling rather than assuming.

**Q-F5-5 — Where does the ask-tier log live, and is it append-only by mechanism or by
convention?** *Evidence needed:* a decision on location, since the guard runs on every
tool call and a log inside the repository would appear in every `git status` and every
diff-stat battery. *Note:* the audit store precedent at DEC-0016 is append-only **by
database grant**, and a file-based log has no equivalent unless one is built.

**Q-F5-6 — What is the guard's behaviour when the log write fails?** *Evidence
needed:* none; a design ruling. The invariant implies fail-closed — a call that cannot
be recorded must not be permitted — but the module's current posture is deliberately
fail-open on a malformed payload so as never to wedge the session, and these two
principles point in opposite directions on the same code path.

**Q-F5-7 — How does an envelope expire?** *Evidence needed:* none; a design ruling.
Queue item 48 states the reason it cannot be deferred: "an envelope that never closes
is a permanent widening wearing a different name."

**Q-F5-8 — Which obligations are deliberately left to M3 rather than to F5?**
*Evidence needed:* the current branch-protection configuration, readable from GitHub.
*Note:* WS-E 75's disposition already routes the ask-tier gap to the M-family, so a
silent division of labour would leave two records each assuming the other covers it.

**Q-F5-9 — Is the option at (c) real?** *Evidence needed:* the source document, or a
ruling that it is superseded. It cannot be assessed while its text is outside the
repository.

---

## 7. Relationship map

**F1–F4 — installed, and a different kind of change.** Corrective fixes to *matching*,
discharged across PRs #142 to #144, closing WS-E 72, 73 and 74. F5 changes *resolution*
and adds *recording*. The distinction matters for expectation-setting: F1–F4 could be
verified by re-running the probes that found the defects, whereas F5 has no
pre-existing defect to re-probe and needs its evidence designed with it.

**Queue-driver F2 — distinct, and the label collision is now the third in this
family.** DEC-0019's operational-status note withholds the 60-second unattended loop
"until defect F2, refused-draft re-paging, lands". That F2 is the **queue driver's**,
and has nothing to do with the guard's F2, which taught the write-detection to
distinguish a descriptor duplication from a file redirection. DEC-0018 already carries
a warning of exactly this shape about the candidate's own F1 footnote, which is
"unrelated to the guard fixes F1–F4 ... which collide only in label". **OPEN-4:** the
fuller characterisation the envelope gives for queue-driver F2 — *refused-draft
terminal state plus stale-sweep archive* — is not documented in the tree. What is
in-tree is the driver's docstring, which records that a refusal produces "an ERROR
page, a log row, and no route" and that "none is retried, because none is transient",
plus DEC-0019's naming of the defect. The gap between those and the envelope's phrasing
is marked rather than reconciled.

**WS-E 73 and 76 unification — owed, and F5 should not pre-empt it.** WS-E 76's
amendment block already states the corrected reading: "the better reading is the
**same rule as item 73, with the descriptor-duplication token removed by the F2 fix**.
'Same false-RED family' stands. 'Third trigger' does not." The write-detection refinement
that would fix both is a `.claude/hooks/` change on the same route as F5 — so they will
compete for the same operator installs, and sequencing them is a real decision. It is
**not** part of F5's scope as CL-31 framed it, and this brief does not claim it.

**Item 34 M2 — this brief is inside the perimeter; one of its options is not.**
Option (c)'s source cannot be read (OPEN-3), which is the M2 gap presenting inside a
brief written partly because of that gap. The DEC-0018 fold-in closed one M2 instance
by transcribing three source documents; this is another, and it is recorded as evidence
for M2's priority rather than as progress against it.

**RB-1, RB-2, RB-3 — all three bear on F5, and one bit this authoring act.** From
`docs/governance/QUEUE_CYCLE_2026-08-21.md` section 3, all three are open boundary
questions for a chair ruling batch. **RB-1** — whether AMD-A4's instrument boundary
reaches writes outside the repository — bears directly on Q-F5-5, because a log file
outside the tree is exactly the case RB-1 leaves unresolved. **RB-2** — whether the
no-`2>&1` rule is standing discipline or spent guard hygiene — bears on what an
envelope manifest may scope, since a rule that is spent should not be encoded into a
new mechanism. **RB-3** — the sanctioned Write-tool pattern for very large files — bit
this act: the envelope grants Write for three files and **no Edit at all**, so the
incremental Write-then-Edit-append route RB-3 describes was unavailable here, and this
brief was written as a single Write by necessity rather than by choice. Recorded
because RB-3 asks which pattern is sanctioned, and a case where the alternative was
foreclosed by grant is evidence for that ruling.

**Refusal as a queue object — this envelope is its own instance.** PROMPT 139 was
refused twice at T1 on 21 August as a mis-window, the lane prefix and TARGET not
matching that terminal's lane, which is DEC-0018/AMD-A3 working exactly as ratified:
"a terminal receiving a release line whose prefix or envelope TARGET does not match its
own lane refuses rather than obeys."

**In-tree corroboration, and its limit.** A listing of both T1 queue directories this
session shows **no `PROMPT-139` artefact of any kind** — not in `inbox`, not in
`outbox` — while the only copy in the queue sits in T2's inbox. So the refusals
produced no queue object. Stated precisely: the absence is consistent with the
refusals having left only terminal text, and it does not by itself prove that is why —
a prompt never routed to T1 would leave the same absence. The two readings agree on the
consequence that matters here, which is that **nothing in the queue records that a
refusal happened**.

That is the gap the queue driver's refused-draft terminal state would close, by making
a refusal a first-class object with a place to live rather than a line in a transcript
that ends when the window does. It connects to F5 through the same invariant: a refusal
must be observable *somewhere*, and "somewhere" cannot mean a terminal session's
scrollback.

**RB batch and panel route.** This brief is panel-reviewable per the sequence at
correction 3(c) — design, brief, chair ruling, install, probe. It is at step two.

---

## 8. OPEN gaps — consolidated

Each is marked OPEN in place above; this list exists so none is lost in the prose.

1. **OPEN-1 — the new response class.** Whether the harness honours an explicit
   `permissionDecision: "allow"` from a `PreToolUse` hook is established nowhere in
   this repository. The module has never emitted one. The alternative, a silent
   fall-through, is indistinguishable from no rule matching. (Section 1.4a.)
2. **OPEN-2 — refusal observability under a settings deny.** What the executor sees
   when a settings-level deny matches is unknown, and whether it lands anywhere
   readable is unknown. This is CL-31's blocker (ii). (Sections 2.5, 5b.)
3. **OPEN-3 — option (c) is unreadable.** The original uplift brief's text is not in
   the repository; a repository-wide search returned nothing, and CL-31 records the
   skeleton as discarded. The option is listed by name only. (Section 5c.)
4. **OPEN-4 — queue-driver F2's characterisation.** The envelope's phrasing — refused-
   draft terminal state plus stale-sweep archive — is not documented in-tree beyond
   DEC-0019's naming of the defect and the driver's docstring on refusal handling.
   (Section 7.)
5. **OPEN-5 — firing order.** Unprovable from inside the harness; the external probe at
   section 4 is designed and not authorised. (Sections 2.4, 4.)
6. **OPEN-6 — the standards-mapping line.** M11 makes the `Control mapping:` line
   prospective for a named list of artefact classes, and a design brief is not among
   them; the `scripts/check_docs.py` assertion M11 calls for does not exist. No mapping
   line is asserted here rather than one being guessed, which follows the precedent set
   at section 6 of `docs/governance/PRECEDENCE_DISCRIMINATOR_OUTCOME_2026-08-14.md`.
7. **OPEN-7 — sequencing against the WS-E 73/76 write-detection fix.** Both are
   `.claude/hooks/` changes on the operator-install route and will compete for the same
   installs. Not decided here, and not claimed as F5 scope.

---

## 9. What this brief does not do

It consumes no register number; it makes no change to the settings file, the guard, or
any existing file; it runs no probe; and it reaches no conclusion. It is one new file.
The decision it feeds is the chair's, and the questions it asks are at section 6.
