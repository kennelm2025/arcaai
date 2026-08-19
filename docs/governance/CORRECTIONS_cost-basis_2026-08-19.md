# Correction of record — 2026-08-18 cost basis

**Status: LANDED 2026-08-19.** This file is the correction of record for one
claim in `docs/governance/SESSION_HANDOVER_2026-08-19.md` section 9. Authored
under PROMPT 135 on branch `governance/item-42-discharge-2026-08-19`.

**The target is NOT amended, and that differs from the precedent.**
`docs/governance/CORRECTIONS_restart-claims_2026-08-14.md` applied its
amendments into the documents they corrected. This one does not, for a reason
specific to the target: the handover is **hash-pinned** and is verified at boot
against that pin. Editing it would break the pin and convert a verifiable
artefact into one whose first check fails, so the correction is recorded beside
it on the discipline the fold-in states — *"corrections to a narrative artefact
are recorded beside it"*.

**Pin, verified in this session before any act of this arc.** The handover's
SHA256 was recomputed at PROMPT 134 and matches the pinned value in full, all
64 hex characters:

```
35eac0d6502624ba962c85ea17b1e80abfa5b81842a638bd6405ed5b1b949b1e
```

It remains byte-frozen at that value after this correction lands, because
nothing in this arc writes to it.

---

## The claim corrected

`docs/governance/SESSION_HANDOVER_2026-08-19.md` section 9 records:

> **NOT SUPPLIED.** The `/cost` readout was requested at the close stop and did
> not reach the executor's context. […]
>
> If the readout is supplied later and the terminal was not restarted, the row
> derives by subtraction from the 2026-08-17 row — $88.05 · API 1h 16m 41s ·
> +4,804 / −56 — on the method stated in that row's notes.

**Both halves are now superseded, and they fail differently.**

**(a) NOT SUPPLIED is superseded by supply, not by error.** The readout was
supplied at the 2026-08-19 boot: **$52.14 · API 1h 3m 12s · +1204 / −31**,
dominant model NOT SUPPLIED. The handover's record was accurate when written —
the figure genuinely had not reached the executor — and it did exactly what this
register asks by writing the absence explicitly rather than leaving a blank.
**No fault attaches to it.** The row now exists at
`docs/governance/SESSION_COSTS.md`.

**(b) The subtraction route was wrong, and would have produced a negative
number.** This half is a real correction rather than a supersession. Subtracting
the 2026-08-17 row from the new readout gives **$52.14 − $88.05 = −$35.91**,
which is not a cost. The route's premise — that the counter was still cumulative
— is false: the readout is **lower** than the $121.05 cumulative anchor the
2026-08-17 close recorded, and a cumulative counter cannot read lower than it
previously read. The counter had reset. The correct basis is **DIRECT**.

## Why the wrong route was reachable, which is the part worth keeping

The handover's conditional was *"if the readout is supplied later **and the
terminal was not restarted**"*. That condition **was satisfied** — the operator
reports the terminal was not restarted — and the route it gated was still wrong.

**The defect is that restart-recollection was used as the reset test.** A
terminal restart is sufficient to reset the counter but is not necessary for it;
the CC session boundary resets it too. So a true answer to "was the terminal
restarted?" licensed a false conclusion about whether the counter had rolled
over. The condition was checkable and checked, and it did not test what it was
being relied on to test.

**Family: check-method** (`CLAUDE.md` queue item 8) — a check whose stated
subject is narrower than the subject it is used to decide. It is the same shape
as the `%(trailers)` and `governed_store_identity.py` instances that item and
item 28 record, and it is the second time in this register's short life that a
cost figure has needed a method note rather than a number.

**The corrective, adopted at the 2026-08-18 row and prospective from it:** a
counter reset is proven by **sign check against the previous cumulative
anchor** — arithmetic on two recorded figures, checkable by any later reader —
and never by recollection of whether a restart occurred. The recollection may
still be recorded, and here it is: it is what locates the reset *boundary* at
the CC session once the sign check has established that a reset *happened*. The
two legs do different work and the note keeps them apart.

## Disposition

Full method, the derived columns and the residual limit — a mid-session reset
would be indistinguishable, so the figure is a lower bound that is probably
exact — are at `docs/governance/SESSION_COSTS.md`, "Notes on the 2026-08-18
row". This file records only the correction.

No control mapping line is carried, for the reason `docs/governance/SESSION_COSTS.md`
states: queue item 34 M11(d) requires per-class mapping content to be defined
once in the control framework, and that framework does not exist yet.
