SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai.

# TY-07 — Typology Report: Account Takeover

**Issued by the Authority · Typology series · Reference TY-07**

## 1. Purpose

1.1 This report describes account takeover: fraud in which the
fraudster obtains control of a genuine customer's access
credentials or channel and operates the account as if they were the
customer. It sits on the opposite side of a line that matters to
every downstream process: in the typologies at TY-02 and TY-03 the
customer authorises the payment under coercion or deception,
whereas here the customer authorises nothing — the authentication
is genuine and the person behind it is not.

1.2 The line is drawn here because reported matters show it drawn
badly in practice. Takeover cases handled as authorised disputes,
and coerced-authorisation cases of the kind TY-02 describes handled
as takeover, each produce the wrong investigation, the wrong
customer treatment and the wrong control feedback. The first task
of a firm receiving a disputed payment claim is to establish which
side of the line the facts sit.

## 2. Acquisition of control

2.1 Credential acquisition routes in reported matters group into
four families. Phishing and its voice and message variants harvest
credentials by imitating the firm — and section 2 of the Fraud Act
2006 (the extract at OGL-0001) is engaged at this first step, the
imitation being a false representation made to obtain the
credentials, with section 2(5) confirming that a representation
submitted to a credential-harvesting page is a representation
notwithstanding that only a system receives it. Malware and remote
access tools capture credentials or sessions from the customer's
own device, frequently installed under the pretext of a support
call. Credential stuffing replays username and password pairs
breached elsewhere against the firm's channels, harvesting the
customers who reuse them. Interception attacks defeat the second
factor itself, most prominently by SIM swap: the fraudster procures
the transfer of the customer's mobile number to their own device,
and one-time codes follow the number.

2.2 The families differ in what the firm can see at login. Stuffing
arrives at volume from automation, with its own traffic signature.
Phished and stuffed credentials are typically used from a device
and network the customer has never used. Malware and remote access
operate from the customer's genuine device, defeating device
recognition entirely; the observable anomalies move to session
behaviour — navigation the customer never performs, dwell patterns
of someone reading an unfamiliar interface, tooling artefacts of
remote control.

## 3. Behaviour after takeover

3.1 The post-takeover sequence in reported matters is compact and
consistent: reconnaissance of balances and products; changes that
consolidate control and blind the customer — contact details
redirected, notification preferences quietened, limits raised; then
extraction, through new payees receiving rapid transfers, and
onward into the mule structures described in TY-01.

3.2 The control changes are the takeover's most distinctive
signature and its most valuable interception point. A genuine
customer changes an email address, or registers a new device, or
raises a payment limit, as isolated events at low frequency. The
cluster — new device, new contact details, quietened alerts, new
payee, maximum payment, all within one session or one day — is
close to unique to this typology, and it occurs before the money
moves. The Authority's expectations for monitoring designed around
event sequences of this kind are set out in the transaction
monitoring guidance at SG-03.

3.3 Extraction itself then resembles the first-generation mule
pattern of TY-01 §5.1 seen from the sending side: a first material
outbound payment inconsistent with all prior activity, to a payee
created minutes earlier, at or near the available balance, repeated
until the balance or the limit is exhausted.

## 4. Distinguishing takeover from coerced authorisation

4.1 The distinction with TY-02's coerced and deceived authorisation
matters most in the remote access variant, where the two typologies
produce near-identical technical evidence: the customer's device,
the customer's network, a remote access tool present. The
differentiating facts are behavioural. In takeover the customer is
absent from the session and typically discovers the fraud later; in
coerced authorisation the customer is present, on a call, being
walked through the journey, and the firm's own contact records
often show the customer reachable and in conversation at the moment
of payment. Interviewing for which of the two occurred — rather
than assuming from the technical artefacts — is the practice the
Authority expects.

## 5. Indicators

5.1 At authentication: credential-stuffing traffic signatures;
logins from new device, network and location combinations; second-
factor deliveries shortly after a mobile number change; impossible
travel between sessions.

5.2 In session: navigation and dwell anomalies against the
customer's established behaviour; remote-access tooling artefacts;
control changes at abnormal frequency, and above all the §3.2
cluster.

5.3 At payment: the §3.3 extraction pattern — new payee, immediate
material transfer, repetition to exhaustion — evaluated jointly
with the authentication and session context rather than as a
standalone payment score. A payment unremarkable in isolation is
remarkable minutes after a device registration and a notification
change, and monitoring that cannot join those events across their
different source systems will pass what it should hold. The data
completeness lesson of TR-01 §3.4 applies with full force: the
joining is only as good as the feeds.

## 6. Use of this report

6.1 Firms should map their detection coverage against the four
acquisition families at §2.1, test whether their monitoring can
assemble the §3.2 cluster across source systems, and examine how
their disputed payment intake distinguishes this typology from
TY-02. This report is descriptive of reported matters; acquisition
techniques turn over quickly, the post-takeover sequence at §3.1
has been durable, and controls anchored on the sequence rather
than the technique of the season age accordingly.

**End of TY-07.**
