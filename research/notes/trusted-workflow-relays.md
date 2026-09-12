---
title: 'Trusted Workflow Relays:'
id: trusted-workflow-relays
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:36:04.565639Z'
updated: '2026-09-12T21:44:34.430046Z'
source: https://arxiv.org/abs/2608.17361v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:36:04.565226Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2608.17361v1 (2026): uses 14 ATT&CK technique-ID occurrences (with
  sub-techniques); ATT&CK release declaration classified as major_only.'
raw_file: raw/trusted-workflow-relays.pdf
doi: arXiv:2608.17361v1
---

Trusted Workflow Relays:
Cross-Tenant Email Abuse and Composable Red Team Initial-Access
Primitives in Multi-Tenant Clouds
Priyank Nigam
Microsoft Security Engineering
August 2026
Abstract
Cloud applications routinely send notifications through
provider-operated mail identities. This delegation is con-
venient and usually improves deliverability, but it also
separates the actor who supplies notification parameters
from the service principal that originates the message.
We present a case study of this trusted workflow relay
pattern in multi-tenant cloud services. In three respon-
sibly disclosed and remediated cross-tenant notification
workflows, an authenticated actor could influence recip-
ients across tenant boundaries and, to different degrees,
control message content that a trusted provider service de-
livered. In the first workflow, backend requests bypassed a
user-interface length restriction, raw HTML and CSS sur-
vived into the delivered message, HTTP(S) links rendered,
and CSS could visually suppress service-controlled text.
Tested iframes and non-web URI schemes were rejected.
A second workflow combined missing recipient-tenant val-
idation with attacker-controlled subject and HTML fields.
A third workflow, an approval application, combined weak
access control, sequential object identifiers, missing ac-
tion authorization, and incomplete token validation, and
shows how notification abuse composes with authorization
failures.
The pattern is analogous to a classical unauthenticated
SMTP open relay, but the failure has moved up the stack:
the initiating actor is authenticated and the cloud provider
is the legitimate sender, yet application-layer authoriza-
tion still fails to constrain who may cause it to send what
to whom. We formally define a trusted workflow relay
as a delivered, service-authentic message for which the
application-level send-authorization predicate is false. We
then give a test matrix for notification pipelines, map the
primitive to MITRE ATT&CK techniques for attachment-
free phishing, and connect it to device-authorization phish-
ing documented in RFC 8628 and recent threat campaigns.
The results show why the standard email authentica-
tion mechanisms—Sender Policy Framework (SPF), Do-
mainKeys Identified Mail (DKIM), and Domain-based
Message Authentication, Reporting, and Conformance
(DMARC)—can correctly authenticate a message yet can-
not establish that an application-level send was autho-
rized. We conclude with controls for tenant binding, typed
templates, object-level authorization, token audience vali-
dation, and identity telemetry.
1
Introduction
Traditional E-mail relays operate at the transport layer.
An improperly configured relay may accept mail from
an unauthorized party and forward it to an arbitrary
recipient. Cloud software has shifted much business email
origination above that layer. A user clicks share, invite,
approve, or notify; an application backend then constructs
a message and a provider-controlled service identity sends
it. The resulting message is not forged. Its infrastructure
and domain authentication can be entirely legitimate.
This change creates a different authorization problem.
A multi-tenant application must bind four elements before
sending: the initiating principal, its tenant, the target
object and recipient, and the content permitted in the
notification. A failure at any of these boundaries can turn
a legitimate notification service into an application-layer
relay. Existing email authentication mechanisms do not
make this decision. The Sender Policy Framework (SPF)
authorizes the hosts that may send mail for a domain,
DomainKeys Identified Mail (DKIM) attaches a crypto-
graphic signature that associates a signing domain with
message content, and Domain-based Message Authentica-
tion, Reporting, and Conformance (DMARC) evaluates
whether those identifiers align with the author domain
and applies the domain owner’s policy [6, 1, 5]. When the
provider itself originates the message, those checks can
pass while the business operation that caused the send
was unauthorized.
This paper reports findings from security assessments
of multi-tenant cloud workflows and places them in a com-
mon model. The specific vulnerabilities were responsibly
disclosed and remediated. Product details and identifiers
that are not needed to understand the failure mode are
generalized. Our contributions are:
• a formal definition of the trusted workflow relay as
the conjunction of service-authentic delivery and failed
1
arXiv:2608.17361v1  [cs.CR]  18 Aug 2026


---

application-level authorization, together with a decom-
position of the required authorization predicates;
• a qualitative case study of three cross-tenant notifi-
cation workflows, including a content-rendering test
matrix derived from delivered messages;
• an analysis of how object-level authorization and token-
validation flaws in the third workflow compose with
trusted notification channels;
• a mapping of the primitive to MITRE ATT&CK for
attachment-free phishing that identifies both the tech-
niques it never needs and the recommended mitigation
that fails by construction; and
• a set of engineering and detection controls spanning no-
tification origination, content rendering, authorization,
and identity telemetry.
2
Background and Threat Model
2.1
Formal definition: from SMTP relays
to workflow relays
A classical SMTP open relay accepts and forwards mes-
sages without an appropriate authorization decision. The
workflows studied here did not expose a general SMTP in-
terface. Instead, an authenticated user invoked a business
operation, and a backend service generated mail through
a privileged provider identity. We use relay to describe
the security effect, not protocol equivalence.
Let u be an initiating principal in tenant Tu, r a recipi-
ent in tenant Tr, o a shared or actioned object, c attacker-
influenced content, and s a trusted sending service. Let
q = (u, Tu, o, r, Tr, c) denote a notification request. The
application’s authorization decision for that request is
Authorizeds(q) ≡MayAct(u, Tu, o)
∧MayTarget(u, Tu, o, r, Tr)
∧MayOriginates(u, Tu, o, r, Tr)
∧SafeContents(c).
(1)
Here, the predicates respectively authorize the actor’s
operation on the object, the recipient relationship, the
privileged notification side effect, and the content admit-
ted to the service-owned template.
Definition (trusted workflow relay).
A service s
exposes a trusted workflow relay if there exists a request
q and message m such that
∃q, m : Delivereds(q, m)
∧Authentics(m) ∧¬Authorizeds(q)
(2)
Authentics(m) means that the message genuinely orig-
inates from and authenticates as the provider service;
it does not assert that the initiating application action
was authorized. Thus, “trusted” describes the message’s
service identity, while “relay” describes the unauthorized
use of that identity’s delivery authority. Equation 2 is
satisfied when any predicate in Equation 1 fails. The most
consequential cases combine a recipient-boundary failure
with a content-boundary failure.
2.2
Attacker capabilities
Our primary attacker has a valid low-privilege account in
a tenant they control or an otherwise ordinary consumer
(non-enterprise) account accepted by the target service.
The attacker can use browser developer tools or an inter-
cepting proxy to replay and modify requests that their
account is already able to issue. The attacker does not
possess a provider signing key, compromise a mail server,
or control the recipient tenant. For the approval-workflow
case, we additionally consider an attacker able to alter a
numeric object identifier in a URL.
We assume the recipient’s mail system may use SPF,
DKIM, DMARC, reputation, and content analysis. These
controls are relevant but cannot replace authorization at
the workflow that originates the message. Prior work
has shown that provider handling and user-interface cues
materially affect spoofing outcomes [4]; our work examines
the distinct case in which the sender is authentic but the
send authority is over-broad.
3
Methodology
3.1
Assessment procedure
We assessed the workflows as black-box application sur-
faces. For each workflow, we first exercised its intended
user interface and captured the corresponding HTTP re-
quest. We then changed one security-relevant field at a
time and observed (1) the HTTP response, (2) whether a
message was delivered to a researcher-controlled mailbox,
and (3) how the resulting body rendered in the tested
mail client. The input classes were recipient tenant, di-
rectory object identifier, subject, body length, markup,
style, embedded frame, and link scheme.
Tests used accounts, tenants, objects, and mailboxes
controlled by or explicitly available to the researcher. We
used benign proof text and links. We did not send unso-
licited messages, collect credentials, or use delivered mes-
sages for a live phishing campaign. In the approval work-
flow, a missing authorization check on a state-changing
action was identified but not exercised against a real
pending record; we therefore report that consequence as
potential impact, not an observed state change.
3.2
Evidence classification
We label evidence in three categories. Observed means
a controlled request or delivered message demonstrated
the behavior. Inferred means a reachable code or UI path
supported an impact that was deliberately not exercised.
Literature-derived means the claim comes from standards,
2


---

vendor guidance, or threat-intelligence reporting. This
distinction is important because successful delivery does
not itself establish inbox placement across providers, user
interaction, or account compromise.
3.3
Reproducibility constraints
The services were remediated after disclosure, so the orig-
inal behavior is not expected to reproduce on current
production deployments. To avoid exposing tenant data
or stale exploit details, this paper includes sanitized re-
quest shapes and the test matrix rather than raw cap-
tures. Exact product versions were not available from the
user-facing services. These constraints favor a qualitative
security case study over a prevalence measurement.
4
Case Study:
Notification Con-
tent and Client Rendering
4.1
Workflow and boundary failure
Workflow A was a multi-tenant application-sharing work-
flow. The normal UI allowed a user to choose a principal,
assign a view role, and optionally add a short custom
message. A provider-operated backend generated the no-
tification; the user did not connect to SMTP or choose
the envelope sender. The relevant request shape was:
{"put":[{"properties":{
"NotifyShareTargetOption":"Notify",
"roleName":"CanView",
"principal":{"id":"<recipient-object-id>",
"type":"User"}}}],
"emailCustomizations":{"message":"<content>"}}
The UI attempted to constrain message length and
rejected obvious HTML characters. Those checks did not
define the backend’s effective policy. A direct request with
more than 200 characters received a success response, and
raw markup supplied to the backend appeared in delivered
messages.
4.2
Rendering matrix
Table 1 summarizes the controlled tests represented in the
research artifacts. “Rendered” means the supplied feature
had the intended visual effect in the tested delivered
message. A failed test narrows the observed surface; it
does not prove that all variants of that class were blocked.
The key result was not script execution. Email clients
commonly disable JavaScript, yet HTML and CSS remain
security-relevant presentation languages. Prior client re-
search has likewise shown that HTML/CSS interpretation
can create security consequences without JavaScript [14].
Here, CSS could hide service-controlled context and place
attacker-controlled content in its visual position. This
creates an integrity failure in the message template even
when active content such as an iframe is blocked.
4.3
Impact and remediation
The provider, not the initiating user, authenticated the
resulting mail. Thus, anti-spoofing success was an ex-
pected property of the message rather than evidence that
its custom content had been authorized. We observed
delivery to a researcher-controlled mailbox and a recog-
nizable provider sender presentation. We did not conduct
a controlled comparison of spam verdicts or inbox rates
and make no quantitative deliverability claim.
The durable fix is to enforce policy at the server-side
composition boundary: bind recipients to authorized ten-
ant relationships; treat custom text as data; escape it for
the output context; and expose a small typed template vo-
cabulary instead of arbitrary HTML or CSS. A client-side
character check or length limit is not a security boundary.
5
Case
Study:
Cross-Tenant
Trusted-Sender Abuse
Workflow B was a second Microsoft-hosted, multi-tenant
collaboration workflow. A share operation accepted both
a directory object identifier and an email address, then
sent a notification from a provider system domain. The
assessed backend did not verify that the recipient resolved
inside the sharer’s tenant or another explicitly authorized
collaboration relationship.
It also accepted a custom
subject and HTML message body. The request can be
represented as:
POST /api/project/share
{
"AADObjectId": "<supplied-guid>",
"Email": "recipient@other-tenant.example",
"CustomSubject": "<supplied-subject>",
"CustomMessage": "<supplied-html>"
}
The recipient-boundary and content-boundary failures
composed. An actor in one tenant could cause the provider
workflow to originate a customized message to a mailbox
in another tenant. In contrast to lookalike-domain or
From-header spoofing, the provider system was the actual
originator. SPF, DKIM, and DMARC are therefore not
expected to reject the message merely because a tenant
user abused the application that requested it. This is con-
sistent with the standards’ scope: domain authentication
does not validate the legitimacy of message content or the
application-level decision to send it [6, 1, 5].
The remediation validated both the email address and
directory object identifier against the host tenant before
sending and rejected recipients outside the authorized
boundary. Both values must be resolved and compared
server-side; checking only a display string or trusting a
caller-supplied tenant identifier leaves room for inconsis-
tent bindings.
3


---

Table 1: Observed behavior in Workflow A. Results are qualitative and specific to the tested workflow and client at
assessment time.
Test
Result
Security interpretation
Body longer than UI limit
Accepted
Client-side length policy was not enforced by the backend.
Plain text
Rendered
Baseline custom-message behavior.
Encoded markup
Not rendered as
markup
The tested encoded representation did not become active HTML.
Raw HTML tags
Rendered
Message data reached an HTML-capable sink.
Arbitrary iframe
Blocked
The tested frame did not render.
HTTP(S) link
Rendered
Attacker-selected web destination was clickable.
Non-web URI schemes
Blocked
Tested file, FTP, SSH, and other schemes did not render as usable
links.
CSS rules
Applied
Attacker-controlled style affected presentation.
CSS positioning
Applied
Content could be repositioned relative to trusted template elements.
Iframe with tested allow-listed
host
Blocked
No frame execution was observed in that variant.
Hide service-controlled text
Applied
CSS could suppress or visually truncate trusted explanatory text.
Combined HTML, CSS, and
HTTPS call to action
Rendered
A provider-originated message could present attacker-selected copy
and a prominent external link.
6
Case Study: Authorization Com-
position in an Approval Work-
flow
Workflow C was a third cross-tenant notification work-
flow. It managed invoice or access-approval records, and
its approve and reject actions caused a provider identity
to notify requesters and approvers who could sit outside
the acting account’s tenant. Its administration page was
intended for employees and a limited set of onboarded sup-
pliers, but an ordinary consumer (non-enterprise)account
could reach the page. Records were selected by a sequen-
tial requestId:
GET /Administration/AccessRequestDetails.aspx
?type=approval&requestId=<N>
Changing N exposed records outside the account’s au-
thorization scope. This is an insecure direct object ref-
erence: user-controlled input selected an object without
a corresponding object-level authorization decision [13].
The page also exposed approve and reject actions with-
out an adequate role check. We did not exercise those
actions on live records. Because such actions generated
trusted workflow notifications, unauthorized mutation
could also cause provider-originated mail with business
consequences.
The same assessment surfaced an incomplete access-
token validation pattern. A multi-tenant API cannot treat
a valid signature or tenant claim as sufficient. A resource
server must verify that the token’s aud claim identifies that
resource; otherwise a token minted for another application
may be accepted by a confused deputy [8, 10]. It must
then authorize the subject and calling application for the
selected tenant, object, and action.
This case illustrates composition. A valid identity is
not necessarily an authorized employee; an authenticated
user is not necessarily allowed to read the selected object;
permission to read one object does not imply permission
to change it; and permission to change an object does not
automatically justify sending a notification. Authorization
should be deny-by-default and evaluated on every request
[12].
7
Formal Definition and Boundary
Model
Equation 2 separates the property established by sender
authentication, Authentics(m), from the application au-
thorization property that must hold before delivery,
Authorizeds(q). Across the cases, that authorization prop-
erty crosses several independently managed boundaries.
Table 2 operationalizes the formal definition as a review
taxonomy.
The model also explains why individually reasonable
controls can fail in composition. A sanitizer may block
iframes but still permit CSS that hides trusted text. A
mail gateway may correctly trust the sending domain but
lack the tenant context needed to judge the send. An API
may validate a token cryptographically but accept the
wrong audience. Effective review therefore follows data
and authority from the initiating request through object
access, template composition, mail origination, and client
rendering.
4


---

Table 2: Boundary-oriented review model for cloud notification workflows.
Boundary
Failure pattern
Required invariant
Initiator
Any authenticated or consumer
(non-enterprise)identity
is
treated as an approved actor.
Authorize immutable subject and tenant identifiers for the
operation.
Object
Caller-supplied or sequential IDs
select records outside the actor’s
scope.
Enforce object-level authorization after object resolution,
for reads and writes.
Recipient
Email and directory identifiers
are accepted without tenant
binding.
Resolve both values server-side and verify an allowed same-
tenant or explicit cross-tenant relationship.
Content
User data reaches subject or
HTML/CSS sinks with only UI
validation.
Use contextual encoding and typed templates; prohibit ar-
bitrary style and markup.
Origination
A privileged service identity
signs mail caused by a weakly
authorized action.
Treat sending as a privileged side effect with its own policy
and audit event.
Token
Signature or issuer is checked
but audience, tenant, subject, or
actor is not.
Use maintained middleware and validate audience plus con-
textual authorization claims.
Telemetry
Logs record only the service
sender, obscuring the initiating
tenant user.
Correlate initiator, tenant, object, recipient tenant, tem-
plate, and message identifier.
8
Composition with Device-Code
Phishing
Device authorization is not a vulnerability in the assessed
notification workflows. It is a standardized OAuth flow for
devices that lack a suitable browser or input mechanism
[2]. We discuss it because public campaigns show how a
trusted delivery channel can compose with a legitimate
identity flow to create initial access.
In the legitimate flow, a client obtains a device_code,
a short user_code, and a verification URI. A user au-
thenticates on a second device and enters the user code
while the original client polls the token endpoint. The
client holding the device code receives the resulting to-
ken. RFC 8628 explicitly identifies remote phishing: an
attacker can initiate the flow and convince a target to
enter the attacker’s code at the genuine verification page
[2].
The resulting composition is:
1. the attacker initiates a device authorization request;
2. a trusted or convincing notification carries the legit-
imate verification URI and attacker-controlled user
code;
3. the victim authenticates and satisfies MFA on provider
infrastructure;
4. the attacker, who retains the device code, polls the
token endpoint and receives tokens for the approved
client and scope.
Microsoft and Volexity documented 2024–2025 cam-
paigns using this pattern, including real-time rapport
building, Microsoft Teams and external-tenant themes,
and automatically refreshed device codes [11, 3]. Microsoft
further reported use of the Microsoft Authentication Bro-
ker client ID to obtain a token for device registration,
register an actor-controlled device, and obtain a Primary
Refresh Token [11]. These are literature-derived obser-
vations; our notification testing did not request victim
tokens or reproduce campaign post-compromise behavior.
9
Mapping to MITRE ATT&CK
The trusted workflow relay is not a new adversary tech-
nique. It is a new way to satisfy the preconditions of
existing ones, and it does so without an attachment. Ta-
ble 3 maps the primitive and its device-code composition
onto ATT&CK for Enterprise [15]. The mapping is ana-
lytic: it describes how the assessed defects would be used,
and only the token-related rows are supported by public
campaign reporting [11, 3].
Techniques the primitive never needs.
Spearphish-
ing Attachment (T1566.001) and User Execution: Ma-
licious File (T1204.002) do not appear.
There is no
file to detonate, so attachment sandboxing and the An-
tivirus/Antimalware mitigation (M1049) have no object
to evaluate, and detection analytics keyed to attachment
metadata or post-download process lineage never fire.
Nothing needs to execute on the endpoint for the primi-
tive to succeed; the payload is a link and a pretext.
5


---

Table 3: Attachment-free phishing mapped to MITRE ATT&CK for Enterprise. Every delivered message in the case
studies carried text, markup, and links only.
Tactic
Technique (ID)
Realization through a trusted workflow relay
Resource Develop-
ment
Establish Accounts:
Cloud Ac-
counts (T1585.003)
The actor registers an ordinary tenant or consumer (non-
enterprise) account that the multi-tenant service accepts;
no mail server, domain, or signing key is acquired.
Resource Develop-
ment
Acquire Infrastructure: Web Ser-
vices (T1583.006)
The provider’s own notification pipeline replaces attacker-
controlled sending infrastructure, so no lookalike domain
(T1583.001) is registered or aged.
Initial Access
Phishing:
Spearphishing
Link
(T1566.002)
Attacker-supplied HTTP(S) anchors survived into the de-
livered body (Table 1). ATT&CK places consent phishing
and device-code phishing under this sub-technique [16].
Initial Access
Phishing: Spearphishing via Service
(T1566.003)
ATT&CK already records abuse of the notification features
of legitimate file-sharing services [17]. The relay generalizes
that behavior to first-party cloud workflows, but the message
arrives through the enterprise mail channel rather than
around it.
Initial Access
Trusted Relationship (T1199)
The abused trust is the recipient’s trust in the provider’s
sending identity rather than delegated administrative access
[19]; adjacent to, not identical with, ATT&CK’s partner
and service-provider framing.
Defense Evasion
Impersonation (T1656)
Attacker-controlled subject text and CSS that visually sup-
presses service-controlled text let the message read as a
first-party notice.
Execution
User Execution:
Malicious Link
(T1204.001)
The victim clicks inside a message that both the mail gate-
way and prior user training treat as authentic provider
correspondence.
Credential Access
Steal Application Access Token
(T1528)
A device-authorization or consent link converts one click
into tokens without a credential prompt [18].
Persistence, Lat-
eral Movement
Valid Accounts:
Cloud Accounts
(T1078.004); Application Access To-
ken (T1550.001)
Follow-on access uses issued tokens and registered devices
rather than malware, so endpoint-centric detection has no
artifact.
Where the recommended mitigation is a no-op.
ATT&CK’s Software Configuration mitigation (M1054)
for T1566.002 recommends SPF, DKIM, and DMARC
to filter messages by sender-domain validity [16]. Equa-
tion 2 explains why that mitigation cannot help here:
Authentics(m) holds by construction, so every sender-
validity check the mitigation prescribes returns a pass.
The remaining mapped mitigations—User Training
(M1017), Restrict Web-Based Content (M1021), and Au-
dit (M1047)—are receiver-side and partial. The control
that would actually falsify the technique, provider-side
send authorization, has no ATT&CK mitigation, because
ATT&CK models adversary behavior against a defending
enterprise rather than authorization defects inside the
sending service.
Detection implications.
Because the attachment and
endpoint stages are absent, detection weight shifts to
three signals: link analysis on messages that pass domain
authentication, sender-provenance telemetry that identi-
fies the initiating tenant behind a service identity, and
identity telemetry for the token follow-on described in
Section 8. Only the provider can emit the second signal,
which is why the telemetry row of Table 2 is a detection
prerequisite and not merely an engineering hygiene item.
10
Defensive Recommendations
10.1
Notification pipeline
• Model notification origination as a privileged action.
Check initiator, tenant, object, recipient relationship,
and template policy immediately before enqueueing a
message.
• Resolve recipient email and immutable directory iden-
tifiers server-side. Reject inconsistent pairs and cross-
tenant recipients unless a documented collaboration
policy explicitly permits them.
• Replace arbitrary subject and HTML fields with typed
templates. Encode text for its output context, allow
only server-owned links or validated destinations, and
do not allow tenant input to define CSS.
• Apply server-side length and schema constraints. Ex-
ercise the backend directly in tests; UI restrictions are
6


---

usability controls, not authorization.
• Record the causal chain: initiating principal and ten-
ant, object, recipient and tenant, template identifier,
message identifier, and authorization decision.
10.2
Application and identity controls
Every object read and state change requires an authoriza-
tion decision after the server resolves the target object.
Random identifiers reduce opportunistic enumeration but
do not replace access control. For access tokens, use main-
tained identity middleware and validate signature, issuer,
lifetime, audience, tenant, subject, calling application,
and required scope or role as applicable [8, 10].
For organizations that do not need device authoriza-
tion, Microsoft recommends blocking it through Condi-
tional Access. Where it is required, scope it narrowly
and first use report-only policy or sign-in logs to es-
tablish legitimate usage [9]. Detection should baseline
and
correlate
authenticationProtocol=deviceCode,
originalTransferMethod=deviceCodeFlow, device reg-
istration, anomalous token use, and access to device-login
URLs [3, 9]. A suspected compromise requires token/ses-
sion revocation and investigation of newly registered de-
vices; revocation can take several minutes to propagate
[7].
10.3
Mail receiver controls
Receivers should retain SPF, DKIM, and DMARC be-
cause they address important forms of spoofing. They
should not treat authentication success as proof that ar-
bitrary content authorized by a multi-tenant application
is benign. Provider and SaaS notification streams benefit
from behavior-based controls such as unusual recipient-
tenant fan-out, novel external links, content-template
divergence, and reputation at a finer granularity than the
parent sending domain. Providers are in the best posi-
tion to expose an authenticated initiating-tenant signal
to these controls.
11
Responsible
Disclosure
and
Ethics
The case-study vulnerabilities were reported through re-
sponsible disclosure and were remediated before this
preprint.
Testing was limited to benign content and
researcher-controlled resources. No production records
were modified to prove the inferred approval impact, and
no credentials or tokens were solicited. The paper omits
live tenant identifiers, hostnames, and record values that
are not necessary to reproduce the reasoning. Sanitization
aims to preserve the engineering lesson while reducing
risk to historical or analogous deployments.
12
Limitations
This is a small, purposive case study, not a survey of cloud-
service prevalence. The tested services, mail client, and
production versions may have changed, and remediation
prevents current replication. The deck artifacts did not
preserve a complete set of raw Authentication-Results
headers, spam verdicts, repeated trials, or cross-provider
delivery measurements. Consequently, we report observed
delivery and rendering only and do not estimate inbox
rate or click-through.
Some system details remain anonymized, which limits
independent reproduction. The content tests establish
the behavior of the tested payloads, not the complete
HTML/CSS or URI-scheme policy. The approval action’s
missing authorization was not exercised on a live pending
record.
The ATT&CK mapping is an analytic corre-
spondence between the assessed defects and published
technique definitions; we did not observe an adversary
executing these techniques through the assessed work-
flows, and technique identifiers may be renumbered in
later ATT&CK releases. Finally, the device-code section
synthesizes standards and public incident reporting rather
than presenting a new campaign or user study.
13
Conclusion
Cloud notification systems move email authority from
end users to privileged service identities. That design can
improve security and reliability, but only if the applica-
tion strongly binds the initiating principal, tenant, object,
recipient, and permitted content. The assessed workflows
broke those bindings in different ways: cross-tenant recip-
ients were insufficiently validated, rich content reached
mail-client rendering sinks, object identifiers were not
authorization boundaries, and token validation omitted
essential context.
The central defensive lesson is that message authentic-
ity and send authorization are separate properties. SPF,
DKIM, and DMARC may all work as designed while a
trusted application sends an attacker-influenced message.
Providers should make the application-level authorization
decision explicit, test it at the backend, carry its prove-
nance into telemetry, and constrain notification content
with typed templates. Defenders should then correlate
that provenance with identity flows, especially legitimate
but phishable mechanisms such as OAuth device autho-
rization.
Acknowledgments and Disclaimer
The author thanks the engineering teams that investigated
and remediated the reported issues. The views expressed
are the author’s own and do not necessarily represent the
views of Microsoft. Product and company names are used
for identification only.
7


---

References
[1] Dave Crocker, Tony Hansen, and Murray Kucherawy.
Domainkeys identified mail (dkim) signatures. RFC
6376, Internet Engineering Task Force, September
2011.
[2] William Denniss, John Bradley, Michael B. Jones,
and Hannes Tschofenig. Oauth 2.0 device authoriza-
tion grant. RFC 8628, Internet Engineering Task
Force, August 2019.
[3] Charlie Gardner, Steven Adair, and Tom Lancaster.
Multiple russian threat actors targeting microsoft
device code authentication. Volexity Threat Research,
February 2025. Accessed August 13, 2026.
[4] Hang Hu and Gang Wang. Revisiting email spoofing
attacks. arXiv preprint arXiv:1801.00853, 2018.
[5] Internet Engineering Task Force.
Domain-based
message authentication, reporting, and conformance
(dmarc). RFC 9989, Internet Engineering Task Force,
2026.
[6] Scott Kitterman. Sender policy framework (spf) for
authorizing use of domains in email, version 1. RFC
7208, Internet Engineering Task Force, April 2014.
[7] Microsoft.
user: revokesigninsessions.
Microsoft
Graph v1.0 Documentation, 2025. Accessed August
13, 2026.
[8] Microsoft. Access tokens in the microsoft identity
platform. Microsoft Learn, 2026. Accessed August
13, 2026.
[9] Microsoft. Authentication flows as a condition in
conditional access policy.
Microsoft Learn, 2026.
Accessed August 13, 2026.
[10] Microsoft. Secure applications and apis by validating
claims. Microsoft Learn, 2026. Accessed August 13,
2026.
[11] Microsoft Threat Intelligence. Storm-2372 conducts
device code phishing campaign. Microsoft Security
Blog, February 2025. Updated July 31, 2026; accessed
August 13, 2026.
[12] OWASP Foundation.
Authorization cheat sheet,
2026. Accessed August 13, 2026.
[13] OWASP Foundation. Testing for insecure direct ob-
ject references. Web Security Testing Guide, WSTG-
ATHZ-04, 2026. Accessed August 13, 2026.
[14] Damian Poddebniak, Christian Dresen, Jens M"uller,
Fabian Ising, Sebastian Schinzel, Simon Friedberger,
Juraj Somorovsky, and J"org Schwenk. Efail: Break-
ing s/mime and openpgp email encryption using ex-
filtration channels. In 27th USENIX Security Sym-
posium, pages 549–566. USENIX Association, 2018.
[15] The MITRE Corporation. MITRE ATT&CK for
enterprise, 2026. Version 19; accessed August 17,
2026.
[16] The MITRE Corporation. Phishing: Spearphishing
link (t1566.002). MITRE ATT&CK for Enterprise,
2026. Accessed August 17, 2026.
[17] The MITRE Corporation.
Phishing: Spearphish-
ing via service (t1566.003). MITRE ATT&CK for
Enterprise, 2026. Accessed August 17, 2026.
[18] The MITRE Corporation. Steal application access
token (t1528).
MITRE ATT&CK for Enterprise,
2026. Accessed August 17, 2026.
[19] The MITRE Corporation.
Trusted relationship
(t1199). MITRE ATT&CK for Enterprise, 2026. Ac-
cessed August 17, 2026.
8
