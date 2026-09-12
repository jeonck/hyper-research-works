---
title: 'DISINFOX: an open-source threat exchange platform'
id: disinfox-an-open-source-threat-exchange-platform
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:35:51.173336Z'
updated: '2026-09-12T21:44:33.176426Z'
source: https://arxiv.org/abs/2504.01803v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:35:51.172885Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2504.01803v1: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/disinfox-an-open-source-threat-exchange-platform.pdf
doi: arXiv:2504.01803v1
---

DISINFOX: an open-source threat exchange platform
serving intelligence on disinformation and influence
operations
Felipe S´anchez Gonz´aleza, Javier Pastor Galindob,∗, Jos´e A.
Ruip´erez-Valientea
aDepartment of Information and Communications Engineering, University of Murcia,
Spain
bDepartment of Computer Systems Engineering, Universidad Politecnica de Madrid,
Spain
Abstract
This paper introduces DISINFOX, an open-source threat intelligence ex-
change platform for the structured collection, management, and dissemi-
nation of disinformation incidents and influence operations. Analysts can
upload and correlate information manipulation and interference incidents,
while clients can access and analyze the data through an interactive web in-
terface or programmatically via a public API. This facilitates integration with
other vendors, providing a unified view of cybersecurity and disinformation
events.
The solution is fully containerized using Docker, comprising a web-based
frontend for user interaction, a backend REST API for managing core func-
tionalities, and a public API for structured data retrieval, enabling seam-
less integration with existing Cyber Threat Intelligence (CTI) workflows.
In particular, DISINFOX models the incidents through DISARM Tactics,
Techniques, and Procedures (TTPs), a MITRE ATT&CK-like framework for
disinformation, with a custom data model based on the Structured Threat
Information eXpression (STIX2) standard.
As an open-source solution, DISINFOX provides a reproducible and exten-
sible hub for researchers, analysts, and policymakers seeking to enhance the
detection, investigation, and mitigation of disinformation threats. The in-
telligence generated from a custom dataset has been tested and utilized by
a local instance of OpenCTI, a mature CTI platform, via a custom-built
connector, validating the platform with the exchange of more than 100 dis-
∗Corresponding author.
Email address: javier.pastor.galindo@upm.es (Javier Pastor-Galindo).
Preprint submitted to SoftwareX
April 3, 2025
arXiv:2504.01803v1  [cs.CR]  2 Apr 2025


---

information incidents.
Keywords:
Disinformation, Influence Operations, Foreign Information
Manipulation and Interference (FIMI), Cybersecurity, Cyber Threat
Intelligence (CTI), DISARM framework
Metadata
Nr.
Code metadata description
Please fill in this column
C1
Current code version
v1.0
C2
Permanent link to code/repository
used for this code version
https://github.com/
CyberDataLab/disinfox
C3
Permanent
link
to
Reproducible
Capsule
-
C4
Legal Code License
MITLicense
C5
Code versioning system used
git
C6
Software code languages, tools, and
services used
Docker,
Python,
Flask,
jinja2,
HTML, Bootstrap, JavaScript
C7
Compilation requirements, operat-
ing environments & dependencies
Windows/Ubuntu/MacOS, Docker
C8
If available Link to developer docu-
mentation/manual
https://github.com/
CyberDataLab/disinfox/blob/
main/README.md
C9
Support email for questions
felipe.sanchezg@um.es
Table 1: Code metadata
1. Motivation and significance
Disinformation has shaped public opinion throughout history [1]. However,
its impact has dramatically increased with the rise of digital communication
and the unprecedented speed at which false narratives can spread [2]. For
example, the Ukrainian war has demonstrated that disinformation attacks
are not merely side effects of conflicts but key strategic components in mod-
ern geopolitical warfare [3]. As a result, detecting, analyzing, and sharing
disinformation intelligence has become a priority among policymakers and
security organizations [4, 5].
Disinformation incidents are often launched alongside traditional cyberat-
tacks to amplify their impact, destabilize societies, and manipulate pub-
lic perception [6].
Both cyberattacks and disinformation campaigns fre-
quently exploit the same digital channels, making them deeply interconnected
2


---

threats. Thus, disinformation can be considered a cybersecurity concern, as
it complements cyber operations by influencing public opinion, disrupting
critical systems, and obscuring the truth behind digital intrusions [7, 8].
To combat the rise of cybersecurity threats, Cyber Threat Intelligence (CTI)
was established to understand the capabilities, intent, motivations, and tac-
tics, techniques, and procedures (TTPs) of adversaries [9]. CTI feed plat-
forms such as AlienVault OTX and ThreatFox aggregate reports and In-
dicators of Compromise (IoCs) from cybersecurity incidents worldwide us-
ing standardized formats like STIX (Structured Threat Information eXpres-
sion) and TAXII (Trusted Automated Exchange of Intelligence Information)
to enable programmatic data extraction to endpoint CTI platforms such
as OpenCTI and MISP, which integrate these feeds to enhance organiza-
tional awareness, improving both proactive and retrospective cybersecurity
defenses.
While CTI exchange platforms are highly mature in handling conventional
cybersecurity incidents, they do not natively support disinformation inci-
dents. Current efforts to monitor and analyze disinformation rely primarily
on fact-checking repositories such as EUvsDisinfo, which document disin-
formation campaigns in unstructured, natural language reports. This ap-
proach limits automated processing, making large-scale analysis and correla-
tion across incidents nearly infeasible.
Recently, frameworks and ontologies for structuring disinformation incidents
have emerged [10, 11, 12]. Specifically, the DISARM framework [13] provides
a structured, MITRE ATT&CK-like matrix for disinformation TTPs, offer-
ing a direct mapping to STIX objects. This enables a systematic approach
to categorizing disinformation incidents and identifying the strategies used
by malicious actors to manipulate public perception in digital spaces [14].
To address the absence of a dedicated threat exchange for disinformation, this
work introduces DISINFOX (DISINFOrmation threat eXchange), an open-
source threat exchange platform for managing and sharing disinformation
incidents in an interoperable format. DISINFOX provides a dedicated repos-
itory with a custom data model based on DISARM TTPs where disinfor-
mation incidents can be structured, stored, and seamlessly integrated with
traditional CTI solutions.
This structured approach to disinformation intelligence offers several advan-
tages. First, it enables automated processing, facilitating faster detection,
preservation, and analysis of disinformation incidents. Second, by placing
disinformation within the same analytical landscape as conventional cyber
threats, DISINFOX enhances the correlation of influence operations with tra-
ditional cyberattacks, revealing deeper threat patterns.
To achieve this,
DISINFOX implements a modular, containerized system consisting of: (i) a
3


---

web-based frontend for submitting incidents with automatic TTPs extraction
and conducting preliminary analysis with interactive knowledge graphs and
statistics, (ii) a RESTful backend API managing the platform’s core func-
tionalities independently from the user interface, and (iii) a public API for
programmatic access to newly uploaded disinformation incidents, enabling
seamless integration with other CTI platforms.
2. Software description
2.1. Software architecture
DISINFOX has been designed through a service-oriented architecture to max-
imize interoperability while maintaining scalability and modularity. The pub-
licly available implementation1 relies on Docker containers for each service.
Docker containers are a light-weight virtualization technology that provides
isolation for processes while reducing the resource usage of traditional virtual
machines [15].
In particular, the Docker architecture defined for DISINFOX consists of (Fig-
ure 1):
Backend
Browser
DISINFOX
OpenCTI
Connector
Other
DISINFOX
Connector
DISINFOX Docker Compose 
environment
Frontend
Public API
MongoDB
OpenCTI
Other vendor
Reporter
Analyst at Org 2
Analyst at Org 1
Figure 1: DISINFOX architecture
2.1.1. Frontend
A web-based interface designed for non-technical users enables them to share
and view disinformation incidents easily. Built with Python 3 and Flask, it
uses Jinja2 templates to render responsive and visually unified HTML pages
1https://github.com/CyberDataLab/disinfox
4


---

using Bootstrap 5.32. Also, Stixview3 was integrated to generate interactive
STIX2 graphs, providing enhanced visualization of incidents. The frontend
interacts with the backend to upload user-submitted incidents, display plat-
form data, and manage user accounts.
2.1.2. Backend REST API
This component manages STIX2 objects and user data within the platform
while interfacing securely with the data store. Developed with Python 3 and
Flask, it provides a REST interface for handling STIX2 objects, enabling
easy integration with future components and functionalities.
Decoupling
the backend from the frontend ensures the system remains agnostic to fron-
tend technologies. The backend primarily sends STIX-formatted bundles to
the frontend while ingesting and validating incidents submitted in the fron-
tend. Using the STIX2 library, the backend transforms submitted data into
well-formatted STIX2 objects and inserts them directly into the MongoDB
collection. Additionally, this backend validates the public API requests and
serves STIX2 objects to it for external CTI platforms.
2.1.3. Data Store
A MongoDB database was selected for its native capability to store STIX2
objects. Various database types were evaluated, with SQL-based DBMSs
discarded due to the extensive transformation required for STIX2 objects.
Document-oriented DBMSs were preferred for their compatibility with JSON
(the format used by STIX), offering flexibility and simplicity in handling the
data. While graph databases could meet the requirements, their complexity
and steep learning curve rendered them less suitable.
Among document-
oriented DBMSs, MongoDB was chosen for being open-source, providing
robust Python library support, offering an official Docker image, and ranking
as the most popular document database4.
Although DISINFOX is designed to function without preloaded data, allowing
incidents to be added dynamically, the open-source code provide a dataset
of 118 incidents from a variety of sources. This dataset includes incidents
from [16], the DISARM repository5, and several new incidents introduced in
this work.
2https://getbootstrap.com/docs/5.3/getting-started/introduction/
3https://github.com/traut/stixview
4https://db-engines.com/en/ranking/document+store
5https://github.com/DISARMFoundation/DISARMframeworks/blob/main/DISARM_
MASTER_DATA/DISARM_DATA_MASTER.xlsx
5


---

2.1.4. Public REST API
This API, also built with Flask and Python 3 exposes endpoints for program-
matic access to DISINFOX ’s incident repository managed by the backend,
allowing CTI connectors and other software to retrieve data. Users must au-
thenticate requests by including an API key, which is generated in the Profile
section of the frontend interface.
2.1.5. DISINFOX OpenCTI Connector
The publicly available6 Python 3 connector for the OpenCTI platform serves
as a proof of concept for demonstrating DISINFOX ’s interoperability. This
connector retrieves new content from DISINFOX and integrates it seamlessly
into OpenCTI. Thanks to using STIX2 natively, no extra steps for the inges-
tion to OpenCTI are needed.
OpenCTI was chosen as the platform to build the connector and validate
the interoperability of the platform due to several key factors. First, it is
part of the technology stack for disinformation sharing agreed upon by the
EU and the United States [17].
Second, OpenCTI demonstrates a com-
mitment to adapting its platform to better support disinformation manage-
ment [18]. Third, it is the most popular open-source platform capable of
ingesting STIX2. Lastly, OpenCTI offers a comprehensive guide for building
connectors and has strong Python library support through the ctipy library.
While DISINFOX relies on all these modules for full functionality, only the
frontend and the public REST API directly interact with external users,
serving as the primary entry points to the platform.
2.2. Software functionalities
The following subsections detail how a disinformation incident is managed
and shared within DISINFOX. To illustrate the process, a use case related to
the Ukraine war is referenced throughout. Figure 2 outlines the main steps
in the lifecycle, from incident upload to ingestion by other CTI platforms.
These steps were performed to generate 118 disinformation incidents from
the ingestion of DISINFOX’s default dataset 7.
2.2.1. Incident modeling
In this platform, the data model presented in our recent paper [19] is used to
provide a simple, interoperable and structured way to categorize disinforma-
6https://github.com/CyberDataLab/opencti-connector-disinfox
7https://github.com/CyberDataLab/disinfox/blob/main/backend/data/
merged_Foulde_DSRM_additions.csv
6


---

1. Incident
modeling
3. STIX2 transformation
4. Retrieval
2. Incident 
upload
Form
CSV/JSON
Public API
access
DISINFOX's
frontend
visualization
5. DISINFOX
OpenCTI
connector
Incident
Actor
IntrusionSet
ThreatActor
Location
Modeled
disinformation
incident
Incident
data
AttackPattern
Country
Technique
SDOs
SROs
attributed-to
targets
uses
Stored
STIX2 
incident
Figure 2: DISINFOX lifecycle
tion incidents thanks to DISARM TTPs. Therefore, for a Reporter user to
upload an incident to the platform, they must first identify a disinformation
incident and recognize their TTPs.
In the following sections, we use the Bucha massacre disinformation cam-
paign [20] as a real-world example to illustrate how incidents are managed
within DISINFOX. This incident, which took place in April 2022, contained at
least 12 identified DISARM techniques employed by Russia against Ukraine.
2.2.2. Incident upload
After a Reporter user identifies a disinformation incident and extracts the
DISARM TTPs, it can upload it through DISINFOX’s frontend by using one
of two methods:
• Manual individual upload: This is the simplest method for upload-
ing a single identified incident.
As illustrated in Figure 3, the user
needs to fill out a form with the following fields: incident name, de-
scription, date, target countries, threat actors, and identified DISARM
techniques.
• Bulk upload: This method is ideal for importing a large set of disin-
formation incidents. The user can upload either a CSV file8 or a JSON
file containing a STIX2 bundle with the incidents they wish to import.
When using this method, the platform performs an intermediate trans-
formation to format each individual incident, simplifying the creation
of STIX2 objects.
The interactive form provides a user-friendly way for the Reporter to upload
all the necessary information about a disinformation incident. The incident
presented in Section 2.2.1 can be used as an example of how to fill out the
form. Figure 3 illustrates the form fields filled with the required information
for the incident. The title is entered as Bucha massacre at Ukraine, while
8The CSV file must follow a specific template based on the one used in this working
paper [16].
7


---

Figure 3: Manual individual upload form.
8


---

the description contains a summary of the source report. The date field is
filled with April 1, 2022, the date of the first evidence of disinformation.
The target country is Ukraine, as it was the target of the false claims. The
threat actor is identified as Russia, as noted in the source report. Finally, the
DISARM techniques are listed according to those identified by the actions
cited in the report.
Once incidents are uploaded using either method, the platform performs
validation checks on the submitted data and transforms the incidents into
individual STIX2 objects.
2.2.3. Automated STIX2 transformation
Once a disinformation incident is uploaded to DISINFOX, the process of cre-
ating STIX2 objects from incident data is guided by the mapping established
in [19]. The following steps indicate how STIX2 Domain Objects (SDOs) are
built and then connected using STIX2 Relationship Objects (SROs) to rep-
resent a disinformation incident in compliance with the STIX2 standard in
DISINFOX:
1. The uploaded disinformation incident data is used to generate individ-
ual SDOs, which are temporarily stored using Python’s stix2 library.
These include IntrusionSet, ThreatActor, and Location objects.
2. All DISARM techniques are already represented as AttackPattern
SDOs, pre-built and stored in the DISARM.json file9 in STIX2 format.
The DISARM techniques selected in the form are iterated through and
matched against their corresponding entries in the JSON file. For each
matching technique, the JSON object is converted into a Python STIX2
object and temporarily stored.
3. SROs are generated to link the previously created SDOs, establish-
ing relationships between the IntrusionSet and the ThreatActor,
Location, and AttackPattern SDOs.
These connections are rep-
resented using the attributed-to, targets, and uses relationship
types, respectively.
4. All generated SDOs and SROs are inserted into the platform’s database.
The disinformation threat landscape is constructed from the STIX2 objects
stored in the database, forming a structured and interoperable dataset for
further analysis and sharing.
9https://github.com/DISARMFoundation/DISARMframeworks/blob/main/
generated_files/DISARM_STIX/DISARM.json
9


---

Figure 4: DISINFOX dashboard
Figure 5: DISINFOX incident listing
2.2.4. Methods for incidents retrieval
The disinformation incidents stored in DISINFOX can be queried in several
ways, depending on the needs of the user:
• For non-technical and casual users, the most effective way of check-
ing incidents is by looking at DISINFOX’s frontend webpage. The first
utility presented to the user is the dashboard (Figure 4), which of-
fers a quick overview of the current disinformation landscape: the last
disinformation incidents, the most active threat actors and the most
attacked countries with an associated heatmap. In addition, the user
can check the list (Figure 5), to visit any of the incidents stored on the
platform. It shows the name, short description and date of the inci-
dents. Once the user has found an interesting incident, he can view its
details to get more information from it (Figure 6). All the information
about the disinformation incident is shown graphically and intuitively:
name, full description, date, target countries with a map, actors, used
10


---

techniques, a graph showing the STIX2 relationships of this incident
and the raw STIX2 bundle that represents this incident. Additionally,
users can generate a PDF or Word report with all the detailed infor-
mation about the incident to export it to other media and can select
the incident as a favorite, so it can be easily found in its Profile.
• Technical users and specialized CTI developers have the option
to use the Public API to query the platform. Access to the API requires
presenting an API key in the HTTP Authorization header, ensuring
proper access monitoring and security. To obtain an API key, develop-
ers must register on the platform and navigate to the API Key section
in their Profile. Once the API key is obtained, the Public API can be
queried, as indicated in the messages between the connector and the
Public API shown in Figure 7.
The request to the /incidents endpoint should include the newer than
parameter, which takes an ISO 8601 datetime string with microsecond
precision. This parameter specifies the point in time from which the
last edited STIX2 objects will be retrieved, making it particularly useful
for reducing traffic and retrieval times by fetching only new or updated
information from the platform. If all the objects need to be retrieved,
the epoch datetime can be used.
This retrieval method allows developers to easily integrate incident data
into their applications in a RESTful manner. Extending this function-
ality to support the ingestion of new incidents through the API is a
goal for future development.
These two methods are essential to provide a useful way of retrieving incidents
for two different use cases.
2.2.5. Incident synchronization and visualization in OpenCTI
As stated in Section 2.2.4, the Public API eases the work of incident retrieval
for applications that want to use DISINFOX’s incidents, especially to connect
it to other CTI solutions.
To demonstrate this, the proof-of-concept DISINFOX connector for OpenCTI
6.4.210 was developed. Although the DISINFOX connector can be used stan-
dalone with an OpenCTI installation, it is recommended to first install
the DISARM connector11.
The DISARM connector not only inserts all
10https://github.com/CyberDataLab/opencti-connector-disinfox
11https://github.com/OpenCTI-Platform/connectors/tree/master/
external-import/disarm-framework
11


---

Figure 6: Visualization of a disinformation incident at the DISINFOX frontend web page
12


---

AttackPattern SDOs from DISARM into OpenCTI but also provides the
DISARM matrix and other additional objects that enhance the utility of
the DISINFOX connector. This allows the DISINFOX incidents shared with
OpenCTI to be analyzed using the matrix, complementing all the other vi-
sualization options available in OpenCTI.
As Figure 7 shows, this connector works in a very simple way thanks to using
STIX2 natively:
1. The OpenCTI platform registers the connector and performs the first
run of DISINFOX’s connector.
2. DISINFOX connector sends a request to DISINFOX Public API with the
newer than parameter set with the epoch timestamp, as this is the
first run, and all the incidents need to be retrieved. It also includes an
Authorization header with the API key that the user have included
in the .env file, previously obtained through its DISINFOX’s profile.
3. DISINFOX Public API checks the API key in the request headers. If
it is valid, it starts retrieving all the incidents from the backend and
sends them back to the DISINFOX connector as a response. The body
of this response will contain all the STIX2 objects representing all the
incidents uploaded to the platform.
4. DISINFOX connector inserts the STIX2 objects from the API response
to OpenCTI without any extra transformation.
5. The last operations are repeated just by changing the newer than
value, which now will be set to the last time that the connector was
set. The next call to the connector will be made depending on the time
set in the CONNECTOR RUN EVERY parameter set in the installation of
the connector to OpenCTI.
Now, all SDOs and SROs are stored in OpenCTI. A listing of all the ingested
disinformation incidents can be easily seen in the Threats > Intrusion Set
section.
The presented use case can be used as an example to see the analysis that
can be done in the OpenCTI platform. Apart from the Overview section that
shows a summary of the properties (name, description, first seen date, etc.),
the Knowledge tab of the Ukrainian incident offers much more interesting
data.
The first picture of Figure 8 shows the Diamond graph that summarizes the
relationships of the intrusion set in 4 dimensions: Adversary, where we find
Russia as the threat actor; Capabilities, where attack patterns (DISARM
techniques) such as Formal Diplomatic Channels or Deliver Ads can be di-
rectly found; Victimology, where Ukraine is set as the target of this intrusion
set; and Infraestructure, which is unused.
13


---

DISINFOX 
Public API
DISINFOX 
OpenCTI connector
OpenCTI
1st retrieval request (all incidents)
GET /incidents?
  newer_than=<epoch>
  HTTP/1.1
Authentication: <APIKEY>
Response with all available incidents
API key check
All incidents retrieval
2nd retrieval request (new incidents)
GET /incidents?
  newer_than=<last_run>
  HTTP/1.1
Authentication: <APIKEY>
API key check
Incidents modified/created
after newer_than
Response with all available incidents
OpenCTI invocation
last_run=now()
OpenCTI invocation
CONNECTOR_RUN_EVERY
OpenCTI ingestion
STIX Bundle
STIX2 obj
OpenCTI ingestion
STIX Bundle
STIX2 obj
STIX Bundle
STIX2 obj
STIX Bundle
STIX2 obj
Figure 7: DISINFOX’s proof-of-concept OpenCTI connector messages
14


---

If the VIEW ALL button in the Capabilities frame or the Attack patterns
button in the right bar is selected, OpenCTI displays the view in the second
picture of Figure 8. This is the matrix view, which shows the used attack
patterns in the matrix model that is selected, in this case, the DISARM
matrix, which has been installed thanks to the DISARM connector. Notice
how all the attack patterns used in the Ukrainian incident are highlighted
under their corresponding tactic in the DISARM matrix.
These are just examples of the possibilities of using OpenCTI to manage dis-
information incidents, but other actions such as Cyber Kill Chain analysis
or correlation with other incidents by taking into account its common DIS-
ARM techniques or target locations can be achieved. Overall, disinformation
analysts can embed this connector into their workflow to monitor, correlate
and asses disinformation incidents with a potentially shared view with other
cybersecurity incidents, providing a rich picture of the current picture of the
threat landscape.
3. Conclusions
This work introduces DISINFOX, an open-source threat intelligence exchange
platform for managing and distributing disinformation incident data. DISIN-
FOX facilitates the structured and interoperable reporting, visualization, and
analysis of disinformation incidents by leveraging DISARM TTPs and a cus-
tom STIX2-based data model. A use case illustrates how these functionalities
operate in practice.
Disinformation incidents can be easily uploaded through the web-based fron-
tend, which supports automated detection of TTPs in complementary PDF
reports. The platform provides an interactive listing of incidents, allowing
users to explore detailed information, including descriptions, affected coun-
tries visualized on a map, associated DISARM TTPs, and a STIX2 graph
representation of the incident. Additionally, incidents can be exported in
more readable formats such as PDF or Word, alongside the original STIX2
Bundle.
The interoperability of DISINFOX ensures seamless integration with other
CTI solutions through its Public API, enabling the ingestion of structured
disinformation incidents into mature cybersecurity platforms. This interop-
erability enhances correlation and investigation capabilities by allowing ana-
lysts to link disinformation campaigns with traditional cybersecurity threats,
reflecting real-world attack scenarios.
To validate this approach, a proof-of-concept DISINFOX connector for OpenCTI
was developed, successfully ingesting over 100 modeled disinformation in-
cidents from various sources. The technology stack adopted (DISARM +
15


---

Figure 8: OpenCTI Knowledge tab in the page of the modeled intrusion set
16


---

STIX2.1 + OpenCTI ) aligns with the strategy jointly agreed upon by the
EU and the US for addressing Foreign Information Manipulation and Inter-
ference (FIMI), as outlined in the EU-US Trade and Technology Council’s
fourth ministerial meeting [17].
Acknowledgements
This study was partially funded by (a) the strategic project “Development
of Professionals and Researchers in Cybersecurity, Cyberdefense and Data
Science (CDL-TALENTUM)” from i) the Spanish National Institute of Cy-
bersecurity (INCIBE) and ii) by the Recovery, Transformation and Resilience
Plan, Next Generation EU, and (b) by a “Juan de la Cierva” Postdoctoral
Fellowship (JDC2023-051658-I) funded by the i) Spanish Ministry of Sci-
ence, Innovation and Universities (MCIU), ii) by the Spanish State Research
Agency (AEI/10.13039/501100011033) and iii) by the European Social Fund
Plus (FSE+).
References
[1] J. Posetti, A. Matthews, A short guide to the history of ‘fake news’
and disinformation, International Center for Journalists 7 (2018) (2018)
2018–07.
[2] S.
Vosoughi,
D.
Roy,
S.
Aral,
The
spread
of
true
and
false
news
online,
Science
359
(6380)
(2018)
1146–1151.
arXiv:
https://www.science.org/doi/pdf/10.1126/science.aap9559,
doi:10.1126/science.aap9559.
[3] B. van Niekerk, The evolution of information warfare in ukraine: 2014
to 2022, Journal of Information Warfare 22 (2023) 10–31.
[4] European External Action Service’s (EEAS) Stratcom, 1st EEAS Re-
port on Foreign Information Manipulation and Interference Threats,
2023.
[5] European External Action Service’s (EEAS) Stratcom, 2nd EEAS Re-
port on Foreign Information Manipulation and Interference Threats,
2024.
[6] J. Pastor-Galindo, P. Nespoli, J. A. Ruip´erez-Valiente, Large-language-
model-powered agent-based framework for misinformation and disinfor-
mation research: Opportunities and open challenges, IEEE Security &
Privacy 22 (3) (2024) 24–36. doi:10.1109/MSEC.2024.3380511.
17


---

[7] K. M. Caramancion, Y. Li, E. Dubois, E. S. Jung, The missing case of
disinformation from the cybersecurity risk continuum: A comparative
assessment of disinformation with other cyber threats, Data 7 (4 2022).
doi:10.3390/data7040049.
[8] K. Baraniuk, P. Marsza lek, The potential of cyber threat intelligence
analytical frameworks in research on information operations and influ-
ence operations, Internal Security Review 2024 (31 (16)) (2024) 279–320.
doi:10.4467/20801335PBW.24.027.20804.
[9] N. Sun, M. Ding, J. Jiang, W. Xu, X. Mo, Y. Tai, J. Zhang, Cyber
threat intelligence mining for proactive cybersecurity defense: A survey
and new perspectives, IEEE Communications Surveys & Tutorials 25 (3)
(2023) 1748–1774. doi:10.1109/COMST.2023.3273282.
[10] G. C. L. de Molina, F. S. Gonz´alez, P. Nespoli, J. Pastor-Galindo, J. A.
Ruip´erez-Valiente, Analyzing frameworks to model disinformation at-
tacks in online social networks, in: 9th National Conference on Cyber-
security Research (JNIC 2024), 2024, pp. 92–99.
[11] A. B. L´opez, J. Pastor-Galindo, J. A. Ruip´erez-Valiente, Frameworks,
modeling and simulations of misinformation and disinformation: A sys-
tematic literature review (2024). arXiv:2406.09343.
[12] A. D. C. Tudela, J. Pastor-Galindo, P. Nespoli, J. A. Ruip´erez-Valiente,
The influence operation ontology (ioo) (2025). arXiv:2503.07304.
URL https://arxiv.org/abs/2503.07304
[13] S. Terp, P. Breuer, Disarm: a framework for analysis of disinformation
campaigns, in: 2022 IEEE Conference on Cognitive and Computational
Aspects of Situation Management (CogSIMA), 2022, pp. 1–8.
doi:
10.1109/CogSIMA54611.2022.9830669.
[14] J. Pastor-Galindo, P. Nespoli, J. A. Ruip´erez-Valiente, D. Camacho,
Influence operations in social networks (2025). arXiv:2502.11827.
URL https://arxiv.org/abs/2502.11827
[15] J. Pastor-Galindo, H. ˆAn Sandlin, F. G. M´armol, G. Bovet, G. M. P´erez,
A big data architecture for early identification and categorization of
dark web sites, Future Generation Computer Systems 157 (2024) 67–81.
doi:10.1016/j.future.2024.03.025.
18


---

[16] M. Fulde-Hardy, Working paper presenting a dataset, a methodology,
and a codebook to guide future applications of structured frameworks
enabling threat assessment (2024).
[17] European External Action Service (EEAS), Ttc ministerial foreign
information manipulation and interference in third countries (2023).
URL
https://www.eeas.europa.eu/eeas/
trade-and-technology-council-fourth-ministerial--annex-foreign-information-m
en
[18] S. Hassine, How OpenCTI helps to fight disinformation and foreign
interferences — Filigran Blog — filigran.io, https://filigran.io/
how-opencti-helps-to-fight-disinformation-and-foreign-interferences/,
[Accessed 30-01-2025].
[19] F. S. Gonz´alez, J. Pastor-Galindo, J. A. Ruip´erez-Valiente, Toward in-
teroperable representation and sharing of disinformation incidents in
cyber threat intelligence (2025). arXiv:2502.20997.
URL https://arxiv.org/abs/2502.20997
[20] DFRLab, Russian War Report: Kremlin claims Bucha massacre was
staged by Ukraine — dfrlab.org, https://dfrlab.org/2022/04/04/
russian-war-report-kremlin-claims-bucha-massacre-was-staged-by-ukraine/,
[Accessed 11-03-2025].
19
