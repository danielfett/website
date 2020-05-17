---
title: DPoP Attacker Model
layout: publication
type: Analysis
toc: yes
---

This document outlines attacker models considered for [DPoP](https://tools.ietf.org/html/draft-ietf-oauth-dpop). 

> **Note:** DPoP is still an IETF working group draft. This is not a normative document and the final attacker model for DPoP might look different to the one presented here!

# Misconfigured Resource Endpoint

A resource endpoint is misconfigured. For example, if OAuth Metadata is used, the following configuration can lead to the userinfo endpoint being under the control of the attacker:

```json
{
    "issuer": "https://attacker.com",
    "authorization_endpoint": "https://honest.com/authorize",
    "token_endpoint": "https://honest.com/token",
    "userinfo_endpoint": "https://attacker.com/userinfo"
}
```
Note that the userinfo endpoint points to an attacker-controlled site.

Attack:

```plantumlcode
@startuml
participant Browser
participant client.com
participant AS
participant attacker.com <<Attacker>>
participant RS


Browser -> client.com: Start
client.com -> Browser: Authz Request
Browser -> AS: Authz Request
Browser <--> AS: authn, authz
AS -> Browser: Authorization Response
Browser -> client.com: Authorization Response
client.com -> AS: Token Request
AS -> client.com: Token Response
client.com -> attacker.com: POST https://attacker.com/resource\nAuthorization: <font color=blue>Bearer 42xyz...</font>
attacker.com -> RS: <font color=red>POST https://rs.com/resource</font>\nAuthorization: <font color=blue>Bearer 42xyz...</font>
@enduml

```


# Compromised/Malicious Resource Server

One of multiple resource servers can become compromised or act maliciously for other reasons.

```plantumlcode
@startuml
participant Browser
participant client.com
participant AS
participant RS1 <<Attacker>>
participant RS2

Browser -> client.com: Start
client.com -> Browser: Authz Request
Browser -> AS: Authz Request
Browser <--> AS: authn, authz
AS -> Browser: Authorization Response
Browser -> client.com: Authorization Response
client.com -> AS: Token Request
AS -> client.com: Token Response
client.com -> RS1: POST https://rs1.com/resource\nAuthorization: <font color=blue>Bearer 42xyz...</font>
RS1 -> RS2: <font color=red>POST https://rs2.com/resource</font>\nAuthorization: <font color=blue>Bearer 42xyz...</font>
@enduml
```

If TLS termination is done at a separate component at the resource server, that component can become compromised, for example by exploting a buffer overflow attack in the reverse proxy: 

```plantumlcode
@startuml
participant Browser
participant client.com
participant AS
box RS1
participant RS1TLS <<Attacker>>
participant RS1Service
end box 
participant RS2

Browser -> client.com: Start
client.com -> Browser: Authz Request
Browser -> AS: Authz Request
Browser <--> AS: authn, authz
AS -> Browser: Authorization Response
Browser -> client.com: Authorization Response
client.com -> AS: Token Request
AS -> client.com: Token Response
client.com -> RS1TLS: POST https://rs1.com/resource\nAuthorization: <font color=blue>Bearer 42xyz...</font>
RS1TLS -> RS1Service: POST http://service/resource\nAuthorization: <font color=blue>Bearer 42xyz...</font>
RS1TLS -> RS2: <font color=red>POST https://rs2.com/resource</font>\nAuthorization: <font color=blue>Bearer 42xyz...</font>
@enduml
```


# Stolen Token (XSS)

An attacker can leverage an XSS attack to exfiltrate the access token from a single page application. The attacker then tries to use the token. It is not required that the victim is still online for this attack.

```plantumlcode
@startuml
participant Browser as "Browser\nw/ JS client"
participant AS
participant attacker.com <<Attacker>>
participant RS


Browser -> AS: Authz Request
Browser <--> AS: authn, authz
AS -> Browser: Authorization Response
Browser -> AS: Token Request
AS -> Browser: Token Response
Browser -> RS: POST https://rs.com/resource\nAuthorization: <font color=blue>Bearer 42xyz...</font>
Browser --> attacker.com: <font color=red>Exfiltrate Token
attacker.com -> RS: <font color=red>POST https://rs.com/resource</font>\nAuthorization: <font color=blue>Bearer 42xyz...</font>
@enduml

```


# XSS (Victim is Online)

If a user's browser is online and an attacker has injected JavaScript code into the client's SPA,  the attacker can use the token without exfiltrating it first. There is most likely no defense against this threat except preventing XSS.

```plantumlcode
@startuml
participant Browser as "Browser\nw/ JS client"
participant AS
participant RS


Browser -> AS: Authz Request
Browser <--> AS: authn, authz
AS -> Browser: Authorization Response
Browser -> AS: Token Request
AS -> Browser: Token Response
Browser -> RS: POST https://rs.com/resource\nAuthorization: <font color=blue>Bearer 42xyz...</font>
Browser -> RS: <font color=red>POST https://rs.com/resource</font>\nAuthorization: <font color=blue>Bearer 42xyz...</font>
@enduml

```

> **Note:** It is in general hard or impossible to defend against this threat. It should therefore be considered out of the scope of DPoP.


# Precomputed Proofs

If the attacker is able to precompute DPoP tokens, or is able to exfiltrate the secret key needed for generating DPoP proofs along with the access token, DPoP does not protect the access token if no server-generated nonce is used in the proof.

```plantumlcode
@startuml
participant Browser as "Browser\nw/ JS client"
participant AS
participant attacker.com <<Attacker>>
participant RS


Browser -> AS: Authz Request
Browser <--> AS: authn, authz
AS -> Browser: Authorization Response
Browser -> AS: Token Request
AS -> Browser: Token Response
Browser -> RS: POST https://rs.com/resource\nAuthorization: <font color=blue>Bearer 42xyz...</font>
Browser --> attacker.com: <font color=red>Exfiltrate precalculated DPoP Proofs
attacker.com -> RS: <font color=red>POST https://rs.com/resource</font>\nAuthorization: <font color=blue>Bearer 42xyz...</font>
@enduml

```

> **Recommendation:** Requiring/allowing for a server-sent nonce via the WWW-Authenticate header would improve the security of DPoP.

# Exfiltration from Otherwise Secure Channel

Attacks on TLS might allow for the recovery of strings in encrypted messages that are repeated in multiple messages. One example would be the BREACH attacks against HTTP compression.

```plantumlcode
@startuml
participant Browser
participant client.com
participant AS
participant attacker.com <<Attacker>>
participant RS


Browser -> client.com: Start
client.com -> Browser: Authz Request
Browser -> AS: Authz Request
Browser <--> AS: authn, authz
AS -> Browser: Authorization Response
Browser -> client.com: Authorization Response
client.com -> AS: Token Request
AS -> client.com: Token Response
client.com -> RS: POST https://attacker.com/resource\nAuthorization: <font color=blue>Bearer 42xyz...</font>
attacker.com -> RS: <font color=red>POST https://rs.com/resource</font>\nAuthorization: <font color=blue>Bearer 42xyz...</font>
@enduml

```


**Update 1:** Added the correct variant of Online XSS; renamed the one that was previously there to "Precomputed proofs"; added "Exfiltration from Otherwise Secure Channel". Thanks, Neil!