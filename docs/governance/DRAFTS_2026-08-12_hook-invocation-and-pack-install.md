# Drafts for ruling — 2026-08-12 accelerator-pack install arc

Register anchor: REPO_MANIFEST regenerated this session 2026-08-12 09:01 UTC —
WS-E highest 67 → **next 68**; DEC highest 0016 → next 0017; ADR highest 0010 →
next 0011; CL highest 25 → next 26. Divergences 0.

Nothing below is ruled. Unconsumed numbers are cited as "next N" per the PR #85
correction note.

---

## 1. WS-E draft — next 68

68. **A relative-path hook command plus a persisted shell cwd deadlocked every
    tool, fail-closed (2026-08-12).** `.claude/settings.json` invoked the
    governance guard as `python .claude/hooks/governance_guard.py`, a path
    resolved against the process working directory. A `cd .claude` issued in the
    persistent PowerShell session moved that directory to
    `D:\ArcaAI-repo\arcaai\.claude`, where `.claude/hooks/governance_guard.py`
    does not exist. Every subsequent call matching the PreToolUse matcher
    (`Bash|PowerShell|Edit|Write|MultiEdit|NotebookEdit`) then invoked a hook
    that could not start. The session could not run a command, could not edit a
    file, and could not navigate back: the single act that would have cleared
    the condition was gated by the gate it had broken. Cleared by ending the
    session, a fresh one starting at repository root. NO HARM, and the direction
    is the whole point — the guard failed CLOSED. A hook that cannot execute
    blocked the tool rather than waving it through, so at no moment was an
    ungoverned write available; the deadlock was the control working, not the
    control absent. That is the property credited at item 67, and the defect
    here is the fragility of the invocation, never the policy.

    The remediation then reproduced the outage twice more, which is the more
    useful half of this entry. First, the absolute path was written with
    escaped backslashes (`D:\\ArcaAI-repo\\...`); these are unescaped twice —
    JSON decodes `\\` to `\`, then command parsing consumes the survivor as an
    escape character — collapsing the path to
    `ArcaAI-repoarcaai.claudehooksgovernance_guard.py` and deadlocking the
    session again, this time inside the corrective itself. Forward slashes carry
    no escaping layer and resolve correctly on Windows. Second, two successive
    operator fixes were reported applied while the loaded configuration stayed
    unchanged. The first account attributed this to a shadowing
    `settings.local.json`; enumeration disproved that — exactly one guard line
    existed anywhere in any settings file — and the cause was a stale editor
    buffer writing old content over new, an edit reporting saved while the
    buffer's stale content is what lands. Corrective: configuration fixes are
    applied by shell string-replace with the read-back appended to the same act,
    never through an editor whose buffer state is unverifiable.

    A read-once-at-session-start hypothesis was raised and excluded on evidence
    already in hand rather than by restarting: the first mis-edit took effect on
    the very next tool call, so hook configuration is re-read per invocation.
    The accidental experiment that caused the outage supplied the evidence that
    bounded it, and a session restart was correctly not spent.

    A second instance of the original root cause was found in the same read and
    remains latent: `current_branch()` in the guard runs
    `git rev-parse --abbrev-ref HEAD` with no `cwd=`, inheriting the same
    ambient directory. Outside a repository it returns `None`, which the guard
    already treats as UNKNOWN and asks on — fail-closed again — but inside a
    *different* repository it would report that repository's branch and could
    clear the HEAD-is-main gate on evidence from the wrong tree.

    CLASS NOTE, two parts. An enforcement path must not depend on ambient state
    that any ordinary act can change; a working directory is the most easily
    changed ambient state there is, and this outage was self-inflicted by one
    routine navigation command. And on probe shape: the guard was certified
    restored only by a DENY-shaped probe returning the guard's own refusal text
    verbatim, paired with an ALLOW-shaped probe that succeeded. A dead hook and
    a working hook are indistinguishable from any command that was going to be
    allowed anyway, so an allow-shaped probe alone would have passed a dead
    guard silently three times over. Same family as items 64 and 67 — a check
    whose stated subject is not the subject it interrogates — and this is the
    reported-done-not-done class at its fourth appearance in two days.

---

## 2. Convention lines draft — for `CLAUDE.md`, "Conventions that will bite you"

- **The harness never bare-`cd`s in a persistent shell.** Commands address
  files by absolute path, or wrap a directory change in `Push-Location` /
  `Pop-Location` with a guaranteed restore. A persisted working directory is
  ambient state that outlives the command that set it, and on 2026-08-12 a
  single `cd .claude` broke the governance hook's relative invocation path and
  deadlocked every tool fail-closed (WS-E next 68).

- **A hook or permission change is verified by re-reading the loaded file AND a
  deny-shaped probe** — never by the editor's word, and never by a command that
  would have been allowed anyway. The probe must return the guard's own refusal
  text verbatim; a refusal arising from a broken invocation is indistinguishable
  from a genuine denial at the blocked level, and an allow-shaped probe cannot
  tell a live guard from a dead one at all. Pair it with one allow-shaped call
  to prove the guard discriminates rather than merely blocks. Apply config fixes
  by shell string-replace with the read-back appended to the same act, because
  an editor can report a save while a stale buffer is what lands (WS-E next 68).

---

## 3. Hook path — options for ruling

The absolute path currently in the tree is a **tourniquet**: it hardcodes one
machine into a tracked file and would fail in CI or any other clone.

**Option A — exec form with `${CLAUDE_PROJECT_DIR}` (RECOMMENDED).**

    {
      "type": "command",
      "command": "python",
      "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/governance_guard.py"],
      "timeout": 10,
      "statusMessage": "Governance guard..."
    }

VERIFIED, not assumed, against the Claude Code hooks documentation: the braced
`${CLAUDE_PROJECT_DIR}` is a path placeholder substituted by Claude Code itself
into `command` and into each `args` element as a plain string, explicitly
"regardless of whether a shell is involved", so expansion is guaranteed on
Windows. The exec form (`args` present) is substituted with **no shell
re-parsing** — which is precisely the layer that ate the backslashes — so this
option is immune to the failure that produced the second deadlock as well as to
the first. Portable across machines, clones and CI.

Correction to my own earlier reading: I reported `CLAUDE_PROJECT_DIR`
unavailable. That test checked the unbraced `$CLAUDE_PROJECT_DIR` in the tool
shell's environment, which is a different question from the braced placeholder
in a hook command. The earlier conclusion was wrong and Option A is available.

**Option B — relative path restored, plus the `cwd=` companion and the
no-bare-`cd` convention.** Returns line 60 to
`python .claude/hooks/governance_guard.py` and relies on the convention to keep
the working directory at repository root. Portable, but it leaves the
enforcement path dependent on ambient state and defended only by a convention —
the exact arrangement that failed today.

**Option C — keep the absolute path.** Works on this machine only. Precedent
exists at settings.json lines 49–50, which already hardcode
`D:\arcaai-repo\arcaai\scripts\*.cmd`.

RECOMMENDATION: **A**, with the `cwd=` companion change at §4 landing regardless
of which is chosen, since it fixes an independent latent defect.

NOT APPLIED UNILATERALLY, and the reason is procedural rather than timid: a hook
edit that fails is unrecoverable inside the session, because `Edit` is itself
behind the broken gate. Three deadlocks today were each cleared only by operator
action. Option A therefore wants one round-trip — rule it, I apply it, then the
deny-shaped and allow-shaped probes certify it before anything else proceeds.

## 4. `.claude/hooks/governance_guard.py` — companion change (independent of the above)

`current_branch()` gains a repository root derived from the module's own
location, so the branch it reports is always this repository's:

    REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
    ...
    subprocess.run([...], cwd=REPO_ROOT, capture_output=True, text=True, timeout=5)

Fail-closed behaviour is preserved exactly: any exception or non-zero return
still yields `None`, and `None` still asks.
