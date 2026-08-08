---
name: ledger-touch
description: Append a WS-E incidents-ledger entry with the sequence-hold check enforced. User-invoked only; never chained from another act.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git diff:*)
---

# Ledger touch — governed WS-E append

Entry to append (operator's words): $ARGUMENTS

Current ledger tail:
!`python -c "import io; lines=io.open('docs/governance/WS-E_INCIDENTS.md',encoding='utf-8').readlines(); print(''.join(lines[-30:]))"`

# Your task

1. From the tail above, identify the highest existing WS-E number.
   State it explicitly.
2. Sequence-hold check (WS-E 58 rule): the next number is highest+1,
   and only that number. If the operator's text implies a different
   number, stop and reconcile before writing anything.
3. Draft the entry in the ledger's exact house format (match the
   style of the visible tail precisely — numbering, date form,
   punctuation). Show the draft to the operator.
4. On explicit confirmation ONLY, append it to
   `docs/governance/WS-E_INCIDENTS.md`. The governance hook will ask
   for confirmation again at write time — that is by design, answer
   it honestly.
5. After the write: `git diff --stat` and show the output. An empty
   diff means the append did not happen.
6. Do not commit. Committing is the operator's separate act.
