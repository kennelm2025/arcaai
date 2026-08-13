# FINDINGS — corpus-design matters raised by the SG-03..09 listing act

**Routed, not folded.** Operator ruling 2026-08-13: "corpus-design findings
routed not folded". These were surfaced while drafting the listing entries for
SYN-SG-03 through SYN-SG-09 at manifest version `2026-08-13.8`. None of them
blocked the listing, and none was fixed as part of it — a listing act lists.
They are recorded here so they have a home, and are addressed by whichever
process owns them.

Provenance: a seven-way `corpus-lister` fan-out, one agent per unlisted
document, read-only against the corpus. Each finding below was raised by the
agent reading that document. Where a claim has been checked against the
repository since, that is said; where it has not, that is said too.

## F-A — SYN-SG-03 §3.4 cites the wrong section of TY-01

The cross-reference at SYN-SG-03 §3.4 points at TY-01 §4, described as
"Onboarding-stage indicators", for recruitment patterns that sit at TY-01 §3.
Off by one section.

**Not checked by the lead.** Raised by the SG-03 agent from a reading of both
documents. It should be confirmed before anyone acts on it.

Owner: corpus content. Natural home is the batch-2 consistency read, since the
documents are immutable once committed and a correction is a new entry with a
new hash, never an edit. Worth noting the asymmetry: an off-by-one section
pointer is cheap to state and expensive to fix under that rule, which is an
argument for catching them at authoring rather than at listing.

## F-B — six cited targets do not exist on disk

Documents cited by the newly listed set that have no file:

| Cited target | Cited by |
|---|---|
| TR-03 | SG-04 §2.1, SG-08 §2.3 |
| TR-05 | SG-07 §2.2 |
| CV-03 | SG-05 §4.1 |
| CV-05 | SG-08 §5.2 |
| DL-06 | SG-07 §5.2 |
| DP-04 | SG-05 |

Several appear in the corpus edges register as planned documents, so these
read as forward references by design rather than defects. Two observations
that are not merely bookkeeping:

- **SG-05 §4.1 makes a MANDATORY assessment depend on CV-03**, which is
  unauthored. A mandatory obligation pointing at nothing is a different
  category from a "read together" pointer, and bears on the inclusion act
  rather than on listing.
- **The SG-07 to TR-05 relationship is asymmetric in the register.** The
  edges register makes SG-07 and DL-06 reciprocal, but TR-05's own set does
  not name SG-07, while SG-07 §2.2 says the two are to be read together.

Owner: corpus design and the authoring queue. Not a listing matter — the
documents were already authored with these references before this act.

## F-C — DEC-0011's no-paraphrase rule has unresolved scope

SYN-SG-06 §3.1 renders the three statutory heads of POCA 2002 s.330(5) in the
document's own words, and SYN-SG-09 paraphrases s.327 closely. DEC-0011
prohibits paraphrasing OGL material. Whether that prohibition reaches
**authored synthetic documents that restate statute in their own words**, or
only the OGL extracts themselves, is not answerable from the documents.

This does not affect either document's licence: both are authored arcaai text
and `synthetic-arcaai` is correct for both, which was verified independently by
two agents against the document content.

Owner: a DEC-0011 scope ruling. It is a question about the rule, not about
these two documents, and it will recur for every synthetic document that
characterises a statutory provision — which is most of the corpus.

## F-D — inclusion ordering is constrained by what is still unlisted

Several of the newly listed documents cite documents that are themselves not
yet included: SG-06 and SG-09 among others. This has no bearing on listing —
all seven are listed at `pending_review` — but it constrains the order of any
future inclusion act, and should be read before that act rather than during it.

## Method findings — the fan-out itself

Recorded because CLAUDE.md queue item 26 asked three scaling questions before
any wider fan-out, and this act answers them on evidence.

**26(a), whether the agent should hold an execution tool: no, and the question
dissolves.** All seven agents reported failure mode 2 on `content_sha256`,
having no way to compute a hash. That gap was harmless because the mechanical
fields came from `scripts/corpus_manifest_entries.py` in a prior pass, and the
lead independently recomputed all seven hashes from the files before writing
the manifest. Routing mechanics to the script removes the need for the grant
rather than justifying it.

**26(b), whether fan-out is the right instrument: split by capability, and both
halves earned their place.** The script produced every deterministic field —
hashes, synthetic-marker verification, drift check — in one pass, and a
seven-agent fan-out to recompute them would have been waste. The agents
produced the seven `source` lines and found F-A through F-D, none of which a
script could see. The instrument question was a false dichotomy; the real
question is which fields are mechanical and which are judgment.

**26(c), the divergent shapes: caused by underspecification, and closed.** The
pilot produced divergent shapes on `processing` and on the eligibility date.
This act pre-specified both in the agent brief, and all seven drafts came back
consistent on all three axes, verified by enumeration rather than by
inspection. The divergence was not a property of fan-out; it was a property of
not saying what shape was wanted.

**A precedent correction worth keeping.** All seven agents reported that the
listing-act date "departs from all precedent". Checked against the manifest,
that is over-stated: in every prior version the authoring date and the listing
date fell on the same day, so precedent was **silent** on the distinction
rather than contrary to it. SG-03..09 is the first case where the two differ.
Seven independent agents converging on the same over-strong claim is itself
worth noting — concurrence is not corroboration when the agents share a brief
and a reading of the same file.
