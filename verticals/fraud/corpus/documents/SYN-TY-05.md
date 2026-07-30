SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai.

# TY-05 — Typology Report: Invoice Redirection and Business Email Compromise

**Issued by the Authority · Typology series · Reference TY-05**

## 1. Purpose

1.1 This report describes invoice redirection fraud and the broader
business email compromise (BEC) family it belongs to: frauds in
which a business is deceived into paying a genuine obligation to
the wrong account, or into paying an obligation that does not
exist, through the compromise or convincing imitation of a trusted
correspondence channel. It is the business-victim counterpart of
the consumer APP typology at TY-03, and the sending-side indicator
families set out there apply with the adjustments described below.

## 2. The shape of the fraud

2.1 In the classic redirection, the fraudster inserts themselves
into an existing supplier relationship. A genuine invoice is
expected; what arrives is either the genuine invoice with altered
payment details, or a plausible notification that the supplier's
bank details have changed, followed by the genuine invoice. The
victim's accounts payable process then does exactly what it is
designed to do — pay the invoice — and does it to the fraudster's
account. Every element of the payment is authorised, correctly
approved, and wrong.

2.2 The channel compromise takes two observed forms. In the first,
the supplier's or customer's mailbox is genuinely compromised, and
the redirection request arrives from the authentic address, inside
the authentic thread, in the authentic voice, sometimes timed to a
real invoice the fraudster can read in the mailbox. In the second,
the fraudster imitates the channel — a lookalike domain a character
away from the real one, a display name over an unrelated address —
and relies on the reader seeing the name and not the address.

2.3 The executive impersonation variant dispenses with the invoice
altogether: a message purporting to come from a senior figure
instructs a payment, urgently and confidentially, often to support
a supposed acquisition or settlement. The urgency and the
confidentiality do the work that the genuine invoice does in the
redirection form — they suppress exactly the checks that would
detect the fraud. The pressure mechanics are those described at
TY-03 §2.3, transplanted into a hierarchy.

## 3. The statutory frame

3.1 Each variant rests on fraud by false representation under
section 2 of the Fraud Act 2006 (the extract at OGL-0001): the
representation that the payment details are the supplier's, that
the sender is the executive, that the obligation exists. Section
2(5) of that extract is directly in point for the imitation forms —
a representation is made even where it is submitted only to a
system or device, so an altered invoice ingested by an automated
accounts payable platform is a false representation to that
platform, with no human reader required.

3.2 Where the fraud is enabled from inside — a member of the
victim's finance function, or of the supplier's, abusing their
access to divert payments or to feed the fraudster the information
that makes the imitation convincing — the conduct also engages
fraud by abuse of position under section 4 of the Fraud Act 2006
(the extract at OGL-0002). That section reaches a person expected
to safeguard another's financial interests who dishonestly abuses
the position, and section 4(2) confirms the abuse may consist of an
omission: the payments clerk who notices the altered details and
says nothing has that provision to consider. Insider-enabled fraud
generally is the subject of TY-09; this report notes the overlap
and moves on.

## 4. Indicators

4.1 The controlling indicator family is change: changed bank
details, changed contact address, changed tone or timing in an
established correspondence. Reported matters repeatedly show the
change notified shortly before a large payment, and shown only in
the channel the fraudster controls — the email says the details
have changed, and nothing else does.

4.2 Verification through a second, independently sourced channel
defeats most of the typology, and its absence is the single most
common finding in reported matters. A telephone number taken from
the requesting email is not an independent channel; it is the
fraudster's switchboard. The verifying call goes to the number the
firm already held.

4.3 For the paying firm's bank, the sending-side signals at TY-03
§4 translate directly: a first payment to a newly created payee,
at a value far above the customer's pattern for that payee name;
account-name checking mismatches on a payee the customer believes
long-established; and payment instructions carrying unusual urgency
from a business customer whose payment runs are otherwise regular
as clockwork. A business that pays supplier invoices on a monthly
cycle and suddenly instructs a same-day payment to a new account
in an established supplier's name is exhibiting the typology.

## 5. Use of this report

5.1 Firms serving business customers should test their payment
anomaly detection against §4.3, and should consider how their
confirmation and warning journeys read to an accounts payable
professional processing their fortieth payment of the day rather
than to a consumer making their first. Business customers
themselves are outside the Authority's perimeter, but firms are
well placed to propagate the second-channel verification practice
at §4.2, and reported matters show that firms which do so
materially reduce their business APP losses.

5.2 This report is descriptive of reported matters. The
correspondence channels, the imitation techniques and the pressure
scripts adapt; the constant is the changed payment detail and the
suppressed check, and controls should anchor on those.

**End of TY-05.**
