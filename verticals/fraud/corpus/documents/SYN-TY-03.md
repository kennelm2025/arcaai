SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai.

# TY-03 — Typology Report: Authorised Push Payment Fraud

**Issued by the Authority · Typology series · Reference TY-03**

## 1. Purpose

1.1 This report describes authorised push payment (APP) fraud: fraud
in which the victim themselves instructs their firm to make a
payment, having been deceived about who they are paying or why. It
is the defining feature of the typology that every control built
around unauthorised access fails, because the access is genuine. The
customer authenticates correctly, passes every challenge, and is the
one pressing send.

1.2 The deception that procures the payment will in the ordinary
case amount to fraud by false representation under section 2 of the
Fraud Act 2006 (the statutory extract at OGL-0001): the fraudster
dishonestly represents, expressly or by implication, a state of
affairs that is untrue — that they are the customer's bank, a
supplier owed money, an investment platform, or a person in genuine
need — intending to make a gain or cause loss. Section 2(5) of that
extract bears emphasis for firms operating digital channels: a
representation is made even where it is submitted only to a system
or device, with no human on the receiving end.

## 2. The shape of the fraud

2.1 APP fraud divides into impersonation frauds and purpose frauds.
In impersonation frauds the victim believes they are paying a
legitimate payee — their own bank moving money to a "safe account",
a supplier whose details have changed, a solicitor at completion. In
purpose frauds the payee is who they claim to be, but the purpose is
false — an investment that does not exist, goods that will never be
delivered, a romantic partner's fabricated emergency.

2.2 The distinction matters operationally. Impersonation frauds are
attackable at the payee: the receiving account is controlled by the
fraudster or a recruited mule, and the receiving firm holds signals
the sending firm cannot see. Purpose frauds are attackable mainly at
the sender: the payment destination may be an entirely genuine
account, and the observable anomaly is in the customer's behaviour
and the payment's context rather than in the payee.

2.3 In either form the fraudster's problem is urgency. A victim
given time reflects, consults, and checks. Every observed APP script
therefore manufactures pressure: the account is "about to be
compromised", the invoice is "overdue and holding up completion",
the investment window is "closing today". Pressure applied to the
payment moment is itself among the most reliable indicators
available to an intervening firm.

## 3. Where the money goes

3.1 The proceeds of APP fraud are extracted through the mule
networks described in TY-01. First-generation accounts receive the
victim's payment and move it onward within hours; the layering that
report describes exists precisely so that recovery attempts arrive
after value has left the second layer. A firm reading the present
report should read it alongside TY-01: the sending-side typology
here and the receiving-side typology there are two views of the
same flow.

3.2 It follows that the receiving firm's onboarding and monitoring
arrangements are APP controls, whether or not they are labelled as
such. The account opening guidance at SG-01 sets the Authority's
expectations for detecting account acquisition at volume, and SG-01
§4.2 sets the expectation that the characteristic first-inbound-
then-rapid-outbound pattern prompts intervention rather than
observation. An account that receives an APP victim's payment
exhibits exactly that pattern.

## 4. Sending-side indicators

4.1 Indicators observed in reported matters cluster around three
questions: is this payment unusual for this customer, is the payee
new or newly changed, and is the customer behaving as though
coached or under pressure.

4.2 Unusual-for-customer signals include payments materially larger
than the customer's established range; first payments to a new
payee at or near available balance; payments emptying a savings
product the customer has never previously drawn on; and sequences
of payments to one payee in amounts that sit just under a
customer's per-transaction limit.

4.3 Payee signals include recently created payees, payee details
changed shortly before a large payment, and payees whose account
names fail to match the name the customer believes they are paying.
Where name-checking services return a mismatch and the customer
proceeds regardless, the proceed decision is itself information.

4.4 Behavioural signals include the customer being on another call
while making the payment; reading answers to security questions or
payment-purpose questions as if from a script; requesting that a
payment be split into several smaller payments after a first
attempt is declined; and visible distress or urgency inconsistent
with the stated purpose. Firms should note the parallel with the
coached-answer indicator at SG-01 §3.4: in mule recruitment it is
the account holder who is scripted, in APP fraud it is the victim,
and in both cases the script is audible.

## 5. Interaction with vulnerability

5.1 APP fraud is not evenly distributed. Fraudsters select for
victims whose circumstances reduce their ability to detect the
deception or resist the pressure, and a material share of reported
matters involve customers with characteristics of vulnerability.
The romance and social engineering typology at TY-06 addresses the
grooming-based subset in detail. Firms should expect their APP
victim population to overlap substantially with their vulnerable
customer population, and should design intervention conversations
accordingly.

## 6. Use of this report

6.1 Firms should test their payment journey controls against the
indicator families at §4 and their receiving-side arrangements
against TY-01 and SG-01. The Authority's expectations for the
treatment of APP victims after the event, including reimbursement
practice, are examined in the thematic review series; this report
confines itself to the typology.

6.2 This report is descriptive of matters reported to the
Authority. Networks and scripts adapt, and firms should treat the
patterns here as a floor for calibration rather than a ceiling.

**End of TY-03.**
