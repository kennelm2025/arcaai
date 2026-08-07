SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai.

# SG-03 — Sector Guidance: Transaction Monitoring for Retail Payment Accounts

**Issued by the Authority · Sector Guidance series · Reference SG-03**

## 1. Status and application

1.1 This guidance applies to relevant firms operating transaction
monitoring over retail payment accounts. It describes how the
Authority interprets the ongoing monitoring obligations of the
Framework and what it will look for in supervisory work. It is
guidance, not rules: a firm may meet the underlying obligations by
other means, but should expect to explain how.

1.2 Firms should be aware that guidance issued by a supervisory
authority is among the matters a court must consider in proceedings
under section 330 of the Proceeds of Crime Act 2002 (the extract at
OGL-0004): see s.330(8). This guidance is written with that context
in mind. Its scope is the fraud dimension of the design and
operation of transaction monitoring; it is not a statement of a
firm's full obligations under that Act, and firms should take their
own advice on them.

1.3 This guidance concerns monitoring of accounts in operation.
Controls at the point of opening, and the treatment of newly opened
accounts, are addressed in SG-01; this guidance assumes the
graduated-capability approach described there (SG-01 §4) and begins
where it ends.

## 2. The risk this guidance addresses

2.1 The Authority's thematic review of transaction monitoring
(TR-01) found that monitoring failure is rarely a failure to collect
data. The findings summarised at TR-01 §2 describe firms holding the
signals that would have identified the losses examined, in systems
that were not designed to ask the right question of them — and, in
particular, receiving-side weaknesses as significant as sending-side
ones.

2.2 The networks described in the typology work at TY-01 depend on
this. Mule chains route proceeds through accounts whose individual
transactions are unremarkable; the design of the chain is precisely
that no single hop looks like anything (TY-01 §5). Monitoring built
exclusively on per-transaction thresholds is monitoring those
networks have already priced in.

## 3. Sequences, not events

3.1 The Authority expects firms' monitoring to be designed around
event sequences as well as individual events. Many of the
highest-harm frauds present as a cluster of individually innocuous
events in close succession: a change of registered contact details,
the registration of a new device, the raising of a payment limit,
the quietening or redirection of alerts by the customer, the
creation of a new payee, and a maximum-value payment, occurring
within one session or one day. Each event, taken alone, sits inside
normal customer behaviour at low frequency. The cluster does not,
and it occurs before the money moves. Temporal compression is part
of the signal: the same events spread across weeks describe a
customer living with an account, and the Authority regards a cluster
dispersed over more than a short operational window as a different
and materially weaker indicator.

3.2 Sequence detection changes what monitoring can do. A
per-transaction rule can, at best, interrupt a payment in flight; a
sequence rule can raise the account's standing before the payment is
attempted. Firms should treat the interval between a suspicious
preparatory sequence and the first material outbound payment as the
intervention window monitoring exists to create, and should be able
to show that their monitoring shortens the distance between
detection and action within it.

3.3 Customer-initiated changes to the monitoring relationship
itself — the suppression, quietening or redirection of alerts, or
changes to the channels on which the firm can reach the customer —
are events, and should be treated as monitoring inputs of elevated
weight when they occur in proximity to other risk-relevant events. A
firm whose alerting can be silenced by the party being monitored,
without that silencing itself registering, has a monitoring design
defect.

3.4 The receiving side carries the same expectation. An account
receiving a payment materially inconsistent with its history,
followed by rapid onward dispersal, is a sequence, and TR-01 §2
records what happens when only the sending side is watched. The
recruitment patterns described at TY-01 §4 mean the receiving
account holder may be a willing participant, a directed one, or a
victim; the duty to detect the pattern is the same in each case, and
the account holder's status bears on how the firm handles what it
has detected, not on whether it should have detected it.

## 4. Calibration, triage and capacity

4.1 The Authority's observations on rule design and calibration at
TR-01 §3 apply with equal force to sequence rules. A sequence rule
tuned so wide that it fires on ordinary customer life events will be
tuned back down by the firm's own alert-handling pressure until it
detects nothing; a rule tuned to fire only on the completed pattern
detects the fraud after the window has closed. Calibration is a
standing activity, not a deployment step, and firms should be able
to evidence the calibration history of their material rules.
Evidence of that history means records of what the rule was and when
it changed — rule-version logs, the false-positive and detection
rates observed against each version, and the rationale for each
material adjustment — or equivalent records serving the same
reconstruction.

4.2 Detection without capacity is not monitoring. The triage
findings at TR-01 §4 describe alert queues whose depth converted
timely detection into untimely review. The Authority regards a
firm's alert-handling capacity, and the prioritisation applied
within it, as part of the monitoring system: a sequence alert of the
kind described at §3.1 arriving in a queue with a multi-day backlog
has failed at the point of queueing, whatever the rule's quality.

4.3 Where monitoring produces an intervention — a declined payment,
a suspended capability, an outbound contact — the firm should know,
per account and per rule, what happened next. Interventions that are
routinely reversed without adverse findings are calibration
information; interventions that are routinely followed by confirmed
fraud elsewhere are also calibration information. Both should flow
back into rule design on the principle set out at TR-01 §5.

## 5. Monitoring and the disclosure obligation

5.1 Section 330 of the Proceeds of Crime Act 2002 (OGL-0004)
attaches consequences not only to what a firm's staff knew or
suspected, but to what there were reasonable grounds for knowing or
suspecting: s.330(2)(b). Monitoring is where such grounds most often
first exist in objective form. A firm whose monitoring cannot
surface the patterns described in this guidance risks finding that
the grounds existed in its systems while no person was in a position
to act on them.

5.2 The Authority accordingly expects the escalation path from
monitoring output to the firm's nominated officer to be defined,
tested and timely. This guidance does not interpret the statutory
tests, and firms should take their own advice on the extracts at
OGL-0004.

## 6. Records

6.1 Firms should retain the inputs to each material monitoring
decision — the events observed, the rule state at the time, the
alert disposition and its rationale — in a form that supports later
reconstruction, on the principle applied at TR-01 §5 and in SG-01
§6. Where a confirmed fraud postdates a monitoring alert that was
closed without action, the Authority's first questions will concern
what the closing analyst saw and what the firm's calibration had
taught the rule by then.

6.2 A firm should be able to reconstruct, for any account and any
day, what its monitoring knew. A monitoring system that cannot
answer that question cannot demonstrate that it works, to the firm
or to the Authority.

**End of SG-03.**
