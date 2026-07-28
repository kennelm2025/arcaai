SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai.

# TR-02 — Thematic Review: Screening Arrangements at the Fraud and Sanctions Boundary

**Issued by the Authority · Thematic Review series · Reference TR-02**

## 1. Purpose and scope

1.1 This review examined how eleven relevant firms operate the
boundary between fraud detection and their screening obligations —
list-based screening of customers and payments against designated
persons, and the handling of matches, near-matches and the fraud
signals that frequently accompany them. The two control families are
usually run by separate teams on separate systems; this review
examined what falls between them.

1.2 The review complements TR-01, which examined transaction
monitoring for fraud. The reporting obligations engaged when
screening or monitoring surfaces reportable conduct are those of
SG-02; nothing in this review varies them.

## 2. Summary of findings

2.1 Screening arrangements were, in isolation, broadly sound: list
management was current at ten of eleven firms, and match-handling
queues were resourced. The weaknesses found were at the boundary —
information that one control family held and the other needed.

2.2 The most consequential pattern: accounts exhibiting the mule
network characteristics of TY-01 were frequently also generating
screening near-matches or adverse-information signals, and neither
team could see the other's picture. At five firms, the review team
assembled — from the firm's own data — a combined view that neither
the fraud function nor the screening function possessed.

2.3 The Authority regards this fragmentation as a design finding,
not an operational one. Controls organised around regulatory category
rather than around the customer will systematically miss actors whose
conduct spans categories, which describes the networks in TY-01 §2
precisely.

## 3. Screening operation findings

3.1 Fuzzy-match calibration varied more than list content did. Two
firms operated thresholds so tight that transliteration variants of
designated names passed unmatched; one operated thresholds so loose
that match volumes overwhelmed the handling team, producing the
queue-aging pathology already described for fraud alerts in TR-01
§2.3. Both extremes are findings; calibration should be evidenced
against test cases, on the principle of TR-01 §3.2.

3.2 Payment-message screening should account for the message fields
that networks actually manipulate. The review found screening
configured to examine payee name fields while remittance-information
and address fields — where obscuring content was observed in the
matters examined — passed unscreened at four firms.

3.3 Match-handling records met the standard expected for
intervention records generally (TR-01 §5.2) at most firms. The
exception was discounted matches: at three firms, near-matches were
discounted with a recorded rationale of "known false positive"
inherited from a previous discount, in chains extending back years.
A discount rationale that consists of a pointer to an earlier
discount is not a rationale; DP-01 §2.1 describes how such records
are weighed after the event.

## 4. The boundary

4.1 Firms should ensure that a screening event on an account is
visible to fraud monitoring as a risk input, and that fraud
indicators on an account are available to the screening function
when it assesses a match on that account. The convergence signals of
TY-01 §5.2 and a screening near-match on the same account are, in
combination, materially more significant than either alone.

4.2 Escalation routes should converge before reporting decisions are
made. Where the fraud route (SG-02 §2) and the screening route reach
different designated functions, firms should ensure a single point
at which the combined picture is assessed against the SG-02 §3
threshold, so that a matter reportable on the combined facts is not
missed because each function saw only half of them.

4.3 Onboarding is part of the boundary. The clustering indicators of
TY-01 §4 and screening results at application should inform one
another; SG-01 §3.2's expectation that collected signals are used in
the opening decision applies to screening outputs as to any other
signal.

## 5. Actions for relevant firms

5.1 Relevant firms should map, concretely, what each control family
can see of the other's outputs, and close the gaps this review
describes. The Authority will include boundary questions in the
supervisory work announced in DL-01 §4.1 and will expect the mapping
to exist.

**End of TR-02.**
