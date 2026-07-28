SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai.

# DL-02 — Letter to Chief Executives: Data Quality Underpinning Fraud Detection Systems

**Issued by the Authority · Chief Executive letter series · Reference DL-02**

Dear Chief Executive,

## 1. Why we are writing

1.1 Two findings recur across our recent thematic work and we have
concluded they warrant a letter of their own. In the transaction
monitoring review, firms were found operating detection rules that
had silently stopped functioning when upstream data changed (TR-01
§3.4). In the screening review, message fields that networks
manipulate were passing unscreened because the screening
configuration did not know they existed (TR-02 §3.2). Both are data
findings before they are fraud findings: the controls were sound in
design and starved in fact.

1.2 We ask that this letter be tabled at your board risk committee
alongside DL-01, and its consideration minuted on the same basis
(DL-01 §1.2).

## 2. What we expect

2.1 **Know what your detection consumes.** For every material fraud
and screening control, we expect the firm to hold a current record of
the data it consumes, its source, and its owner. A control whose
inputs cannot be enumerated cannot be assured.

2.2 **Detect starvation within a business day.** Where a feed
consumed by a detection control degrades or stops, we expect the firm
to know within one business day, and the compensating position to be
documented in advance — the standard set in TR-01 §3.4. Silence from
a detection system is not evidence of absence of fraud; it is
frequently evidence of absence of data.

2.3 **Test with production-shaped data.** We have observed controls
tested against data that did not resemble what production would
supply — cleaner, more complete, better typed. Testing should include
the degraded shapes production actually produces, including the
partially populated messages at issue in TR-02 §3.2.

2.4 **Own changes end to end.** Upstream change control should treat
detection systems as consumers of record. A schema or semantic change
to customer, payment or device data that reaches production without
the fraud and screening functions having assessed impact is a
governance failure whoever caused it, and we will attribute it as
DP-02 §2 describes — on what the responsible individual should have
known and provided for.

## 3. What good looks like

3.1 The strongest firms in our recent work could produce, on
request: the input inventory of 2.1; feed-health monitoring with the
one-day standard of 2.2; test evidence per 2.3; and change records
showing detection impact assessed before release. None of this is
novel; all of it is the record-keeping discipline the Framework
already expects, applied to the data layer (TR-01 §5.2, SG-01 §6.1).

3.2 Boards should ask a simple question of their firms: if a feed
our fraud detection depends on failed today, when and how would we
learn? The quality of the answer is the state of the control.

## 4. What we will do

4.1 The supervisory work announced in DL-01 §4.1 will include the
expectations of this letter. Where we find detection starved of data
and no mechanism that would have noticed, we will treat the absence
of the mechanism as the finding, on the principle recorded in DP-01
§2.2 — an inoperative control untested by events is still a finding.

Yours faithfully,

**Director of Payments Supervision**
*for the Authority*

**End of DL-02.**
