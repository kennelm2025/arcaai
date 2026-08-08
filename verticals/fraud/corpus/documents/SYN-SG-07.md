SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai.

# SG-07 — Sector Guidance: Automated Fraud Detection Systems

**Issued by the Authority · Sector Guidance series · Reference SG-07**

## 1. Status and application

1.1 This guidance applies to relevant firms operating automated
systems in the detection of fraud over retail payment accounts. It
describes how the Authority interprets the Framework's obligations
as they bear on the design, validation and oversight of those
systems, and what it will look for in supervisory work. It is
guidance, not rules: a firm may meet the underlying obligations by
other means, but should expect to explain how.

1.2 This guidance is concerned with the fraud dimension of
automated detection. It is not a statement of a firm's obligations
in respect of the processing of personal data, or of its
obligations concerning fairness in the treatment of customers,
which arise elsewhere; firms should take their own advice on them.

1.3 This guidance concerns the systems through which a firm's
detection obligations are met, whether those systems apply written
rules, learn their behaviour from data, or combine the two. What a
firm's monitoring should be capable of detecting is addressed at
SG-03, and the treatment of newly opened accounts at SG-01 §4; this
guidance assumes those expectations and addresses how the systems
that carry them are built, proven and supervised.

## 2. The risk this guidance addresses

2.1 Automated systems are now the means by which most firms see
fraud at all. That concentration changes the character of failure. A
member of staff who misjudges a case misjudges one case, and the
error is visible in the file; a detection system that is wrong is
wrong uniformly, silently, and on every account it touches, until
something outside the system reveals it. The Authority's concern is
accordingly less with the sophistication of a firm's systems than
with whether the firm can demonstrate that its own is working — and
can still demonstrate it a year after deployment.

2.2 The Authority's thematic review at TR-05 examines firms'
practice in this area; this guidance sets out the expectations
against which that practice will be assessed, and the two should be
read together.

2.3 A firm may be able to describe what its system was built to
catch, and to produce alert volumes and performance statistics for
it, and still be unable to say what the system did in a particular
case or why. A system whose decisions cannot be reconstructed
cannot be shown to work, to the firm or to the Authority.

## 3. Design, data and the limits of learned detection

3.1 A detection system should be designed against the fraud it is
meant to find, and firms should be able to state which fraud that
is. The typology work at TY-02 supplies the clearest illustration
of the difficulty. In every scenario that report describes, the
payment is genuinely authorised by the account holder; controls
built on the question whether the customer authorised the payment
therefore pass it (TY-02 §2.1). A system whose inputs encode the
authenticity of the instruction — authentication succeeded, the
device is known, the session is the customer's own — will score
these payments as good ones, and will do so with confidence,
because on the question it has been asked they are good ones. The
operative questions are different, and what the system is given to
work with must differ accordingly.

3.2 Systems that learn from outcomes learn from the outcomes a firm
records, and those outcomes are not a neutral sample of the fraud
the firm suffers. Authorised fraud is under-represented among
confirmed cases wherever a firm's controls treat authorisation as
dispositive, and coerced authorisation is under-represented further
still: TY-02 §4.1 records that coerced cases rarely present the
urgency signature of the impersonation scenarios and frequently
present none of the payee-novelty signals on which detection
commonly rests. A system trained on such a record will improve at
what the firm already catches, and its improving performance
figures will report that narrowing as success. Firms should know
what their labelled data does not contain, and should be able to
say what they do about it.

3.3 Where a customer occupies more than one role, the record should
say so. TY-02 §4.2 describes the customer who is at once a victim
on the sending side and a recruited account holder on the receiving
side, and cautions firms against classifying such customers by
whichever role was detected first. A classification taken for
operational convenience becomes, in a system that learns, a
training label; the firm's first impression is then generalised
across every similar customer the system subsequently scores.

3.4 The Authority expects firms to be able to explain the exclusion
of signals they hold. SG-01 §3.2 asks a firm that collects device
and session signals at onboarding, and does not use them in its
opening decision, to be able to say why; the same expectation
attaches to signals the firm holds and withholds from, or does not
make available to, its detection systems. Where the analysis of
fraud outcomes by onboarding cohort described at SG-01 §5 shows a
cohort the system serves poorly, that finding is an input to the
system's design and should be evidenced as such.

3.5 A firm may obtain a detection system from a third party; it may
not obtain from a third party the ability to explain the decisions
it takes. Where a system is supplied, inherited, or operated under
an arrangement that prevents the firm from examining how outputs
are reached, the firm should recognise that it has accepted a
constraint on its own ability to meet the expectations in this
guidance, and should expect to be asked how that constraint is
managed.

## 4. Validation, calibration and degradation

4.1 A system should be validated before it is relied upon, by
people who did not build it, against the fraud it is intended to
detect and on data it has not seen. The validation should be
recorded: what was tested, what was found, what limitations were
accepted, and by whom. A firm unable to produce that record has
deployed the system on the strength of the confidence of its
builders.

4.2 Detection systems degrade, and the Authority regards
degradation as the normal condition of a system operating against
an adversary rather than as an incident to be reported when
noticed. The typology work at TY-09 §3.1 describes the mechanism
from the inside: among the commodities an insider sells, the least
visible and most damaging is control intelligence — which patterns
the monitoring catches, which thresholds trigger review, which
checks are performed on which queues, and when. A network holding
current control intelligence designs its activity to pass, and the
firm's detection statistics stay green while its losses move. A
stable alert rate is therefore not evidence that a system is
working. Firms should assess the performance of their detection
systems against outcomes rather than against activity, and should
treat a divergence between the two as a matter for investigation.

4.3 Calibration is a standing activity, not a deployment step. The
expectation at SG-03 §4.1 — that firms be able to evidence the
calibration history of their material rules — applies to automated
systems generally, and extends to the thresholds at which their
outputs are acted upon. A score is not a decision until a threshold
is applied to it, and the threshold is as material a control as the
system that produces the score.

4.4 Changes should be controlled and recorded. A firm should be
able to say which version of which system was in force on any date,
what changed at each revision, what testing supported the change,
and who approved it. Where a system is retrained on new data, that
is a change within the meaning of this paragraph, whether or not
anything else about it was altered.

## 5. Oversight, accountability and access

5.1 Where an automated output determines or materially influences
an outcome affecting a customer — a payment declined, a capability
suspended, a relationship exited — the Authority expects a person
to be in a position to understand the output and to depart from it.
Understanding here means the basis of the output, in terms the
person can weigh against the case in front of them, and not merely
the fact of its production. Firms should be able to demonstrate
that departures occur, and should examine an oversight arrangement
that never produces one.

5.2 Accountability for these systems is not a technical matter and
should not rest solely with the function that operates them. The
Authority's expectations of firms' chief executives in respect of
the matters addressed in this guidance are set out in the Chief
Executive letter at DL-06, and firms should be able to show how the
arrangements described there govern the systems in scope here.

5.3 Access to a detection system's logic, thresholds and outputs is
a fraud-relevant privilege and should be controlled as one. On the
reasoning of TY-09 §3.1, a firm's detection systems are where
control intelligence is most concentrated, and the staff who can
read them are exposed to the same cultivation as those who can
release payments. TY-09 §4.3 records that effective insider
analytics require a joining capability deliberately separated from
the operational teams whose data it examines, and that reported
matters include cases where the monitoring existed and the insider
was among its administrators. Firms should ensure that the ability
to change a detection system's behaviour, the ability to see what
it catches, and the ability to review the cases it raises do not
accumulate in the same hands unobserved.

5.4 The Authority examines these arrangements in supervisory work,
and will ask a firm to demonstrate them by reference to particular
cases rather than by description of the arrangement.

## 6. Records

6.1 Firms should retain, for each material decision taken by or on
the strength of an automated system, the inputs the system
received, the version of the system in force, the output produced,
the rule or threshold applied to that output, the disposition and
its basis, and the identity of any person who reviewed it — in a
form that supports later reconstruction, on the principle applied
in SG-01 §6 and SG-03 §6.1.

6.2 A firm should be able to answer, for any account and any day,
what its detection systems saw, what they concluded, and why the
firm acted as it did. Where a confirmed fraud follows a decision an
automated system took or informed, those are the Authority's first
questions.

**End of SG-07.**
