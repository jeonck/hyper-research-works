---
title: IEEE Copyright Notice
id: ieee-copyright-notice
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:34:14.299141Z'
updated: '2026-09-12T21:44:26.696475Z'
source: https://arxiv.org/abs/2401.07995v2
source_domain: arxiv.org
fetched_at: '2026-09-12T21:34:14.296850Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2401.07995v2: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/ieee-copyright-notice.pdf
doi: arXiv:2401.07995v2
---

IEEE Copyright Notice
© 2024 IEEE. Personal use of this material is
permitted. Permission from IEEE must be obtained
for all other uses, in any current or future me-
dia, including reprinting/republishing this material
for advertising or promotional purposes, creating
new collective works, for resale or redistribution
to servers or lists, or reuse of any copyrighted
component of this work in other works.
Submitted to: IEEE SoutheastCon 2024 · March
15-17, 2024 - Westin Peachtree Plaza, Atlanta,
Georgia https://ieeesoutheastcon.org/
Preprint Version, February 21, 2024
arXiv:2401.07995v2  [cs.CR]  21 Feb 2024


---

The Pulse of Fileless Cryptojacking Attacks:
Malicious PowerShell Scripts
Said Varlioglu, Nelly Elsayed, Eva Ruhsar Varlioglu*, Murat Ozer, Zag ElSayed
School of Information Technology
*School of Criminal Justice
University of Cincinnati
Cincinnati, Ohio, USA
varlioms@mail.uc.edu, elsayeny@ucmail.uc.edu, varliorr@mail.uc.edu, ozermm@ucmail.uc.edu, elsayezs@ucmail.uc.edu
Abstract—Fileless malware predominantly relies on PowerShell
scripts, leveraging the native capabilities of Windows systems
to execute stealthy attacks that leave no traces on the victim’s
system. The effectiveness of the fileless method lies in its ability to
remain operational on victim endpoints through memory execu-
tion, even if the attacks are detected, and the original malicious
scripts are removed. Threat actors have increasingly utilized this
technique, particularly since 2017, to conduct cryptojacking at-
tacks. With the emergence of new Remote Code Execution (RCE)
vulnerabilities in ubiquitous libraries, widespread cryptocurrency
mining attacks have become prevalent, often employing fileless
techniques. This paper provides a comprehensive analysis of Pow-
erShell scripts of fileless cryptojacking, dissecting the common
malicious patterns based on the MITRE ATT&CK framework.
Index Terms—Powershell, malicious, scripts, fileless malware,
cryptojacking, cryptomining
I. INTRODUCTION
PowerShell, developed by Microsoft for Windows, is a
robust command-line shell and scripting language based on
the .NET framework. It derives its strength from a rich set
of cmdlets, object-oriented data handling, and seamless inte-
gration with Microsoft technologies. Widely used for system
administration, automation, and scripting in Windows environ-
ments, PowerShell provides comprehensive access to critical
Windows system functions, such as Windows Management
Instrumentation (WMI) and Component Object Model (COM)
objects. These capabilities enable remote content retrieval, in-
memory command execution, and access to local registry keys
and scheduled tasks [1].
PowerShell’s versatility and ubiquitousness minimize the
need for adversaries to customize payloads or download
overtly malicious tools on a target system. Adversaries can
abuse PowerShell to reflectively (filelessly) load and execute
commands/executables through the invocation feature without
creating new system processes [2], [3].
Fileless malware primarily relies on PowerShell due to its
robust functionality. This trend has emerged as an urgent
and challenging problem [1] since 2017 [4], especially with
the prevalence of common attacks such as ransomware and
cryptojacking utilizing this technique [5].
In particular, threat actors have found this technique ef-
fective because even when the attacks are detected and the
original malicious scripts are identified and removed, the
processes may remain operational on victim endpoints [4].
Additionally, threat actors use various open-source frame-
works, including PowerShell Empire and PowerSploit, that
have been created to support the use of PowerShell scripting
in post-exploitation cyber-offensive activities [1], [6], [7].
Threat actors have combined PowerShell-based fileless at-
tacks with cryptojacking [4]. Furthermore, with the emergence
of new Remote Code Execution (RCE) vulnerabilities such
as Log4Shell (CVE-2021-44228) affecting numerous software
products across various industries, widespread fileless crypto-
jacking and ransomware attacks have become prevalent [8].
In our work, this paper has two primary contributions.
Firstly, we analyzed malicious PowerShell scripts containing
fileless cryptojacking scripts as a descriptive study and aimed
at gaining an understanding of the problem and the overall
characteristics of fileless activities. Secondly, we collected
scripts providing a new dataset for this unique research area,
presenting a potential avenue for further research.
II. POWERSHELL-BASED FILELESS MALWARE
PowerShell-based fileless malware is considered an ad-
vanced volatile attack, as it operates entirely in system memory
(RAM) without leaving an executable file on the disk for in-
spection [9]. However, in some instances, fileless malware can
exhibit indirect file activity while establishing persistence by
configuring a WMI (Windows Management Instrumentation)
filter, allowing them to install a PowerShell command within
the WMI repository. Although this approach theoretically
involves a malicious WMI object residing on the disk, it
does not interact with the conventional file system, making
it challenging to detect and mitigate [10].
In fileless attacks such as Cobalt Strike, the scripts have
been observed employing obfuscation techniques such as
Base64-encoded commands with GunZip compression and
encrypted XOR keys. That conceals the specific Windows API
calls made by the shellcode and process injection into the
legitimate processes. Additionally, it masks the establishment
of Command and Control (C2) connections. Those techniques
help threat actors hide Windows API calls and secure session
data with encryption [11].


---

III. POWERSHELL-BASED FILELESS CRYPTOJACKING
MALWARE
In-memory-only cryptojacking can run on memory exploit-
ing PowerShell for execution [12]. It is more dangerous
than in-browser and in-host cryptojacking attacks because its
evasion and persistent techniques are more sophisticated [12].
Since fileless threats can give attackers command and control
abilities with backdoors [13], a fileless cryptojacking can be
converted to a data exfiltration activity or a ransomware attack.
Similar to the fileless ransomware attacks [13], cryptojack-
ers use open-source attack frameworks (Phase 1) to deliver
malicious scripts using phishing emails or vulnerability ex-
ploitations (Phase 2) and exploit PowerShell to execute the
payload on memory (Phase 3) and to create scheduled tasks
for persistent mechanism (Phase 4) with continues download
processes of malicious scripts [14]. Also, those malicious
scripts are frequently stored and downloaded from text storage
web services such as Pastebin. [15]. Attackers want a mali-
cious connection to remain to spread throughout the network
by escalating privileges (Phase 5) and exploiting common
vulnerabilities such as the use of EternalBlue SMB vulner-
ability [16] or RDP brute-forcing (Phase 6). This provides the
cryptojackers large pools of CPU resources (Phase 7) in victim
enterprises for efficient cryptocurrency mining slaves (Phase
8) [14] to gain illicit profit with cryptocurrencies (Phase 9).
A fileless cryptojacking attack can be started with phishing
emails, zero-day vulnerability exploitations, and hidden scripts
of malicious websites [17].
After infections, the endpoints send reports of the connec-
tion status and mining activity to the attackers’ Command
and control servers (C2). Attackers can also run remote
commands for other purposes, such as data exfiltration or
ransomware. This is another dangerous face of fileless crypto-
jacking compared with traditional cryptojacking techniques.
Lateral movement routines are observed for spreading in
victim networks [18]. As a fileless threat pattern, fileless
cryptojacking also uses scheduled tasks or registry keys such
as "Run" or "RunOnce" for malware propagation. Also, cryp-
tojackers can store PowerShell commands under scheduled
tasks and registry keys. System information is important to
run cryptojacking scripts. Thus the commands can collect
computer names, GUIDs, MAC addresses, OS, and timestamp
information. In the final stage, victim endpoints become slaves
of mining deployers or mining pools for the illicit gains of
cryptojackers.
The most prevalent fileless cryptojacking malware currently
found in the wild includes Lemon Duck, Purple Fox, Ghost-
Miner, PCASTLE, Tor2Mine [4]. Those malware strains are
primarily observed in Monero cryptocurrency (XMR) mining
activities.
Lemon Duck, targeting Windows systems, uses PowerShell
scripts and exploits vulnerabilities with an effective lateral
moving capability [19]. It can use Mimikatz to dump cre-
dentials, adfind.exe to scan active directories, and many other
techniques such as task scheduling, registry exploitation, WMI
subscriptions for persistent mechanism [20]. It can quickly
infiltrate networks, starting with a single infection and swiftly
spreading across the entire infrastructure to turn the resources
into cryptocurrency mining slaves [20]. Also, its malicious
scripts might be seen using the term “$Lemon_Duck” as a
variable [14].
Purple Fox exploits Windows vulnerabilities with rootk-
its
and
evasion
tactics
using
the
open-source
Invoke-
ReflectivePEInjection tool [21] to reflectively (filelessly) load
and execute GZIP-compressed executables into PowerShell
processes running on the memory [22].
GhostMiner injects malicious JavaScript into web pages
to mine cryptocurrency on unsuspecting visitors’ computers.
It has the high-level evasion techniques [23]. GhostMiner
exploits WMI objects as a fileless threat routine for a persistent
mechanism [24].
PCASTLE utilizes PowerShell and legitimate tools for hid-
den mining on Windows. WannaMine, leveraging EternalBlue,
mimics WannaCry and employs fileless methods for stealthy
mining [25].
Tor2Mine employs PowerShell to disable security, install
Monero miners, and collect Windows credentials, spreading
through networks by gaining admin access and deploying
services or using fileless commands when needed. Its goal
is to compromise entire networks, and although it has evolved
with various versions, the central strategy remains consistent:
exploiting software vulnerabilities to sustain a persistent min-
ing operation on infected networks [26].
In general, threat actors exploit PowerShell for fileless
cryptojacking [22], [26] to:
• Execute malicious code
• Obfuscate malicious activity
• Utilize living-off-the-land techniques
• Inject code into memory without touching the disk
• Spawn additional processes
• Steal system credentials
• Remotely download and execute arbitrary code
• Establish persistence mechanisms
• Disable security features
• Free up system resources for mining
• Disable any competing cryptojacking
• Re-infect other systems on the compromised network
IV. THE DATASET
Our research is based on a dataset sourced from cyber-
security blogs and the research body. This dataset, publicly
available on GitHub, comprises 200 fileless-based malicious
PowerShell scripts used for cryptojacking. It offers a compre-
hensive collection of malicious scripts associated with well-
known cryptojacking malware, including Purple Fox, Lemon
Duck, Tor2Mine, and others. These scripts serve as a valuable
resource for understanding cryptojacking activities, aligning
with the various attack phases defined in the MITRE ATT&CK
framework [27], spanning Initial Access (TA0001) to Com-
mand and Control (TA0011).


---

TABLE I
COMMON COMMAND PARAMETERS OF POWERSHELL-BASED FILELESS CRYPTOJACKING
Command
Parameter
Potential Exploitation
-nop
NoProfile
Bypass loading the user’s PowerShell profile.
-exec or -EP
ExecutionPolicy
Modify execution policy for the session.
-bypass
Bypass
Enable script execution without restrictions.
-w
Window
Open PowerShell in a new window.
-hidden
WindowStyle
Start PowerShell window hidden.
-c
Command
Specify a command to run in the session.
-IEX
Invoke-Expression
Execute a string as a command.
-enc
EncodedCommand
Use a base64-encoded command.
-nologo
NoLogo
Suppress PowerShell logo at startup.
-noni
NonInteractive
Run PowerShell non-interactively.
-f
Force
Override restrictions and warnings.
-if
InputFormat
Set script input data format.
-noexit
NoExit
Keep the session open after script execution.
V. DATA ANALYSIS WITH MITRE ATT&CK FRAMEWORK
Examining the cryptojacking scripts in the context of the
MITRE ATT&CK framework [27] sheds light on their opera-
tional methodologies during the execution phase. This analysis
deepens the understanding of cryptojacking activities and
has significant implications for cybersecurity efforts and the
broader research community.
In the next sections, we will explore how these scripts
operate throughout the different phases below, where appli-
cable, within the MITRE ATT&CK framework [27]. This
comprehensive analysis aims to provide a holistic view of the
behavior and tactics of fileless cryptojacking.
• TA0001 Initial Access
• TA0002 Execution
• TA0003 Persistence
• TA0005 Defense Evasion
• TA0006 Credential Access
• TA0007 Discovery
• TA0008 Lateral Movement
• TA0011 Command and Control
A. TA0001 Initial Access
A fileless cryptojacking attack can be started with phish-
ing emails, exploiting public-facing applications, and hidden
scripts of malicious websites [17]. Especially with the emer-
gence of new Remote Code Execution (RCE) vulnerabilities
such as Log4Shell (CVE-2021-44228) [28], and effective
penetration testing tools such as Cobalt Strike, fileless crypto-
jacking has become effective.
In a sample Log4Shell exploitation [29], HTTP requests
with JNDI injection payloads targeted the server with the
Base64-encoded payload involving downloading and executing
a script from a specified URL. This technique exploits vulnera-
bilities within a Tomcat server to establish unauthorized access
and execute arbitrary commands on the compromised system.
The attack deployed XMRig Monero miners with a PowerShell
downloader script retrieving content from a Pastebin page. The
other PowerShell command is associated with downloading a
batch file, and subsequently executing it. It reflectively loads
a Windows binary containing an encrypted, Base64-encoded
loader. The batch file contains a code fragment for miner setup,
specifying a wallet address. [8].
The forensics research reports show that threat actors can
compromise a domain controller in an organization network
environment, execute cryptojacking scripts, and deploy coin-
miners on the domain endpoints within two hours [30].
B. TA0002 Execution
Upon compromising an endpoint within an environment,
cryptojacking scripts leverage PowerShell to execute their
malicious agenda. The scripts were seen to adapt to system
variables, disable security measures, and maintain persistence
while evading detection.
PowerShell scripts might offer distinct advantages to threat
actors seeking to deploy a coinminer efficiently. In some
sample scripts [31], it was observed that the actors exploit
PowerShell by instantiating a "System.Net.WebClient" object,
a class designed for web interactions. The scripts then employ
the class’s "DownloadFile" method to retrieve coinminer batch
files from external sources, specifically GitHub repositories or
Pastebin pages. This shows the maintaining agility in payload
updates and modifications without altering the core script. The
scripts leverage the flexibility and parameterization capabilities
of PowerShell, using the "GetTempFileName" method from the
"System.IO.Path" class to generate a temporary file for storing
the downloaded batch file. Including a specific argument
during the execution of the batch file allows for dynamic
configuration, showcasing the threat actor’s intent to customize
the coinminer’s behavior without modifying the script itself.
Using PowerShell’s living-off-the-land capabilities, such as
obfuscation and temporary file usage, enhances the script’s
ability to minimize its footprint and avoid detection by security
tools. Utilizing the "Remove-Item" cmdlet, with the "-Force"
parameter, indicates the minimizing traces of the activities
by removing the temporary file post-execution. Obfuscation
and encoding of scripts are used to evade traditional antivirus
solutions and enhance the overall stealthiness of the attack.
Also, cryptojacking scripts were seen using ";" as a com-
mand separator, allowing for the sequential execution of these
operations.


---

With the breaking down of PowerShell commands in a
sample attack [8], the command "powershell.exe -exec bypass
-enc aQBl..." employs the execution policy bypass ("-exec
bypass") to override any restrictions and specifies that the
subsequent command is Base64-encoded ("-enc"). The second
command utilizes the "IEX" alias for "Invoke-Expression"
to execute the expression. It creates a new instance of the
"System.Net.WebClient" class and retrieves content from a
Pastebin page using the "DownloadString" method.
The use of Pastebin website is frequently observed in fileless
cryptojacking attacks. Pastebin is an online service for storing
and sharing plain text, commonly used for source code or
configuration data in the software development community.
Users can upload text, and others can view and edit it as
needed [32].
Threat actors can exploit Pastebin not only to download
malicious payloads but also as a straightforward command and
control (C2) communication channel. When creating a pastie,
they can later edit it. The scripts may be executed through
a persistence mechanism, which retrieves the content of a
specified Pastebin paste and dynamically adjusts its behavior
based on the retrieved content. Pastebin-related scripts are
observed with "curl" commands and might include parameters
such as "-WindowStyle hidden," "-ExecutionPolicy ByPass,"
and "DownloadString." These parameters indicate attempts to
hide script execution, bypass execution policies, and download
content from the internet [31].
In another example, the inclusion of -NoP and -NonI
parameters reflects operating without the burden of load-
ing PowerShell profiles or engaging in interactive sessions.
This allows for a swift and inconspicuous execution of the
script. The -W Hidden parameter, setting the window style
to "Hidden," strategically conceals the PowerShell window
during execution, adding a layer of obfuscation to the attack.
Including -Exec Bypass is pivotal in bypassing PowerShell’s
default execution policies, giving the threat actor the flexibil-
ity to execute the script regardless of the system’s security
configuration. Using environment variables, such as env:temp,
ensures the file is saved to the system’s temporary directory,
a common tactic to avoid raising suspicion. The subsequent
Start-Process cmdlet then initiates the execution of the down-
loaded executable.
To carry out their tasks, these scripts use various classes
and methods, each serving a specific purpose. This in-
cludes classes such as "text.encoding" for character encoding,
"IO.StreamReader" for stream reading, and "net.webrequest"
for handling web requests. Key methods involved in these
operations comprise "getbytes()" for converting data to UTF-
8 encoding, "readtoend()" to extract the entire content of
a stream, and "FromBase64String()" for decoding Base64-
encoded data. Additionally, the scripts also work with classes
like "RSAParameters" and "RSACryptoServiceProvider" for
encryption tasks.
Lemon Duck scripts also leverage "certutil" within Pow-
erShell to download and execute malicious scripts, including
compiled Python executables. These scripts can be executed
using Windows schedule tasks, leading to the execution of
malicious PowerShell commands and the download of a Cobalt
Strike beacon. These payloads initiate a Cobalt "beacon"
within the newly spawned PowerShell process memory, aiming
to establish communication with a command and control
server [33].
Also, cryptojacking scripts were seen by downloading the
XMRig ZIP file from a remote server and installing it. XMRIG
is an open-source software for mining cryptocurrencies like
Monero or Bitcoin [34]. PowerShell command employs the
"System.IO.Compression.ZipFile" class to extract the contents
of "xmrig.zip" to "mimu6". Mimu is a variant of the XMrig
Monero miner botnet [8]. The script downloads additional
tools, such as 7za.exe and nssm.zip, if necessary. 7z is a
popular file archiver (compression) tool. NSSM is also a tool
that ensures if the application running as a service fails, it
will be restarted. NSSM is seen as a persistence helper of the
XMrig mining bot [35].
The fileless part of the execution phase is seen with Pow-
erShell commands, which modify the "config.json" file within
the XMRig directory, replacing placeholders with specified
values for URL, user, password, CPU usage, and log file.
Conditional statements determine the startup directory and
execute different setups based on the value of the "ADMIN"
variable [34].
One of the other patterns was Base64-encoded commands
in the cryptojacking scripts. The encoded commands were
observed with specific configurations, including the suppres-
sion of profile loading ("-NoP"), non-interactive mode ("-
NonI"), hidden window ("-W Hidden"), and bypassing execu-
tion policies ("-Exec Bypass"). The decoded versions of those
commands show that downloader commands aim to fetch and
execute additional PowerShell codes.
C. TA0003 Persistence
In fileless cryptojacking attacks, threat actors have been
observed establishing persistence by exploiting specific Win-
dows components, including Task Scheduler and Windows
Management Instrumentation (WMI) event subscriptions. Task
Scheduler is a feature in Windows that enables the automation
of various tasks at specified intervals or in response to specific
events. Concurrently, Windows Management Instrumentation
(WMI) is leveraged to install event filters, providers, con-
sumers, and bindings that execute code when predefined events
occur.
In a sample command, threat actors utilized the "schtasks"
command to create a new scheduled task with various param-
eters. The "/create" flag indicates the intent to create a task,
and the "/sc MINUTE" parameter schedules the task to run at
specified minute intervals. The "/F" flag enforces the creation
of the task, overwriting it if it already exists.
Additionally, the "/ru" system parameter is specified to run
the task under the "system" account, a high-privileged built-in
account in Windows systems. These scripts interact with the
Task Scheduler service to verify the user’s administrator privi-
leges. Tasks are set up under the "system" account; otherwise,


---

they are created for the current user. The initial step involves
checking the current Windows identity using the "GetCurrent"
method from the "System.Security.Principal.WindowsIdentity"
class. If the identity does not contain the string "SYSTEM," the
script deletes all existing scheduled tasks using "SchTasks.exe
/Delete /TN * /F".
The "/RL HIGHEST" parameter sets the task to run with
the highest privileges. The command "mshta <URL>.hta"
launches the mshta utility to open a web page. The "-w
hidden -c <VARIABLE>" parameter defines the action ex-
ecuted when the task runs, launching a hidden PowerShell
command with the -w hidden flag and executing a PowerShell
script. Additionally, it pauses execution for a specific period
using the "start-sleep" command. The configuration includes
PowerShell commands that download and execute code from
specified Pastebin URLs [34].
The scripts involve the registration of event filters, con-
sumers, and bindings, typically associated with Windows
Management Instrumentation (WMI) event handling. In a
sample script, a conditional block attempts to create a WMI
event filter and consumer. The "Set-WmiInstance" cmdlet
configures the event filter and consumer with specified names.
The event query, constructed with the "SELECT" statement,
targets "Win32_PerfFormattedData_PerfOS_System" within a
300-second timeframe. The -enc flag executes a base64-
encoded PowerShell command, hidden and non-interactive, to
execute a script downloaded from Pastebin. An empty catch
block is present in case of an error during WMI instance
creation.
To retrieve a WMI event filter from the "root/subscription"
namespace, the scripts use the "Get-WMIObject" command,
specifying "-Class __EventFilter" and "-NameSpace root/sub-
scription".
The scripts utilize the PowerShell "getRan()" function to
generate random strings for task names, ensuring uniqueness
and unpredictability. COM objects representing the Windows
Task Scheduler service are created, connecting to it using the
"Connect()" method. An attempt is made to retrieve a task
from the root folder of the Task Scheduler service by calling
"GetFolder" and "GetTask" methods.
These cryptojacking scripts, under scheduled tasks, target
servers on the default RDP port ("3389/TCP"), attempting
access using common administrator usernames. On success,
the script adjusts Windows Firewall settings to open a specific
TCP port, acting as a marker. The continuous exploitation code
operates with a specific minute pause, generating new, random
IP addresses to compromise SMB and MS-SQL services. It
collects machine profiling data for transmission to a command-
and-control server, and modifying Windows Firewall settings
serves as a persistence mechanism.
The scripts attempt to delete specific scheduled tasks, pos-
sibly to cover tracks or remove traces. In preparation for
installing a cryptocurrency miner, they stop services, terminate
processes, and remove executable files. Commands like "net
stop" and "taskkill /f" halt services and terminate processes,
while "cmd /c del" deletes certain executable files.
In Purple Fox attacks, the scripts enter loops, checking for
the existence of the registry key. These loops act as a form
of persistence, ensuring continuous execution until specified
registry keys are set [36].
D. TA0005 Defense Evasion
Threat actors exhibit sophisticated evasion tactics for fileless
cryptjoacking. Each subsection below provides insights into
the intricate techniques utilized by threat actors to evade
detection and carry out malicious activities discreetly.
• Manipulating Antivirus Products
• Uninstalling Antivirus Products
• Firewall Disabling
• Dynamic Delay and Content Fetching
• Steganographic Tactics
• Reflective PE Injection
• Dynamic Payload Evasion
• Disrupting Competing Mining Services
1) Manipulating Antivirus Products: Fileless cryptojack-
ing scripts were observed using a method that involved insert-
ing exclusion rules into Windows Defender. The command,
encapsulated within a try-catch block, was intended to ex-
empt the entire C drive from virus scans utilizing the "Add-
MpPreference" cmdlet. This deliberate exclusion enabled ma-
licious actors to download and install tools on the C drive
without setting off virus scans. Furthermore, the commands
featured base64-encoded payloads crafted to retrieve and ex-
ecute the subsequent phase of the attack, thereby bolstering
their capacity to conduct malicious activities discreetly. [28].
Also, the scripts were seen to register custom com-
mands to initiate trusted Windows processes, like CompMgmt-
Launcher.exe or ComputerDefaults.exe, and subsequently re-
move the associated registry keys to disable Windows De-
fender real-time monitoring and add exclusions for specific
paths and processes [37].
2) Uninstalling Antivirus Products: Furthermore, cryp-
tojacking scripts leverage PowerShell to uninstall various
antivirus products, including ESET, Kaspersky, and Avast.
This uninstallation is achieved using the Windows Manage-
ment Instrumentation Command-line (WMIC) with the ""call
uninstall" command to invoke the uninstall operation on anti-
malware tools.
Specifically, the Windows Management Instrumentation
Command-line ("wmic.exe") employs the "/nointeractive" pa-
rameter to ensure unattended removal, eliminating the need for
user interaction during the uninstallation process. Additionally,
the command involves executing the uninstaller with the
"/verysilent" parameter, ensuring an extremely silent uninstal-
lation, as well as "/suppressmsgboxes" to prevent the display
of message boxes during the uninstallation. The "/norestart"
parameter avoids a system restart after removing the antivirus
product.
Lemon Duck also attempts to uninstall security products
from the machine through WMI, employing "taskkill" for
forced process termination and Windows service controller
commands to disable and remove these security products [33].


---

In Tor2Mine cryptojacking attacks, the scripts were ob-
served using the "sc (Service Control)" command to stop
and delete services associated with antivirus products. This
disrupts the normal operation of these security services. Also,
registry modifications are made to disable Windows Defender.
This involves setting "DWORD" values in specific registry
keys to "1," disabling of antivirus features with the Windows
Defender parameters below [26].
• DisableAntiSpyware
• DisableBehaviorMonitoring
• DisableOnAccessProtection
• DisableScanOnRealtimeEnable
3) Firewall Disabling: In addition to the fileless cryp-
tojacking scripts and the strategic exclusion from Windows
Defender scans, the threat actors took further measures to
enhance their attack capabilities. Specifically, they disable
Windows firewall by setting all profiles to state=off "netsh
advfirewall set allprofiles state off" [34]. This command uses
the "netsh" utility to modify the configuration of the Windows
Advanced Firewall. In particular, it sets the state of all firewall
profiles (Domain, Private, and Public) to "off," effectively
turning off the firewall protection for all network profiles.
Disabling the Windows Firewall removes a significant layer
of defense that the operating system provides against unautho-
rized network access and inbound/outbound communication.
By turning off the firewall, the threat actors aim to create
a more permissive environment for their malicious activities,
allowing unrestricted communication and data transfer without
impeding the firewall’s security measures.
4) Dynamic Delay and Content Fetching: The other tech-
nique is to use the "Start-Sleep -Seconds <Integer>" command
for a deliberate delay of specified seconds to evade immediate
detection and to ensure a specific state on the compromised
system. Following the delay, the script utilizes the "(New-
Object System.Net.WebClient).DownloadString" method. The
method is directed to fetch the contents of a remote URL. This
dynamic retrieval of content from a remote server indicates a
strategy threat actors employ to avoid static signatures and
continuously adapt their tactics.
5) Steganographic Tactics & Disguising Malicious Pay-
loads in JPG & PNG Files: In fileless cryptojacking at-
tacks, threat actors use the "steganography" technique to
conceal malicious activities within seemingly innocuous JPG
or PNG image files, as seen in Fig. 1 [36]. The image file is
downloaded and then extracted from memory. The embedded
encoded code is decoded, and the payload is run.
The embedded code below is an obfuscated PowerShell
script to download and execute malicious content from a
remote server. Specifically, it creates a "Bitmap" object from
an image fetched from a specified URL, then processes the
pixel data to form a payload, and finally executes the payload
using the IEX (Invoke-Expression) command.
Fig. 1. Sample image file for a fileless cryptojacking steganography [36].
$uyxQcl8XomEdJUJd=’sal a New-Object;Add-Type
-A System.Drawing;$g=a System.Drawing.Bitmap
((a Net.WebClient).OpenRead("
http[:]//rawcdn.githack[.]cyou/up.php?key=3")
;$o=a Byte[] 589824;(0..575)|%{foreach($x
in(0..1023)) {$p=$g.GetPixel($x,$_)
;$o[$_*1024+$x]=([math]::Floor
(($p.B-band15)*16)-bor($p.G -band 15))}};
IEX([System.Text.Encoding]::ASCII.GetString
($o[0..589362]) IEX ($uyxQcl8XomEdJUJd)
Steganography allows threat actors to hide executable code,
scripts, or other malicious payloads within the pixels or meta-
data of an image file without visibly altering its appearance
[36]. In PurpleFox scripts, it was seen that JPG files were
malicious MSI installation packages. PowerShell scripts can
be camouflaged as a .jpg image file. Upon execution, the
script performs malicious actions, including the download and
execution of Purple Fox’s main component or attempts at
privilege escalation [38]. In the sample attack, the PowerShell
script showcases a set of actions executed if the current user
possesses administrative privileges. The script dynamically
defines a ".NET" type named "msi" using the "Add-Type"
cmdlet, encapsulating native Windows Installer API functions
within this custom type. Subsequently, the "MsiInstallProduct"
function specifies the URL with a jpg extension as the package
path [39].
The cryptojacking scripts might have URLs also specify-
ing PNG file formats [40], traditionally an image format.
However, in a sample script, it was seen that the commands
invoke the Windows Installer (Msiexec) to install the content
retrieved from the URL. In a sample command, "Msiexec
/i http://<DomainAddress>/<FileName.Png /Q", the "/i" flag
indicates an installation process, while the URL specifies the
location of the payload disguised as a PNG image. The "/Q"
flag ensures a quiet installation without user interaction [40].
In the steganography technique, the scripts use "Sys-
tem.Drawing" classes and manipulating pixel data. In a Pow-


---

erShell script, the encoded strings are decoded and executed
using the "IEX Invoke-Expression" cmdlet. "System.Drawing"
assembly is then loaded using "Add-Type". Subsequently,
the script downloads an image from a specified URL us-
ing "Net.WebClient" and creates a "System.Drawing.Bitmap"
object from the downloaded image via the ("New-Object
Net.WebClient).OpenRead"method. The script then iterates
through each pixel of the image, manipulates the RGB com-
ponents, and stores the resulting values in an array. The script
concludes by executing a command obtained by decoding a
portion of the data within the array using another instance of
IEX [38].
Byte arrays are used to store pixel information. The
script processes each row of pixels in the image, extract-
ing information from the specific components. The extracted
data is then encoded into the byte array. The encoded
payload is converted from "ASCII" encoding using "[Sys-
tem.Text.Encoding]::ASCII.GetString(<Byte
Array>)".
This
payload is then executed using "Invoke-Expression" command.
The intentional delays were observed with "Start-Sleep <In-
teger>" that allows the script to evade immediate detection
[40].
6) Reflective
PE
Injection:
Threat
actors
frequently
utilize the open-source PowerSploit framework’s "Invoke-
ReflectivePEInjection" module for process injection in fileless
attacks. This module mimics reflective DLL injection, a tech-
nique commonly employed by adversaries [22].
Purple Fox attacks leverage reflective PE injection to evade
detection mechanisms. The injected code operates entirely in
memory without leaving traces on the disk. The "Invoke-
ReflectivePEInjection" function encapsulates this technique,
enabling the injection of a Portable Executable (PE) bi-
nary directly into the memory space of another process.
By fetching the reflective DLL and executable from re-
mote URLs, adversaries enhance the fileless nature of their
attack, making it challenging for traditional antivirus so-
lutions to detect and mitigate. The overarching goal of
such a technique is often to establish persistence, exe-
cute arbitrary commands, or deploy additional malicious
payloads without relying on conventional file-based execu-
tion methods. In the sample PowerShell scripts, the invo-
cation of the Invoke-ReflectivePEInjection function comes
with a URL "http://<domain>/<filename>.jpg" that signifies
the source of the reflective DLL, while the second URL
"http://<domain>/filename.jpg" serves as the target executable
into which the reflective DLL is intended to be injected.
The script executes a silent installation of an MSI package,
employing the command "msiexec /i <VARIABLE> /q". The
script embeds native Windows Installer API functions with
the MSI package. This script showcases a multi-faceted attack
strategy where a reflective DLL, obtained from a disguised
image file, is injected into a seemingly innocuous executable.
The incorporation of a silent MSI package installation further
underscores the threat actor’s intention to carry out malicious
activities without drawing attention. The use of reflective PE
injection not only enhances the fileless nature of the attack
but also aims for persistence and stealth, evading conventional
security measures [39].
In
these
scripts,
employing
the
"Invoke-
ReflectivePEInjection" cmdlet with the "-ExeArgs" parameter
provides
additional
arguments
to
the
executed
process,
including PowerShell flags such as "-nop", "-windowstyle
hidden", "-exec bypass", and "-EncodedCommand". These
flags collectively enhance stealth and bypass PowerShell
execution policies, showcasing the threat actors’ focus on
evasion and maintaining a low profile during exploitation.
This technique was mostly seen leveraging steganography for
advanced evasion techniques in fileless cryptojacking attacks.
7) Dynamic Payload Evasion: Threat actors use advanced
obfuscation and runtime loading in PowerShell. Threat ac-
tors leverage such intricate obfuscation and dynamic loading
techniques to bypass static security measures. In a sample
script, the usage of dynamic assembly loading allows ad-
versaries to fetch and execute payloads on-the-fly, making
it challenging for traditional antivirus solutions to detect
and block the malicious activities at the initial stage. The
repetition of this process indicates an attempt to ensure
persistence and to achieve a specific evasion goal. Within
each iteration, the script downloads data from a specified
URL using "Net.WebClient" and loads it as an assembly
with "[System.Reflection.Assembly]::Load". The specific sleep
period between iterations adds a delay, enhancing the script’s
stealthiness and complicating detection efforts.
Fetch and execute payloads on-the-fly" refers to a technique
where a piece of code, typically malicious, retrieves additional
components or instructions dynamically from an external
source during runtime. In the context of cybersecurity, this
often involves downloading malicious content or instructions
from a remote server or source, allowing threat actors to adapt
and evolve their attacks in real-time. This dynamic behavior
enhances the attackers’ ability to evade static security defenses,
as the specific payload or instructions are not present in the
initial code but are fetched during execution.
In the sample PowerShell script, the script downloads data
from a remote server, loads it as an assembly, and executes
the retrieved payload. This dynamic loading and execution
occur on-the-fly, meaning that the actual content and actions
are determined and executed during the script’s runtime rather
than being predefined in the static code.
8) Usage of VBScripts: Threat actors leverage VBScripts
as a versatile tool for executing commands aimed at network
manipulation, file system tampering, disruption of normal
system operations, and manipulating Windows Management
Instrumentation (WMI).
In a sample script, it executes a series of "netsh" commands,
allowing threat actors to modify "IPv4" and "IPv6" settings,
establish "IPsec" policies and filter lists, and control network
traffic by adding filters on specific ports and protocols. This
demonstrates threat actors interact with the Windows environ-
ment, enabling the alteration of critical network configurations
via VBScripts.


---

Additionally, the script showcases attempts to manipulate
default system files, such as "jscript.dll" and "cscript.exe", by
taking ownership and adjusting access permissions. The "take-
own" command is used to take ownership of the specified files,
allowing threat actors to gain control over them. Subsequently,
the "cacls" command is utilized to modify access control lists
(ACLs), restricting permissions for the ""everyone"" group
and effectively denying access to these files. This strategy
aims to impede the execution of scripts and hinder security
mechanisms that rely on these files.
The script also uses the Start-Sleep and "Restart-Computer
-Force" commands. The deliberate use of delays, such as
the "15-minute" pause before a system restart, suggests an
evasion tactic to evade immediate detection and response.
Overall, threat actors employ VBScripts due to their ease of
use, integration with Windows systems, and ability to execute
various commands, making them a potent tool in the arsenal
of cyber adversaries for carrying out disruptive actions [36].
Furthermore, the script employs conditional statements to
execute different payloads depending on the identified OS
version. For instance, it attempts to install an MSI package
silently when running on "Windows XP" or "Windows Vista",
and it executes encoded PowerShell commands when running
on "Windows 7".
9) Disrupting Competing Mining Services: On the other
hand, the scripts were observed with preparing the mining en-
vironment by removing previous miner instances. The scripts
employ several built-in methods and parameters, such as "sc
stop" and "sc delete" for stopping and deleting other miners
services such as named "gado_miner" and "taskkill /f /t"
to forcefully terminate the processes such as "xmrig.exe",
"logback.exe". The scripts attempt directory removal using
"rmdir /q /s" to recursively delete the other miner directories
such as ""mimu6"". An error-checking mechanism verifies the
successful removal of the directory and repeats the removal
attempt until successful or until a specified condition is met
[34].
The scripts also use "taskkill /F /PID <PID>" command
to eradicate processes and files associated with cryptocur-
rency mining activities systematically targeting specific pro-
cess names. The scripts terminate them and remove their
associated temporary directories in the Temp folder.
Also, the scripts include "netstat -ano | findstr TCP" to
identify any process operating on ports 3333, 4444, 5555,
7777, 9000 and stop the running processes [34] to disable
the other mining services.
E. TA0006 Credential Access
Upon compromising an endpoint within an environment,
cryptojacking scripts turn to PowerShell for credential access.
They use brute-force attacks on the other server account
credentials, such as the Microsoft SQL server. This process
involves utilizing a password, hash dictionary, and an array of
NTLM hashes in a "pass the hash" attack. This phase encom-
passes activities focused on acquiring valid account credentials
to gain unauthorized access to systems and resources.
Threat actors commonly utilize Mimikatz by executing
the commands specific parameters such as "log" to en-
able logging, "privilege::debug" to grant debug privileges,
"sekurlsa::logonpasswords" for extracting plaintext passwords
from the LSASS memory, and "sekurlsa::tickets /export" to
export Kerberos tickets, all culminating with the exit directive.
The attackers also employ a VBScript (launch.vbs) to execute
Mimikatz with elevated privileges, requesting administrative
access through runas extracting credentials and exporting
Kerberos tickets [30].
In a compromised environment, cryptojacking scripts lever-
age PowerShell to randomly generate IP addresses for potential
targets, enabling port scans and exploiting vulnerabilities in
services like SMB and MS-SQL. To compile a list of target IP
addresses, these scripts use PowerShell features like "ipconfig"
and "netstat", along with regular expression matching, array
manipulation, and web requests.
Attackers scan for vulnerable machines, specifically on
various versions of the Windows operating system. The scan
identifies potentially vulnerable endpoints, and the attacker
exploits the target system upon discovery. Specifically, these
scripts use PowerShell’s "System.Net.Sockets.TcpClient" .NET
class to establish network connections, primarily for scanning
IP addresses. The scripts focus on identifying open port 445
for exploitation. Depending on the Windows version, the script
executes specific functions, ultimately compromising the target
and advancing the attacker’s goals. This phase involves active
code execution to exploit vulnerabilities and gain unauthorized
access. It is worth noting that Lemon Duck scripts employ the
PingCastle EternalBlue vulnerability scanner [41].
F. TA0007 Discovery
Upon securing a substantial foothold within the network
with the executions and persistence mechanisms of crypto-
jacking attacks, the threat actors execute PowerShell com-
mands targeting the Active Directory. A sample command
"powershell.exe get-adcomputer -filter * -properties * | select
name, operatingsystem, ipv4address >", was seen as designed
to extract a comprehensive list of all machines affiliated with
the domain. This action provided the malicious actors with
valuable information, including the names, operating systems,
and IPv4 addresses of connected machines, enabling them
to strategize further and escalate their activities within the
compromised network [28].
Also, the cryptojacking scripts were observed using the
command "net accounts" to display and configure the network-
wide user account settings on a local system [30].
Additionally, the scripts were seen downloading strings
from remote servers, passing encoded information about the
system’s domain and the presence of specific software such
as Veeam [8]. The specific parameters, representing the URL-
encoded domain and the specific software presence informa-
tion, respectively, are appended to the URL. This dynamic
parameterization allows threat actors to customize the informa-
tion sent to the remote server based on the specific attributes
of the target system. By querying the system’s domain and


---

identifying the presence of specific software, attackers gain
insights into the organizational structure and potentially exploit
vulnerabilities associated with specific software installations.
G. TA0008 Lateral Movement
Lemon Duck cryptojacking employs various PowerShell
techniques for lateral movement within a compromised net-
work. The scripts are observed utilizing EternalBlue for
SMB exploitation, scanning machines for vulnerabilities, and
launching attacks based on the target’s Windows OS version.
In a sample script, the actors scan the network that responds
on 445/TCP using a tool called PingCastle to see if they are
susceptible to the EternalBlue vulnerability. Additionally, the
can leverage USB and network drives by writing malicious
Windows *.lnk shortcut files and DLL files to removable
storage connected to infected machines. The scripts might also
engage in Pass-the-Hash attacks, verifying user privileges and
using NTLM hashes to upload malicious scripts and associated
files to remote machines in the network. Furthermore, the
malicious scripts may conduct MS-SQL Server brute-forcing
by attempting various passwords for the specific user accounts
and RDP brute-forcing by cycling through a list of hardcoded
passwords to gain unauthorized access. These lateral move-
ment techniques, coupled with the continuous monitoring and
reporting to the command-and-control server, enable Lemon
Duck to persistently propagate and conduct cryptojacking
activities across the network [14].
Also, the sample scripts show that the script employs a
"foreach loop" to iterate through a list of IP addresses with
open RDP ports stored in an array. For each IP address, the
script checks whether it meets specific conditions, including
not being present in an array and having a length greater than
"6" characters. This ensures that the script focuses on unique
and potentially vulnerable RDP targets. Within the loop, the
script initiates an RDP brute-force attack by iterating through a
list of passwords stored in an array . For each password, it uses
an object ("RDP.BRUTE" in the sample script), instantiating
it with the current IP, the username "administrator," and the
password for the RDP login attempt [14].
H. TA0011 Command and Control
Cryptojacking scripts, executed within PowerShell, were
observed to have command and control (C2) capability to
report important machine profile details and module statuses
to a central C2 server. By collecting essential system data like
MAC address, UUID, and computer name, the script utilizes
the Net.WebClient class and the DownloadString method to
relay this information. It transmits comprehensive data, en-
compassing system statistics, open port counts, IP addresses,
and module execution details. This continuous communication
allows the attacker to maintain real-time oversight of the
compromised system’s environment, adjusting their strategy
based on insights into user accounts, system configuration,
privileges, exploitation and mining module statuses, and more.
The scripts also manipulate port openings and firewall rules
and set up port proxies.
The script leverages the native netsh command-line utility,
employing a range of parameters and arguments for various
tasks. These include the "firewall" parameter, which configures
the Windows Firewall; the "add portopening" parameter used
to create new port opening rules in the Windows Firewall;
and the "TCP" parameter specifying rules for TCP traffic.
Additionally, the script utilizes "interface portprox" to config-
ure port proxying on the network interface. It employs "add
v4tov4" to create IPv4-to-IPv4 port proxy rules, facilitating
traffic forwarding from one IPv4 address/port to another IPv4
address/port. "Listenport" designates the port where the proxy
listens for incoming traffic, while "connectaddress" determines
the destination IPv4 address to which incoming traffic is
forwarded. Lastly, "connectport" specifies the port at the
destination address to which incoming traffic is forwarded.
The unauthorized cryptocurrency mining activity, in addi-
tion to cryptojacking, poses a risk of deploying extra malicious
scripts for remote command and control (C2). In a sample
attack [8], backdoors were introduced alongside the crypto-
jacking operation, showcasing the script’s dual functionality.
The script establishes a persistent reverse shell through a
continuous ’"while"’ loop, utilizing a TCP connection with the
"Net.Sockets.TCPClient" class to communicate with a remote
server. Bidirectional communication allows threat actors to ex-
ecute commands remotely, enabling activities like data exfiltra-
tion and lateral movement. The "GetStream()" method obtains
a network stream for data transmission, and "IO.StreamWriter"
facilitates writing data using the "WriteToStream" function.
The continuous loop and dynamic command execution en-
hance flexibility. Features like a prompt "SHELL>" con-
tribute to maintaining interactivity. Subsequently, the script
decodes and executes received commands using "Invoke-
Expression". The command output is returned to the attacker
by establishing a bidirectional communication channel through
"WriteToStream". The inclusion of a delay, DNS client cache
clearing using "Clear-DnsClientCache", and hidden window
style contributes to persistence, bidirectional communication,
and evasion techniques, highlighting its adaptability for mul-
tifaceted malicious operations.
VI. CONCLUSION
In this paper, we first reviewed PowerShell-based fileless
cryptojacking attacks, specifically focusing on unauthorized
coinminer deployments that operate in-memory (RAM), orig-
inating from prevalent cryptojacking malware families. Sub-
sequently, we analyzed collected fileless cryptojacking scripts
within the MITRE ATT&CK framework. Our findings high-
light an increased effectiveness in fileless cryptojacking, at-
tributed to the rise of new Remote Code Execution (RCE) vul-
nerabilities and the integration of penetration testing tools like
Cobalt Strike, aligning it with the prevalence of another com-
mon threat, ransomware. During the execution phase, these
scripts consistently leverage standard PowerShell exploitation
parameters to evade detection, often utilizing platforms like
Pastebin. In the persistence phase, the employed techniques
share similarities with other attacks, but a notable observation


---

is the intentional disabling of competitive coinminers. This
logic extends to the defense evasion step, wherein exclusions
for coinminer scripts are deliberately established. The creden-
tial access, discovery, lateral movement, and command-and-
control phases exhibit similar attack patterns consistent with
attacks aiming for domain-wide impact.
The identified patterns are summarized in a table, and
specific details regarding these patterns are elaborated in
the research. This offers an opportunity to leverage Natural
Language Processing (NLP) and deep learning methods for
analyzing the textual data of PowerShell scripts, facilitating
the development of more effective detection methods in future
research.
REFERENCES
[1] D. Hendler, S. Kels, and A. Rubin, “Amsi-based detection of malicious
powershell code using contextual embeddings,” in Proceedings of the
15th ACM Asia Conference on Computer and Communications Security,
2020, pp. 679–693.
[2] R.
Canary,
“2023
red
canary
threat
detection
report,”
Jun
2023.
[Online].
Available:
https://redcanary.com/resources/guides/
threat-detection-report/
[3] A. Afreen, M. Aslam, and S. Ahmed, “Analysis of fileless malware
and its evasive behavior,” in 2020 International Conference on Cyber
Warfare and Security (ICCWS).
IEEE, 2020, pp. 1–8.
[4] S. Varlioglu, N. Elsayed, Z. ElSayed, and M. Ozer, “The dangerous
combo: Fileless malware and cryptojacking,” SoutheastCon 2022, pp.
125–132, 2022.
[5] M. N. Olaimat, M. A. Maarof, and B. A. S. Al-rimy, “Ransomware
anti-analysis and evasion techniques: A survey and research directions,”
in 2021 3rd international cyber resilience conference (CRC).
IEEE,
2021, pp. 1–6.
[6] J. Piet, B. Anderson, and D. McGrew, “An in-depth study of open-
source command and control frameworks,” in 2018 13th International
Conference on Malicious and Unwanted Software (MALWARE), 2018,
pp. 1–8.
[7] T. Nelson and H. Kettani, “Open source powershell-written post ex-
ploitation frameworks used by cyber espionage groups,” in 2020 3rd
International Conference on Information and Computer Technologies
(ICICT), 2020, pp. 451–456.
[8] G. S. Gabor Szappanos and S. Gallagher, “Horde of miner bots and
backdoors leveraged log4j to attack vmware horizon servers,” Mar
2022. [Online]. Available: http://tinyurl.com/miner-bots-log4j
[9] A. Bulazel and B. Yener, “A survey on automated dynamic malware
analysis evasion and counter-evasion: Pc, mobile, and web,” in Pro-
ceedings of the 1st Reversing and Offensive-oriented Trends Symposium,
2017, pp. 1–21.
[10] Microsoft,
“Fileless
threats,”
2021.
[Online].
Available:
https://docs.microsoft.com/en-us/windows/security/threat-protection/
intelligence/fileless-threats
[11] P.
Newton,
“Analysing
fileless
malware:
Cobalt
strike
beacon,”
Jul
2020.
[Online].
Available:
https://newtonpaul.com/
analysing-fileless-malware-cobalt-strike-beacon/
[12] W. Handaya, M. Yusoff, and A. Jantan, “Machine learning approach
for detection of fileless cryptocurrency mining malware,” in Journal of
Physics: Conference Series, vol. 1450, no. 1.
IOP Publishing, 2020, p.
012075.
[13] R. Moussaileb, N. Cuppens, J.-L. Lanet, and H. L. Bouder, “A survey
on windows-based ransomware taxonomy and detection mechanisms,”
ACM Computing Surveys (CSUR), vol. 54, no. 6, pp. 1–36, 2021.
[14] R. Nataraj, V. Singh, and M. Wood, “Lemon duck powershell
malware cryptojacks enterprise networks,” 2019. [Online]. Available:
https://tinyurl.com/yc4fmkdz
[15] L. Gundert. [Online]. Available: https://go.recordedfuture.com/hubfs/
reports/rep-2016-9006.pdf
[16] E. Nakashima and C. Timberg, “Nsa officials worried about the day
its potent hacking tool would get loose. then it did,” Washington Post,
vol. 16, 2017.
[17] P.
A.
Macaraeg,
Arvin
Roi;
Roderno,
“Trojan.ps1.pcastle.b,”
2019.
[Online].
Available:
https://www.trendmicro.com/vinfo/us/
threat-encyclopedia/malware/trojan.ps1.pcastle.b
[18] “Powershell,”
2018.
[Online].
Available:
https://hunter2.gitbook.io/
darthsidious/enumeration/powershell
[19] T. Micro, “Lemon duck cryptocurrency-mining malware information,”
2020.
[Online].
Available:
https://success.trendmicro.com/solution/
000261916
[20] V. V. Koushik, “Lemon duck malware : Infecting outdated windows
systems
using
eternalblue,”
Ssecpod,
2020.
[Online].
Available:
https://www.secpod.com/blog/lemon-duck-malware/
[21] M00nRise, “Post-exploitation tool for hiding processes from monitoring
applications,” 2016. [Online]. Available: https://github.com/M00nRise/
ProcessHider/blob/master/PowerShell/Invoke-ReflectivePEInjection.ps1
[22] C.
G.
S.
Team,
“Threat
alert:
Lemonduck
crypto-mining
malware.”
[Online].
Available:
https://www.cybereason.com/blog/
research/threat-alert-lemonduck-crypto-mining-malware
[23] T. Caldwell, “The miners strike–addressing the crypto-currency threat
to enterprise networks,” Computer Fraud & Security, vol. 2018, no. 5,
pp. 8–14, 2018.
[24] C. M. Pascual, “Ghostminer weaponizes wmi, kills other mining
payloads,” 2019. [Online]. Available: https://tinyurl.com/2w49k6v3
[25] J. Agcaoili, “Monero-mining malware pcastle uses fileless techniques,”
2019. [Online]. Available: https://tinyurl.com/4kh3f3x5
[26] S.
Gallagher,
“Two
flavors
of
tor2mine
miner
dig
deep
into
networks with powershell, vbscript,” Dec 2021. [Online]. Available:
http://tinyurl.com/tor2mine-powershell
[27] MITRE, “Command and control,” The MITRE Corporation MITRE
ATT&CK, 2019. [Online]. Available: https://attack.mitre.org/tactics/
TA0011/
[28] C. CISA, “Iranian government-sponsored apt actors
compromise
federal network, deploy crypto miner, credential harvester: Cisa,”
Nov
2022.
[Online].
Available:
https://www.cisa.gov/news-events/
cybersecurity-advisories/aa22-320a
[29] T. Trellix, Aug 2022. [Online]. Available: http://tinyurl.com/trellix-miner
[30] D. DFIR-Report, “All that for a coinminer?” Jan 2021. [Online].
Available: https://thedfirreport.com/2021/01/18/all-that-for-a-coinminer/
[31] J. LEIN, “Sketchy powershell scripts on pastebin,” Aug 2021. [Online].
Available: https://jon-lein.github.io/Powershell_Malware_Pastebin/
[32] Patebin, “What is pastebin.com all about?” [Online]. Available:
https://pastebin.com/faq#1
[33] R.
Nataraj,
“New
lemon
duck
variants
ex-
ploiting
microsoft
exchange
server,”
May
2021.
[Online].
Available:
https://news.sophos.com/en-us/2021/05/07/
new-lemon-duck-variants-exploiting-microsoft-exchange-server/
[34] H.
Darley,
S.
Robinson,
and
R.
Ellis,
“Exploring
a
crypto-
mining campaign which used
the log4j vulnerability:
Darktrace
blog,”
Apr
2022.
[Online].
Available:
https://darktrace.com/blog/
exploring-a-crypto-mining-campaign-which-used-the-log-4j-vulnerability
[35] I. Patterson. [Online]. Available: https://nssm.cc/download
[36] G. Kristal, “Purple fox ek: New cves, steganography, and virtualization
added to attack flow - sentinellabs,” Oct 2020. [Online]. Available:
http://tinyurl.com/purple-fox-steganography
[37] J.
G.
SZÉLES,
Oct
2020.
[Online].
Available:
https://www.bitdefender.com/files/News/CaseStudies/study/373/
Bitdefender-PR-Whitepaper-LemonDuck-creat4826-en-EN-GenericUse.
pdf
[38] B. Helps, M. Crossan, and C. Stewart, Apr 2022. [Online]. Available:
https://www.foregenix.com/blog/an-overview-on-purple-fox
[39] J. Triunfante, E. M. Earnshaw, and M. J. Ofiaza, “Purple fox’
malware can rootkit and abuse powershell,” 2019. [Online]. Available:
https://tinyurl.com/2w6vzbc6
[40] B. Bojan, “Purple fox - a comparison of old and new techniques
in the exploitation phase,” Sep 2022. [Online]. Available: https:
//diverto.github.io/2020/09/22/purple-fox
[41] PingCastle, “Pingcastle vulnerability scanner,” Oct 2022. [Online].
Available: https://www.pingcastle.com/documentation/scanner/
