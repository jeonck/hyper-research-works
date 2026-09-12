---
title: Updates - Updates - April 2026 | MITRE ATT&CK®
id: updates-updates-april-2026-mitre-attck
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
- primary-artefact
created: '2026-09-12T17:44:02.190150Z'
updated: '2026-09-12T21:34:09.372278Z'
source: https://attack.mitre.org/resources/updates/updates-april-2026/
source_domain: attack.mitre.org
fetched_at: '2026-09-12T17:44:02.189288Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'MITRE ATT&CK v19 release notes (April 2026, official page): names the Defense
  Evasion split into Stealth and Defense Impairment as the biggest change, lists Enterprise
  revocations of the Impair Defenses sub-techniques into new Disable or Modify Tools
  / System Firewall sub-techniques, and defines the change classes used in release
  notes.'
---

Updates - Updates - April 2026 | MITRE ATT&CK®
ATT&CKcon 7.0 in-person tickets are open! Join us October 27-28, 2026 in McLean, VA.
Register here
for in-person tickets; hotel and location details can be found in the
FAQ
.
Home
Resources
Version History
April 2026 Release Notes
Updates - April 2026
Version
Start Date
End Date
Data
Changelogs
ATT&CK v19
April 28, 2026
Current version of ATT&CK
v19.0 on MITRE/CTI
v19.1 on MITRE/CTI
18.1 - 19.0
Details
(
JSON
)
19.0 - 19.1
Details
(
JSON
)
Note: For the subsequent ATT&CK v19.2 release notes, see
Updates - August 2026
.
The April 2026 (v19) ATT&CK release updates Techniques, Groups, Campaigns and Software for Enterprise, Mobile, and ICS.
The biggest changes in ATT&CK v19 are the split of the Defense Evasion Tactic in Enterprise ATT&CK into the
Stealth
and
Defense Impairment
Tactics, the addition of Sub-Techniques to ICS ATT&CK, and the beginnings of
Detection Strategies
in Mobile ATT&CK. A post describing the rationale behind the Defense Evasion split was published to
ATT&CK's Blog
in March, and an
accompanying blog post
describes final details of the split, contains guidance for transitioning to the new Tactics, and details changes across the entire ATT&CK release.
This release also includes a
human-readable detailed changelog
showing more specifically what changed in updated ATT&CK objects, and a
machine-readable JSON changelog
, whose format is described in
ATT&CK's Github
.
This version of ATT&CK contains 949 Pieces of Software, 178 Groups, and 59 Campaigns.
Broken out by domain:
Enterprise: 15 Tactics, 222 Techniques, 475 Sub-Techniques, 174 Groups, 821 Pieces of Software, 56 Campaigns, 44 Mitigations, 697 Detection Strategies, 1758 Analytics, and 106 Data Components
Mobile: 12 Tactics, 77 Techniques, 47 Sub-Techniques, 20 Groups, 126 Pieces of Software, 3 Campaigns, 13 Mitigations, 124 Detection Strategies, 211 Analytics, and 29 Data Components
ICS: 12 Tactics, 79 Techniques, 18 Sub-Techniques, 14 Groups, 23 Pieces of Software, 8 Campaigns, 52 Mitigations, 18 Assets, 97 Detection Strategies, 96 Analytics, and 36 Data Components
Release Notes Terminology
New objects: ATT&CK objects which are only present in the new release.
Major version changes: ATT&CK objects that have a major version change. (e.g. 1.0 → 2.0)
Minor version changes: ATT&CK objects that have a minor version change. (e.g. 1.0 → 1.1)
Other version changes: ATT&CK objects that have a version change of any other kind. (e.g. 1.0 → 1.2)
Patches: ATT&CK objects that have been patched while keeping the version the same. (e.g., 1.0 → 1.0 but something like a typo, a URL, or some metadata was fixed)
Object revocations: ATT&CK objects which are revoked by a different object.
Object deprecations: ATT&CK objects which are deprecated and no longer in use, and not replaced.
Object deletions: ATT&CK objects which are no longer found in the STIX data.
Table of Contents
Release Notes Terminology
Table of Contents
Techniques
Enterprise
New Techniques
Major Version Changes
Minor Version Changes
Patches
Revocations
Mobile
Minor Version Changes
ICS
New Techniques
Minor Version Changes
Patches
Revocations
Software
Enterprise
New Software
Major Version Changes
Minor Version Changes
Patches
Mobile
New Software
ICS
Minor Version Changes
Groups
Enterprise
New Groups
Major Version Changes
Minor Version Changes
Patches
Mobile
New Groups
Major Version Changes
Minor Version Changes
ICS
Minor Version Changes
Patches
Campaigns
Enterprise
New Campaigns
Minor Version Changes
Patches
ICS
New Campaigns
Minor Version Changes
Assets
ICS
Minor Version Changes
Mitigations
Enterprise
Patches
ICS
Minor Version Changes
Data Components
Enterprise
Major Version Changes
Minor Version Changes
Patches
Mobile
New Data Components
Minor Version Changes
ICS
Major Version Changes
Minor Version Changes
Patches
Detection Strategies
Enterprise
New Detection Strategies
Minor Version Changes
Patches
Deprecations
ICS
New Detection Strategies
Analytics
Enterprise
New Analytics
Minor Version Changes
Patches
Mobile
Major Version Changes
Minor Version Changes
ICS
New Analytics
Minor Version Changes
Patches
Contributors to this release
Techniques
Enterprise
New Techniques
Disable or Modify System Firewall
(v1.0)
Disable or Modify System Firewall:
Cloud Firewall
(v1.0)
Disable or Modify System Firewall:
Network Device Firewall
(v1.0)
Disable or Modify System Firewall:
Windows Host Firewall
(v1.0)
Disable or Modify Tools
(v1.0)
Disable or Modify Tools:
Clear Linux or Mac System Logs
(v1.0)
Disable or Modify Tools:
Clear Windows Event Logs
(v1.0)
Disable or Modify Tools:
Disable or Modify Cloud Log
(v1.0)
Disable or Modify Tools:
Disable or Modify Linux Audit System Log
(v1.0)
Disable or Modify Tools:
Disable or Modify Windows Event Log
(v1.0)
Disable or Modify Tools:
Modify or Spoof Tool UI
(v1.0)
Downgrade Attack
(v1.0)
Exploitation for Defense Impairment
(v1.0)
Generate Content
(v1.0)
Generate Content:
Audio-Visual Content
(v1.0)
Generate Content:
Written Content
(v1.0)
Obfuscated Files or Information:
Invisible Unicode
(v1.0)
Prevent Command History Logging
(v1.0)
Query Public AI Services
(v1.0)
Safe Mode Boot
(v1.0)
Social Engineering
(v1.0)
Social Engineering:
Email Spoofing
(v1.0)
Social Engineering:
Impersonation
(v1.0)
Major Version Changes
Abuse Elevation Control Mechanism
(v1.5→v2.0)
Abuse Elevation Control Mechanism:
Bypass User Account Control
(v2.2→v3.0)
Abuse Elevation Control Mechanism:
Elevated Execution with Prompt
(v1.1→v2.0)
Abuse Elevation Control Mechanism:
Setuid and Setgid
(v1.2→v2.0)
Abuse Elevation Control Mechanism:
Sudo and Sudo Caching
(v1.1→v2.0)
Abuse Elevation Control Mechanism:
TCC Manipulation
(v1.1→v2.0)
Abuse Elevation Control Mechanism:
Temporary Elevated Cloud Access
(v1.2→v2.0)
Access Token Manipulation
(v2.1→v3.0)
Access Token Manipulation:
Create Process with Token
(v1.3→v2.0)
Access Token Manipulation:
Make and Impersonate Token
(v1.2→v2.0)
Access Token Manipulation:
Parent PID Spoofing
(v1.1→v2.0)
Access Token Manipulation:
SID-History Injection
(v1.1→v2.0)
Access Token Manipulation:
Token Impersonation/Theft
(v1.3→v2.0)
Adversary-in-the-Middle:
Name Resolution Poisoning and SMB Relay
(v1.4→v2.0)
BITS Jobs
(v1.5→v2.0)
Build Image on Host
(v1.3→v2.0)
Debugger Evasion
(v1.1→v2.0)
Delay Execution
(v1.0→v2.0)
Deobfuscate/Decode Files or Information
(v1.4→v2.0)
Deploy Container
(v1.4→v2.0)
Direct Volume Access
(v2.3→v3.0)
Domain or Tenant Policy Modification
(v3.2→v4.0)
Domain or Tenant Policy Modification:
Group Policy Modification
(v1.1→v2.0)
Domain or Tenant Policy Modification:
Trust Modification
(v2.2→v3.0)
Execution Guardrails
(v1.3→v2.0)
Execution Guardrails:
Environmental Keying
(v1.1→v2.0)
Execution Guardrails:
Mutual Exclusion
(v1.0→v2.0)
Exploitation for Stealth
(v1.5→v2.0)
File and Directory Permissions Modification
(v2.3→v3.0)
File and Directory Permissions Modification:
Linux and Mac Permissions
(v1.2→v2.0)
File and Directory Permissions Modification:
Windows Permissions
(v1.2→v2.0)
Hide Artifacts
(v1.4→v2.0)
Hide Artifacts:
Bind Mounts
(v1.0→v2.0)
Hide Artifacts:
Email Hiding Rules
(v1.4→v2.0)
Hide Artifacts:
Extended Attributes
(v1.0→v2.0)
Hide Artifacts:
File/Path Exclusions
(v1.0→v2.0)
Hide Artifacts:
Hidden File System
(v1.1→v2.0)
Hide Artifacts:
Hidden Files and Directories
(v1.2→v2.0)
Hide Artifacts:
Hidden Users
(v1.2→v2.0)
Hide Artifacts:
Hidden Window
(v1.4→v2.0)
Hide Artifacts:
Ignore Process Interrupts
(v1.0→v2.0)
Hide Artifacts:
NTFS File Attributes
(v1.2→v2.0)
Hide Artifacts:
Process Argument Spoofing
(v1.1→v2.0)
Hide Artifacts:
Resource Forking
(v1.1→v2.0)
Hide Artifacts:
Run Virtual Instance
(v1.3→v2.0)
Hide Artifacts:
VBA Stomping
(v1.2→v2.0)
Hijack Execution Flow
(v1.3→v2.0)
Hijack Execution Flow:
AppDomainManager
(v1.0→v2.0)
Hijack Execution Flow:
COR_PROFILER
(v1.1→v2.0)
Hijack Execution Flow:
DLL
(v2.1→v3.0)
Hijack Execution Flow:
Dylib Hijacking
(v2.1→v3.0)
Hijack Execution Flow:
Dynamic Linker Hijacking
(v2.1→v3.0)
Hijack Execution Flow:
Executable Installer File Permissions Weakness
(v1.1→v2.0)
Hijack Execution Flow:
KernelCallbackTable
(v1.0→v2.0)
Hijack Execution Flow:
Path Interception by PATH Environment Variable
(v1.2→v2.0)
Hijack Execution Flow:
Path Interception by Search Order Hijacking
(v1.1→v2.0)
Hijack Execution Flow:
Path Interception by Unquoted Path
(v1.1→v2.0)
Hijack Execution Flow:
Services File Permissions Weakness
(v1.1→v2.0)
Hijack Execution Flow:
Services Registry Permissions Weakness
(v1.3→v2.0)
Indicator Removal
(v2.4→v3.0)
Indicator Removal:
Clear Command History
(v1.6→v2.0)
Indicator Removal:
Clear Mailbox Data
(v1.2→v2.0)
Indicator Removal:
Clear Network Connection History and Configurations
(v1.2→v2.0)
Indicator Removal:
Clear Persistence
(v1.2→v2.0)
Indicator Removal:
File Deletion
(v1.2→v2.0)
Indicator Removal:
Network Share Connection Removal
(v1.2→v2.0)
Indicator Removal:
Relocate Malware
(v1.2→v2.0)
Indicator Removal:
Timestomp
(v1.2→v2.0)
Indirect Command Execution
(v1.3→v2.0)
Masquerading
(v1.8→v2.0)
Masquerading:
Break Process Trees
(v1.0→v2.0)
Masquerading:
Browser Fingerprint
(v1.0→v2.0)
Masquerading:
Double File Extension
(v1.0→v2.0)
Masquerading:
Invalid Code Signature
(v1.0→v2.0)
Masquerading:
Masquerade Account Name
(v1.0→v2.0)
Masquerading:
Masquerade File Type
(v1.1→v2.0)
Masquerading:
Masquerade Task or Service
(v1.2→v2.0)
Masquerading:
Match Legitimate Resource Name or Location
(v2.0→v3.0)
Masquerading:
Overwrite Process Arguments
(v1.0→v2.0)
Masquerading:
Rename Legitimate Utilities
(v2.0→v3.0)
Masquerading:
Right-to-Left Override
(v1.1→v2.0)
Masquerading:
Space after Filename
(v1.1→v2.0)
Modify Authentication Process
(v2.6→v3.0)
Modify Authentication Process:
Conditional Access Policies
(v1.1→v2.0)
Modify Authentication Process:
Domain Controller Authentication
(v2.1→v3.0)
Modify Authentication Process:
Hybrid Identity
(v1.1→v2.0)
Modify Authentication Process:
Multi-Factor Authentication
(v1.4→v2.0)
Modify Authentication Process:
Network Device Authentication
(v2.1→v3.0)
Modify Authentication Process:
Network Provider DLL
(v1.0→v2.0)
Modify Authentication Process:
Password Filter DLL
(v2.1→v3.0)
Modify Authentication Process:
Pluggable Authentication Modules
(v2.1→v3.0)
Modify Authentication Process:
Reversible Encryption
(v1.1→v2.0)
Modify Cloud Compute Infrastructure
(v1.2→v2.0)
Modify Cloud Compute Infrastructure:
Create Cloud Instance
(v1.2→v2.0)
Modify Cloud Compute Infrastructure:
Create Snapshot
(v1.2→v2.0)
Modify Cloud Compute Infrastructure:
Delete Cloud Instance
(v1.2→v2.0)
Modify Cloud Compute Infrastructure:
Modify Cloud Compute Configurations
(v2.0→v3.0)
Modify Cloud Compute Infrastructure:
Revert Cloud Instance
(v1.2→v2.0)
Modify Cloud Resource Hierarchy
(v1.0→v2.0)
Modify Registry
(v2.0→v3.0)
Modify System Image
(v1.1→v2.0)
Modify System Image:
Downgrade System Image
(v1.1→v2.0)
Modify System Image:
Patch System Image
(v1.1→v2.0)
Network Boundary Bridging
(v1.2→v2.0)
Network Boundary Bridging:
Network Address Translation Traversal
(v1.2→v2.0)
Obfuscated Files or Information
(v1.7→v2.0)
Obfuscated Files or Information:
Binary Padding
(v1.3→v2.0)
Obfuscated Files or Information:
Command Obfuscation
(v1.0→v2.0)
Obfuscated Files or Information:
Compile After Delivery
(v1.2→v2.0)
Obfuscated Files or Information:
Compression
(v1.0→v2.0)
Obfuscated Files or Information:
Dynamic API Resolution
(v1.0→v2.0)
Obfuscated Files or Information:
Embedded Payloads
(v1.2→v2.0)
Obfuscated Files or Information:
Encrypted/Encoded File
(v1.1→v2.0)
Obfuscated Files or Information:
Fileless Storage
(v2.1→v3.0)
Obfuscated Files or Information:
HTML Smuggling
(v1.3→v2.0)
Obfuscated Files or Information:
Indicator Removal from Tools
(v1.2→v2.0)
Obfuscated Files or Information:
Junk Code Insertion
(v1.0→v2.0)
Obfuscated Files or Information:
LNK Icon Smuggling
(v1.0→v2.0)
Obfuscated Files or Information:
Polymorphic Code
(v1.1→v2.0)
Obfuscated Files or Information:
SVG Smuggling
(v1.0→v2.0)
Obfuscated Files or Information:
Software Packing
(v1.3→v2.0)
Obfuscated Files or Information:
Steganography
(v1.2→v2.0)
Obfuscated Files or Information:
Stripped Payloads
(v1.2→v2.0)
Plist File Modification
(v1.0→v2.0)
Pre-OS Boot
(v1.3→v2.0)
Pre-OS Boot:
Bootkit
(v1.2→v2.0)
Pre-OS Boot:
Component Firmware
(v1.2→v2.0)
Pre-OS Boot:
ROMMONkit
(v1.1→v2.0)
Pre-OS Boot:
System Firmware
(v1.2→v2.0)
Pre-OS Boot:
TFTP Boot
(v1.1→v2.0)
Process Injection
(v1.4→v2.0)
Process Injection:
Asynchronous Procedure Call
(v1.2→v2.0)
Process Injection:
Dynamic-link Library Injection
(v1.4→v2.0)
Process Injection:
Extra Window Memory Injection
(v1.1→v2.0)
Process Injection:
ListPlanting
(v1.2→v2.0)
Process Injection:
Portable Executable Injection
(v1.2→v2.0)
Process Injection:
Proc Memory
(v1.1→v2.0)
Process Injection:
Process Doppelgänging
(v1.1→v2.0)
Process Injection:
Process Hollowing
(v1.4→v2.0)
Process Injection:
Ptrace System Calls
(v1.2→v2.0)
Process Injection:
Thread Execution Hijacking
(v1.2→v2.0)
Process Injection:
Thread Local Storage
(v1.2→v2.0)
Process Injection:
VDSO Hijacking
(v1.2→v2.0)
Reflective Code Loading
(v1.3→v2.0)
Rogue Domain Controller
(v2.2→v3.0)
Rootkit
(v1.3→v2.0)
Selective Exclusion
(v1.0→v2.0)
Subvert Trust Controls
(v1.3→v2.0)
Subvert Trust Controls:
Code Signing
(v1.2→v2.0)
Subvert Trust Controls:
Code Signing Policy Modification
(v1.1→v2.0)
Subvert Trust Controls:
Gatekeeper Bypass
(v1.3→v2.0)
Subvert Trust Controls:
Install Root Certificate
(v1.3→v2.0)
Subvert Trust Controls:
Mark-of-the-Web Bypass
(v1.2→v2.0)
Subvert Trust Controls:
SIP and Trust Provider Hijacking
(v1.1→v2.0)
System Binary Proxy Execution
(v3.2→v4.0)
System Binary Proxy Execution:
CMSTP
(v2.2→v3.0)
System Binary Proxy Execution:
Compiled HTML File
(v2.2→v3.0)
System Binary Proxy Execution:
Control Panel
(v2.1→v3.0)
System Binary Proxy Execution:
Electron Applications
(v1.0→v2.0)
System Binary Proxy Execution:
InstallUtil
(v2.1→v3.0)
System Binary Proxy Execution:
MMC
(v2.1→v3.0)
System Binary Proxy Execution:
Mavinject
(v2.0→v3.0)
System Binary Proxy Execution:
Mshta
(v2.1→v3.0)
System Binary Proxy Execution:
Msiexec
(v2.1→v3.0)
System Binary Proxy Execution:
Odbcconf
(v2.1→v3.0)
System Binary Proxy Execution:
Regsvcs/Regasm
(v2.1→v3.0)
System Binary Proxy Execution:
Regsvr32
(v2.2→v3.0)
System Binary Proxy Execution:
Rundll32
(v2.5→v3.0)
System Binary Proxy Execution:
Verclsid
(v2.1→v3.0)
System Script Proxy Execution
(v2.1→v3.0)
System Script Proxy Execution:
PubPrn
(v2.1→v3.0)
System Script Proxy Execution:
SyncAppvPublishingServer
(v1.0→v2.0)
Template Injection
(v1.4→v2.0)
Traffic Signaling
(v2.5→v3.0)
Traffic Signaling:
Port Knocking
(v1.2→v2.0)
Traffic Signaling:
Socket Filters
(v1.0→v2.0)
Trusted Developer Utilities Proxy Execution
(v1.3→v2.0)
Trusted Developer Utilities Proxy Execution:
ClickOnce
(v1.1→v2.0)
Trusted Developer Utilities Proxy Execution:
JamPlus
(v1.0→v2.0)
Trusted Developer Utilities Proxy Execution:
MSBuild
(v1.4→v2.0)
Unused/Unsupported Cloud Regions
(v1.1→v2.0)
Use Alternate Authentication Material
(v1.5→v2.0)
Use Alternate Authentication Material:
Application Access Token
(v1.8→v2.0)
Use Alternate Authentication Material:
Pass the Hash
(v1.3→v2.0)
Use Alternate Authentication Material:
Pass the Ticket
(v1.2→v2.0)
Use Alternate Authentication Material:
Web Session Cookie
(v1.5→v2.0)
Valid Accounts
(v2.8→v3.0)
Valid Accounts:
Cloud Accounts
(v1.9→v2.0)
Valid Accounts:
Default Accounts
(v1.5→v2.0)
Valid Accounts:
Domain Accounts
(v1.5→v2.0)
Valid Accounts:
Local Accounts
(v1.5→v2.0)
Virtualization/Sandbox Evasion
(v1.4→v2.0)
Virtualization/Sandbox Evasion:
System Checks
(v2.3→v3.0)
Virtualization/Sandbox Evasion:
Time Based Checks
(v2.0→v3.0)
Virtualization/Sandbox Evasion:
User Activity Based Checks
(v1.2→v2.0)
Weaken Encryption
(v1.1→v2.0)
Weaken Encryption:
Disable Crypto Hardware
(v1.1→v2.0)
Weaken Encryption:
Reduce Key Space
(v1.1→v2.0)
XSL Script Processing
(v1.3→v2.0)
Minor Version Changes
Command and Scripting Interpreter
(v2.6→v2.7)
Scheduled Task/Job
(v2.4→v2.5)
Patches
Adversary-in-the-Middle
(v2.5)
Cloud Service Discovery
(v1.4)
Compromise Host Software Binary
(v2.2)
Create or Modify System Process:
Windows Service
(v1.6)
Data Encoding:
Non-Standard Encoding
(v1.1)
Data Manipulation
(v1.1)
Data Manipulation:
Runtime Data Manipulation
(v1.2)
Data Manipulation:
Stored Data Manipulation
(v1.1)
Data Manipulation:
Transmitted Data Manipulation
(v1.1)
Develop Capabilities:
Exploits
(v1.0)
Event Triggered Execution:
Image File Execution Options Injection
(v1.2)
Exploit Public-Facing Application
(v2.8)
Financial Theft
(v1.2)
Internal Spearphishing
(v1.4)
Native API
(v2.3)
Network Sniffing
(v1.7)
Obtain Capabilities:
Artificial Intelligence
(v1.1)
Obtain Capabilities:
Exploits
(v1.0)
Phishing
(v2.7)
Phishing:
Spearphishing Voice
(v1.2)
Phishing for Information
(v1.4)
Phishing for Information:
Spearphishing Voice
(v1.0)
Software Extensions:
Browser Extensions
(v1.1)
Stage Capabilities:
Upload Malware
(v1.3)
User Execution:
Malicious Copy and Paste
(v1.1)
Revocations
Clear Linux or Mac System Logs (revoked by Disable or Modify Tools:
Clear Linux or Mac System Logs
)
(v1.0)
Clear Windows Event Logs (revoked by Disable or Modify Tools:
Clear Windows Event Logs
)
(v1.5)
Disable Windows Event Logging (revoked by Disable or Modify Tools:
Disable or Modify Windows Event Log
)
(v1.4)
Disable or Modify Cloud Firewall (revoked by Disable or Modify System Firewall:
Cloud Firewall
)
(v1.3)
Disable or Modify Cloud Logs (revoked by Disable or Modify Tools:
Disable or Modify Cloud Log
)
(v2.1)
Disable or Modify Linux Audit System (revoked by Disable or Modify Tools:
Disable or Modify Linux Audit System Log
)
(v1.0)
Disable or Modify Network Device Firewall (revoked by Disable or Modify System Firewall:
Network Device Firewall
)
(v1.0)
Disable or Modify System Firewall (revoked by
Disable or Modify System Firewall
)
(v1.3)
Disable or Modify Tools (revoked by
Disable or Modify Tools
)
(v1.7)
Downgrade Attack (revoked by
Downgrade Attack
)
(v1.3)
Email Spoofing (revoked by Social Engineering:
Email Spoofing
)
(v1.1)
Impair Command History Logging (revoked by
Prevent Command History Logging
)
(v2.3)
Impair Defenses (revoked by
Disable or Modify Tools
)
(v1.7)
Impersonation (revoked by Social Engineering:
Impersonation
)
(v1.1)
Indicator Blocking (revoked by
Disable or Modify Tools
)
(v1.5)
Safe Mode Boot (revoked by
Safe Mode Boot
)
(v1.1)
Spoof Security Alerting (revoked by Disable or Modify Tools:
Modify or Spoof Tool UI
)
(v1.0)
Mobile
Minor Version Changes
Phishing
(v1.1→v1.2)
ICS
New Techniques
Block Communications
(v1.0)
Block Communications:
Ethernet
(v1.0)
Block Communications:
Serial COM
(v1.0)
Block Communications:
Wi-Fi
(v1.0)
Block Operational Technology Message
(v1.0)
Block Operational Technology Message:
Command Message
(v1.0)
Block Operational Technology Message:
Reporting Message
(v1.0)
Insecure Credentials
(v1.0)
Insecure Credentials:
Default Credentials
(v1.0)
Insecure Credentials:
Hardcoded Credentials
(v1.0)
Modify Firmware
(v1.0)
Modify Firmware:
Module Firmware
(v1.0)
Modify Firmware:
System Firmware
(v1.0)
Program Download:
Download All
(v1.0)
Program Download:
Online Edit
(v1.0)
Program Download:
Program Append
(v1.0)
Project File Infection:
Siemens Project File Format
(v1.0)
Remote System Discovery:
Broadcast Discovery
(v1.0)
Remote System Discovery:
Multicast Discovery
(v1.0)
Remote System Discovery:
Port Scan
(v1.0)
Unauthorized Message
(v1.0)
Unauthorized Message:
Command Message
(v1.0)
Unauthorized Message:
Reporting Message
(v1.0)
Minor Version Changes
Project File Infection
(v1.0→v1.1)
Patches
Remote System Discovery
(v1.1)
Revocations
Block Command Message (revoked by Block Operational Technology Message:
Command Message
)
(v1.1)
Block Reporting Message (revoked by Block Operational Technology Message:
Reporting Message
)
(v1.0)
Block Serial COM (revoked by Block Communications:
Serial COM
)
(v1.1)
Default Credentials (revoked by Insecure Credentials:
Default Credentials
)
(v1.0)
Hardcoded Credentials (revoked by Insecure Credentials:
Hardcoded Credentials
)
(v1.0)
Module Firmware (revoked by Modify Firmware:
Module Firmware
)
(v1.1)
Spoof Reporting Message (revoked by Unauthorized Message:
Reporting Message
)
(v1.2)
System Firmware (revoked by Modify Firmware:
System Firmware
)
(v1.1)
Unauthorized Command Message (revoked by Unauthorized Message:
Command Message
)
(v1.2)
Software
Enterprise
New Software
ANELLDR
(v1.0)
AshTag
(v1.0)
BRICKSTORM
(v1.0)
BRUSHFIRE
(v1.0)
Caminho
(v1.0)
Crocodilus
(v1.0)
DCRAT
(v1.0)
DOWNIISSA
(v1.0)
DRYHOOK
(v1.0)
Diskpart
(v1.0)
DynoWiper
(v1.0)
Fooder
(v1.0)
GlassWorm
(v1.0)
HTTPTroy
(v1.0)
HeartCrypt
(v1.0)
HiddenFace
(v1.0)
IronWind
(v1.0)
LAMEHUG
(v1.0)
LODEINFO
(v1.0)
LP-Notes
(v1.0)
LazyWiper
(v1.0)
MirrorStealer
(v1.0)
MuddyViper
(v1.0)
NOOPLDR
(v1.0)
PHASEJAM
(v1.0)
PHPsert
(v1.0)
PureCrypter
(v1.0)
ROAMINGHOUSE
(v1.0)
RustyWater
(v1.0)
SPAWNCHIMERA
(v1.0)
SameCoin
(v1.0)
Shai-Hulud
(v1.0)
SystemBC
(v1.0)
TRAILBLAZE
(v1.0)
TruffleHog
(v1.0)
Tsundere Botnet
(v1.0)
evilginx2
(v1.0)
Major Version Changes
Qilin
(v1.0→v2.0)
UPPERCUT
(v1.1→v2.0)
Minor Version Changes
Arp
(v1.2→v1.3)
BITSAdmin
(v1.4→v1.5)
Cobalt Strike
(v1.13→v1.14)
FRP
(v1.0→v1.1)
Havoc
(v1.0→v1.1)
Industroyer
(v1.1→v1.2)
LockerGoga
(v2.0→v2.1)
Mimikatz
(v1.10→v1.11)
Net
(v2.7→v2.8)
Nltest
(v1.3→v1.4)
PUBLOAD
(v1.0→v1.1)
Ping
(v1.4→v1.5)
PlugX
(v3.2→v3.3)
QuasarRAT
(v2.1→v2.2)
Rclone
(v1.2→v1.3)
Remcos
(v1.3→v1.4)
Rubeus
(v1.1→v1.2)
ShrinkLocker
(v1.0→v1.1)
Stuxnet
(v1.4→v1.5)
TONESHELL
(v1.0→v1.1)
Tasklist
(v1.2→v1.3)
Tor
(v1.4→v1.5)
Wevtutil
(v1.2→v1.3)
certutil
(v1.5→v1.6)
ipconfig
(v1.1→v1.2)
njRAT
(v1.6→v1.7)
sqlmap
(v1.0→v1.1)
Patches
HyperStack
(v1.0)
MCMD
(v1.1)
OSInfo
(v1.1)
RemoteCMD
(v1.1)
SDBbot
(v2.1)
Mobile
New Software
Crocodilus
(v1.0)
DocSwap
(v1.0)
SameCoin
(v1.0)
VajraSpy
(v1.0)
ICS
Minor Version Changes
INCONTROLLER
(v1.0→v1.1)
Industroyer
(v1.1→v1.2)
LockerGoga
(v2.0→v2.1)
PLC-Blaster
(v1.0→v1.1)
Stuxnet
(v1.4→v1.5)
Triton
(v1.1→v1.2)
Groups
Enterprise
New Groups
MirrorFace
(v1.0)
VOID MANTICORE
(v1.0)
Major Version Changes
APT-C-36
(v1.1→v2.0)
MuddyWater
(v6.0→v7.0)
WIRTE
(v2.0→v3.0)
Minor Version Changes
APT28
(v5.2→v5.3)
Gamaredon Group
(v3.2→v3.3)
Kimsuky
(v5.1→v5.2)
Wizard Spider
(v4.0→v4.1)
Patches
APT29
(v6.2)
APT3
(v1.4)
APT38
(v3.1)
FIN13
(v1.0)
Mustang Panda
(v3.0)
TA505
(v3.0)
Threat Group-1314
(v1.1)
Turla
(v5.1)
Volt Typhoon
(v2.0)
Mobile
New Groups
Kimsuky
(v5.2)
MONSOON
(v1.0)
Patchwork
(v1.6)
Stolen Pencil
(v1.1)
WIRTE
(v3.0)
Major Version Changes
MuddyWater
(v6.0→v7.0)
Minor Version Changes
APT28
(v5.2→v5.3)
ICS
Minor Version Changes
Wizard Spider
(v4.0→v4.1)
Patches
APT38
(v3.1)
Campaigns
Enterprise
New Campaigns
2025 Poland Wiper Attacks
(v1.0)
Anthropic AI-orchestrated Campaign
(v1.0)
Operation AkaiRyū
(v1.0)
Operation Digital Eye
(v1.0)
Minor Version Changes
HomeLand Justice
(v1.0→v1.1)
Triton Safety Instrumented System Attack
(v1.0→v1.1)
Patches
SharePoint ToolShell Exploitation
(v1.0)
Water Curupira Pikabot Distribution
(v1.0)
ICS
New Campaigns
2025 Poland Wiper Attacks
(v1.0)
Minor Version Changes
Triton Safety Instrumented System Attack
(v1.0→v1.1)
Assets
ICS
Minor Version Changes
Application Server
(v2.0→v2.1)
Control Server
(v2.0→v2.1)
Data Historian
(v2.0→v2.1)
Distributed Control System (DCS) Controller
(v1.0→v1.1)
Field I/O
(v1.0→v1.1)
Human-Machine Interface (HMI)
(v1.0→v1.1)
Intelligent Electronic Device (IED)
(v1.0→v1.1)
Jump Host
(v1.0→v1.1)
Programmable Automation Controller (PAC)
(v1.0→v1.1)
Programmable Logic Controller (PLC)
(v1.0→v1.1)
Remote Terminal Unit (RTU)
(v1.0→v1.1)
Safety Controller
(v1.0→v1.1)
Virtual Private Network (VPN) Server
(v1.0→v1.1)
Workstation
(v2.0→v2.1)
Mitigations
Enterprise
Patches
Network Segmentation
(v1.2)
ICS
Minor Version Changes
Access Management
(v1.0→v1.1)
Audit
(v1.0→v1.1)
Authorization Enforcement
(v1.1→v1.2)
Boot Integrity
(v1.0→v1.1)
Code Signing
(v1.0→v1.1)
Communication Authenticity
(v1.0→v1.1)
Encrypt Network Traffic
(v1.0→v1.1)
Encrypt Sensitive Information
(v1.0→v1.1)
Filter Network Traffic
(v1.0→v1.1)
Human User Authentication
(v1.1→v1.2)
Network Allowlists
(v1.0→v1.1)
Network Intrusion Prevention
(v1.0→v1.1)
Network Segmentation
(v1.0→v1.1)
Out-of-Band Communications Channel
(v1.0→v1.1)
Restrict File and Directory Permissions
(v1.0→v1.1)
Software Process and Device Authentication
(v1.1→v1.2)
Static Network Configuration
(v1.1→v1.2)
Data Components
Enterprise
Major Version Changes
Application Log Content
(v2.0→v3.0)
Cloud Service Enumeration
(v2.0→v3.0)
File Access
(v2.0→v3.0)
File Creation
(v2.0→v3.0)
File Deletion
(v2.0→v3.0)
File Modification
(v2.0→v3.0)
Module Load
(v2.0→v3.0)
Process Access
(v2.0→v3.0)
Scheduled Job Creation
(v2.0→v3.0)
User Account Authentication
(v2.0→v3.0)
Minor Version Changes
Command Execution
(v2.0→v2.1)
Driver Metadata
(v2.0→v2.1)
File Metadata
(v2.0→v2.1)
Group Enumeration
(v2.0→v2.1)
Host Status
(v2.0→v2.1)
Instance Modification
(v2.0→v2.1)
Network Connection Creation
(v2.0→v2.1)
Network Traffic Content
(v2.0→v2.1)
Network Traffic Flow
(v2.0→v2.1)
OS API Execution
(v2.0→v2.1)
Process Creation
(v2.0→v2.1)
Process Metadata
(v2.0→v2.1)
Service Modification
(v2.0→v2.1)
User Account Metadata
(v2.0→v2.1)
Patches
Service Metadata
(v2.0)
Windows Registry Key Modification
(v2.0)
Mobile
New Data Components
Application Log Content
(v3.0)
Application State
(v1.0)
Cloud Service Enumeration
(v3.0)
File Access
(v3.0)
File Creation
(v3.0)
File Deletion
(v3.0)
File Metadata
(v2.1)
File Modification
(v3.0)
Module Load
(v3.0)
Process Access
(v3.0)
Scheduled Job Creation
(v3.0)
User Account Authentication
(v3.0)
Minor Version Changes
API Calls
(v2.0→v2.1)
Application Assets
(v2.0→v2.1)
Application Permission
(v2.0→v2.1)
Command Execution
(v2.0→v2.1)
Host Status
(v2.0→v2.1)
Network Communication
(v2.0→v2.1)
Network Connection Creation
(v2.0→v2.1)
Network Traffic Content
(v2.0→v2.1)
Network Traffic Flow
(v2.0→v2.1)
OS API Execution
(v2.0→v2.1)
Process Creation
(v2.0→v2.1)
Process Metadata
(v2.0→v2.1)
Protected Configuration
(v2.0→v2.1)
System Notifications
(v2.0→v2.1)
System Settings
(v2.0→v2.1)
ICS
Major Version Changes
Application Log Content
(v2.0→v3.0)
File Access
(v2.0→v3.0)
File Creation
(v2.0→v3.0)
File Deletion
(v2.0→v3.0)
File Modification
(v2.0→v3.0)
Module Load
(v2.0→v3.0)
Scheduled Job Creation
(v2.0→v3.0)
User Account Authentication
(v2.0→v3.0)
Minor Version Changes
Command Execution
(v2.0→v2.1)
File Metadata
(v2.0→v2.1)
Network Connection Creation
(v2.0→v2.1)
Network Traffic Content
(v2.0→v2.1)
Network Traffic Flow
(v2.0→v2.1)
OS API Execution
(v2.0→v2.1)
Process Creation
(v2.0→v2.1)
Process History/Live Data
(v2.0→v2.1)
Process Metadata
(v2.0→v2.1)
Process/Event Alarm
(v2.0→v2.1)
Service Modification
(v2.0→v2.1)
Patches
Service Metadata
(v2.0)
Windows Registry Key Modification
(v2.0)
Detection Strategies
Enterprise
New Detection Strategies
Detect Social Engineering
(v1.0)
Detect Windows Firewall
(v1.0)
Detection Strategy for Invisible Unicode
(v1.0)
Detection of Audio-Visual Content
(v1.0)
Detection of Defense Impairment
(v1.0)
Detection of Generate Content
(v1.0)
Detection of Query Public AI Services
(v1.0)
Detection of Written Content
(v1.0)
Minor Version Changes
Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms.
(v1.0→v1.1)
Patches
Detect Disabled Windows Event Log
(v1.0)
Detection Strategy for Defense Impairment via Prevent Command History Logging across OS platforms.
(v1.0)
Detection Strategy for Disable or Modify Cloud Log
(v1.0)
Detection Strategy for Disable or Modify Linux Audit System Log
(v1.0)
Detection Strategy for Exploitation for Stealth
(v1.0)
Detection for Spoofing Tool UI across OS Platforms
(v1.0)
Detection of Remote Service Session Hijacking for RDP.
(v1.0)
Detection of Unauthorized Network Firewall Rule Modification
(v1.0)
Deprecations
Detection Strategy for Impair Defenses Across Platforms
(v1.0)
Detection Strategy for Impair Defenses Indicator Blocking
(v1.0)
ICS
New Detection Strategies
Detection of Block Communications
(v1.0)
Detection of Block Ethernet
(v1.0)
Detection of Block Operational Technology Message
(v1.0)
Detection of Block Wi-Fi
(v1.0)
Detection of Broadcast Discovery
(v1.0)
Detection of Firmware Modification
(v1.0)
Detection of Insecure Credentials
(v1.0)
Detection of Multicast Discovery
(v1.0)
Detection of Online Edit
(v1.0)
Detection of Port Scan
(v1.0)
Detection of Program Append
(v1.0)
Detection of Program Download All
(v1.0)
Detection of Siemens Project File Format Infection
(v1.0)
Detection of Unauthorized Message
(v1.0)
Analytics
Enterprise
New Analytics
Analytic 2033
(v1.0)
Analytic 2034
(v1.0)
Analytic 2035
(v1.0)
Analytic 2036
(v1.0)
Analytic 2037
(v1.0)
Analytic 2038
(v1.0)
Analytic 2039
(v1.0)
Analytic 2040
(v1.0)
Analytic 2041
(v1.0)
Analytic 2042
(v1.0)
Analytic 2043
(v1.0)
Analytic 2044
(v1.0)
Analytic 2059
(v1.0)
Analytic 2060
(v1.0)
Analytic 2061
(v1.0)
Analytic 2062
(v1.0)
Analytic 2063
(v1.0)
Analytic 2064
(v1.0)
Analytic 2065
(v1.0)
Minor Version Changes
Analytic 1370
(v1.0→v1.1)
Analytic 1371
(v1.0→v1.1)
Analytic 1372
(v1.0→v1.1)
Analytic 1373
(v1.0→v1.1)
Analytic 1374
(v1.0→v1.1)
Analytic 1452
(v1.0→v1.1)
Analytic 1612
(v1.0→v1.1)
Analytic 1614
(v1.0→v1.1)
Patches
Analytic 0551
(v1.0)
Analytic 1615
(v1.0)
Analytic 1616
(v1.0)
Analytic 1617
(v1.0)
Analytic 1940
(v1.0)
Analytic 1959
(v1.0)
Analytic 2026
(v1.0)
Mobile
Major Version Changes
Analytic 1650
(v1.0→v2.0)
Analytic 1693
(v1.0→v2.0)
Analytic 1694
(v1.0→v2.0)
Analytic 1708
(v1.0→v2.0)
Analytic 1774
(v1.0→v2.0)
Analytic 1782
(v1.0→v2.0)
Analytic 1795
(v1.0→v2.0)
Minor Version Changes
Analytic 1644
(v1.0→v1.1)
Analytic 1645
(v1.0→v1.1)
Analytic 1646
(v1.0→v1.1)
Analytic 1647
(v1.0→v1.1)
Analytic 1648
(v1.0→v1.1)
Analytic 1649
(v1.0→v1.1)
Analytic 1652
(v1.0→v1.1)
Analytic 1653
(v1.0→v1.1)
Analytic 1654
(v1.0→v1.1)
Analytic 1657
(v1.0→v1.1)
Analytic 1658
(v1.0→v1.1)
Analytic 1663
(v1.0→v1.1)
Analytic 1664
(v1.0→v1.1)
Analytic 1665
(v1.0→v1.1)
Analytic 1666
(v1.0→v1.1)
Analytic 1669
(v1.0→v1.1)
Analytic 1670
(v1.0→v1.1)
Analytic 1675
(v1.0→v1.1)
Analytic 1676
(v1.0→v1.1)
Analytic 1677
(v1.0→v1.1)
Analytic 1678
(v1.0→v1.1)
Analytic 1681
(v1.0→v1.1)
Analytic 1682
(v1.0→v1.1)
Analytic 1683
(v1.0→v1.1)
Analytic 1684
(v1.0→v1.1)
Analytic 1697
(v1.0→v1.1)
Analytic 1698
(v1.0→v1.1)
Analytic 1701
(v1.0→v1.1)
Analytic 1702
(v1.0→v1.1)
Analytic 1706
(v1.0→v1.1)
Analytic 1710
(v1.0→v1.1)
Analytic 1711
(v1.0→v1.1)
Analytic 1712
(v1.0→v1.1)
Analytic 1713
(v1.0→v1.1)
Analytic 1714
(v1.0→v1.1)
Analytic 1715
(v1.0→v1.1)
Analytic 1716
(v1.0→v1.1)
Analytic 1717
(v1.0→v1.1)
Analytic 1718
(v1.0→v1.1)
Analytic 1719
(v1.0→v1.1)
Analytic 1720
(v1.0→v1.1)
Analytic 1721
(v1.0→v1.1)
Analytic 1722
(v1.0→v1.1)
Analytic 1723
(v1.0→v1.1)
Analytic 1724
(v1.0→v1.1)
Analytic 1725
(v1.0→v1.1)
Analytic 1726
(v1.0→v1.1)
Analytic 1727
(v1.0→v1.1)
Analytic 1728
(v1.0→v1.1)
Analytic 1729
(v1.0→v1.1)
Analytic 1730
(v1.0→v1.1)
Analytic 1731
(v1.0→v1.1)
Analytic 1732
(v1.0→v1.1)
Analytic 1733
(v1.0→v1.1)
Analytic 1734
(v1.0→v1.1)
Analytic 1737
(v1.0→v1.1)
Analytic 1738
(v1.0→v1.1)
Analytic 1739
(v1.0→v1.1)
Analytic 1740
(v1.0→v1.1)
Analytic 1741
(v1.0→v1.1)
Analytic 1742
(v1.0→v1.1)
Analytic 1743
(v1.0→v1.1)
Analytic 1747
(v1.0→v1.1)
Analytic 1748
(v1.0→v1.1)
Analytic 1751
(v1.0→v1.1)
Analytic 1752
(v1.0→v1.1)
Analytic 1753
(v1.0→v1.1)
Analytic 1754
(v1.0→v1.1)
Analytic 1755
(v1.0→v1.1)
Analytic 1756
(v1.0→v1.1)
Analytic 1758
(v1.0→v1.1)
Analytic 1759
(v1.0→v1.1)
Analytic 1762
(v1.0→v1.1)
Analytic 1763
(v1.0→v1.1)
Analytic 1764
(v1.0→v1.1)
Analytic 1767
(v1.0→v1.1)
Analytic 1768
(v1.0→v1.1)
Analytic 1770
(v1.0→v1.1)
Analytic 1771
(v1.0→v1.1)
Analytic 1772
(v1.0→v1.1)
Analytic 1773
(v1.0→v1.1)
Analytic 1776
(v1.0→v1.1)
Analytic 1777
(v1.0→v1.1)
Analytic 1778
(v1.0→v1.1)
Analytic 1779
(v1.0→v1.1)
Analytic 1780
(v1.0→v1.1)
Analytic 1781
(v1.0→v1.1)
Analytic 1784
(v1.0→v1.1)
Analytic 1785
(v1.0→v1.1)
Analytic 1788
(v1.0→v1.1)
Analytic 1789
(v1.0→v1.1)
Analytic 1793
(v1.0→v1.1)
Analytic 1794
(v1.0→v1.1)
Analytic 1797
(v1.0→v1.1)
Analytic 1800
(v1.0→v1.1)
Analytic 1801
(v1.0→v1.1)
Analytic 1802
(v1.0→v1.1)
Analytic 1803
(v1.0→v1.1)
Analytic 1804
(v1.0→v1.1)
Analytic 1805
(v1.0→v1.1)
Analytic 1806
(v1.0→v1.1)
Analytic 1807
(v1.0→v1.1)
Analytic 1808
(v1.0→v1.1)
Analytic 1809
(v1.0→v1.1)
Analytic 1812
(v1.0→v1.1)
Analytic 1815
(v1.0→v1.1)
Analytic 1816
(v1.0→v1.1)
Analytic 1817
(v1.0→v1.1)
Analytic 1820
(v1.0→v1.1)
Analytic 1821
(v1.0→v1.1)
Analytic 1822
(v1.0→v1.1)
Analytic 1823
(v1.0→v1.1)
Analytic 1824
(v1.0→v1.1)
Analytic 1825
(v1.0→v1.1)
Analytic 1826
(v1.0→v1.1)
Analytic 1827
(v1.0→v1.1)
Analytic 1828
(v1.0→v1.1)
Analytic 1829
(v1.0→v1.1)
Analytic 1830
(v1.0→v1.1)
Analytic 1837
(v1.0→v1.1)
Analytic 1840
(v1.0→v1.1)
Analytic 1841
(v1.0→v1.1)
Analytic 1842
(v1.0→v1.1)
Analytic 1847
(v1.0→v1.1)
Analytic 1848
(v1.0→v1.1)
Analytic 1849
(v1.0→v1.1)
Analytic 1850
(v1.0→v1.1)
Analytic 1851
(v1.0→v1.1)
Analytic 1852
(v1.0→v1.1)
Analytic 1853
(v1.0→v1.1)
Analytic 1854
(v1.0→v1.1)
ICS
New Analytics
Analytic 2045
(v1.0)
Analytic 2046
(v1.0)
Analytic 2047
(v1.0)
Analytic 2048
(v1.0)
Analytic 2049
(v1.0)
Analytic 2050
(v1.0)
Analytic 2051
(v1.0)
Analytic 2052
(v1.0)
Analytic 2053
(v1.0)
Analytic 2054
(v1.0)
Analytic 2055
(v1.0)
Analytic 2056
(v1.0)
Analytic 2057
(v1.0)
Analytic 2058
(v1.0)
Minor Version Changes
Analytic 1864
(v1.0→v1.1)
Analytic 1922
(v1.0→v1.1)
Patches
Analytic 1879
(v1.0)
Contributors to this release
Alberto Garcia
Alex Soler, AttackIQ
Alex Wong
Arad Inbar, Fidelis Security
Arun Seelagan, CISA
Austin Clark, @c2defense
Blake Strom, Microsoft Threat Intelligence
Caio Silva
Cian Heasley
Contributor: Dominik Breitenbacher, ESET
Daniel Feichter, @VirtualAllocEx, Infosec Tirol
Dominik Breitenbacher, ESET
Dongwook Kim, KISA
Dragos Threat Intelligence
Emile Kenning, Sophos
Expel
Gal Singer, @galsinger29, Team Nautilus Aqua Security
Gilberto Pérez
Gordon Long, LegioX/Zoom, asaurusrex
Ibrahim Ali Khan
Jaesang Oh, KC7 Foundation
Janantha Marasinghe
Joe Gumke, U.S. Bank
Jorell Magtibay, National Australia Bank Limited
Kiyohito Yamamoto, RedLark, NTT Communications
Kyaw Pyiyt Htet (@KyawPyiytHtet)
Lab52 by S2 Grupo
Liran Ravich, CardinalOps
Lucas Heiligenstein
Manikantan Srinivasan, NEC Corporation India
Marco Pedrinazzi, @pedrinazziM, InTheCyber
Matt Snyder, VMware
Mayuresh Dani, Qualys
Menachem Goldstein
Nathaniel Quist, Palo Alto Networks
Nay Myo Hlaing (Ethan), DBS Bank
Patrick Mkhael (aka Pinguino)
Pawel Partyka, Microsoft Threat Intelligence
Pedro Rodriguez
Pooja Natarajan, NEC Corporation India
Prasad Somasamudram, McAfee
Prasanth Sadanala, Cigna Information Protection (CIP) - Threat Response Engineering Team
Rich Rafferty (NR Labs)
Rob Smith
Sarathkumar Rajendran, Microsoft Defender365
Sekhar Sarukkai, McAfee
Serhii Melnyk
SeungYoul Yoo, AhnLab
Stijn Geerts
Syed Ummar Farooqh, McAfee
Taewoo Lee, KISA
Takemasa Kamatani , NEC Corporation
Tim (Wadhwa-)Brown
Tommaso Tosi, @tosto92, InTheCyber
Uriel Kosayev
Vikas Singh, Sophos
Víctor Alba
Wai Linn Oo, Kernellix Co.,Ltd.
Wietze Beukema @Wietze
Yusuke Kubo, RedLark, NTT Communications
Ziv Karliner, @ziv_kr, Team Nautilus Aqua Security
×
Core Objects:
All
Core ATT&CK Objects
All
None
Matrices
Tactics
Techniques
Sub-Techniques
Defenses:
All
Defenses
All
None
Mitigations
Assets
Detection Strategies
Analytics
Data Components
CTI:
All
CTI
All
None
Groups
Software
Campaigns
Reference:
All
Reference
All
None
Resources
Domains:
All
Domains
All
None
Enterprise
Mobile
ICS
Reset filters