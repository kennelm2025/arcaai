---
name: ledger-touch
description: Append a WS-E incidents-ledger entry with the sequence-hold check enforced. User-invoked only; never chained from another act.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git diff:*)
---

# Ledger touch — governed WS-E append

Entry to append (operator's words): $ARGUMENTS

Current ledger tail — CONTEXT ONLY, never a numbering source. This is
the file's last 30 lines, which are addendum cross-references ("To
51/55:", "To 56/58:") and footnotes. The numbers appearing in it are
back-references to earlier items, not the sequence head, so it cannot
contain the highest item number:
!`python -c "import io; lines=io.open('docs/governance/WS-E_INCIDENTS.md',encoding='utf-8').readlines(); print(''.join(lines[-30:]))"`

Numbered-item sequence — the authoritative numbering source (last five
items, read from the item headings themselves):
!`python -c "import re,io; ls=[l.rstrip() for l in io.open('docs/governance/WS-E_INCIDENTS.md',encoding='utf-8') if re.match(r'^[0-9]{1,3}\. ',l)]; print('\n'.join(ls[-5:]))"`

# Your task

1. Identify the highest existing WS-E number from the ledger's
   numbered sequence itself — the item headings in
   `docs/governance/WS-E_INCIDENTS.md`, as rendered above — and
   corroborate it against the WS-E figure in this session's
   regenerated REPO_MANIFEST. Never derive it from the tail render,
   and never from a manifest found on disk. State the number
   explicitly and name the two sources that agreed. If they
   disagree, stop and reconcile before writing anything.
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
