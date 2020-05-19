---
title: DPoP Attacker Model
layout: publication
type: Analysis
toc: yes
---

This document outlines attacker models considered for [DPoP](https://tools.ietf.org/html/draft-ietf-oauth-dpop). 
<!--more-->

> **Note:** DPoP is still an IETF working group draft. This is not a normative document and the final attacker model for DPoP might look different to the one presented here!


<div class="alert alert-info" role="alert">
  <b>Disclaimer:</b> This document discusses theoretical or practical attacks on OAuth or OpenID Connect. Nonetheless, both standards can be used securely as shown by, among others, formal analyses. With the appropriate security mechanisms, both are even suitable for high-risk environments. As with any security protocol, a careful evaluation of potential threats and the required security mechanisms is indispensable when designing a solution based on OAuth/OpenID Connect.
</div>

## Misconfigured Resource Endpoint

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

<img src="/img/plantuml/0cdb925a9cdcdfac505159dee8588fb659060cc0917f7f001bb27fd81a202fd6.svg" class="svg">


## Compromised/Malicious Resource Server

One of multiple resource servers can become compromised or act maliciously for other reasons.

<img src="/img/plantuml/0a9f7a2b950fe131bcd3622b7c4a652744a24388eae986cb96bffbe05aece232.svg" class="svg">

If TLS termination is done at a separate component at the resource server, that component can become compromised, for example by exploting a buffer overflow attack in the reverse proxy: 

<img src="/img/plantuml/d7ebccf61f43d00d5b2b7881874ea14da4965bf9142d40bbf512d4b5f9ddd3d9.svg" class="svg">


## Stolen Token (XSS)

An attacker can leverage an XSS attack to exfiltrate the access token from a single page application. The attacker then tries to use the token. It is not required that the victim is still online for this attack.

<img src="/img/plantuml/a423b5d72e059a385a1f3ca8e6d1af6315d35850fb1e7908f4ba33a31b3ab37c.svg" class="svg">


## XSS (Victim is Online)

If a user's browser is online and an attacker has injected JavaScript code into the client's SPA,  the attacker can use the token without exfiltrating it first. There is most likely no defense against this threat except preventing XSS.

<img src="/img/plantuml/344c65fd8ad56bd7ee740331acd651ebe568cd9924f43e1cd033c2ee99929d79.svg" class="svg">

> **Note:** It is in general hard or impossible to defend against this threat. It should therefore be considered out of the scope of DPoP.


## Precomputed Proofs

If the attacker is able to precompute DPoP tokens, or is able to exfiltrate the secret key needed for generating DPoP proofs along with the access token, DPoP does not protect the access token if no server-generated nonce is used in the proof.

<img src="/img/plantuml/185817e572aa17d3d09f852df76fc925ae2a908bd130bc706fc27a5b53f1db3d.svg" class="svg">

> **Recommendation:** Requiring/allowing for a server-sent nonce via the WWW-Authenticate header would improve the security of DPoP.

## Exfiltration from Otherwise Secure Channel

Attacks on TLS might allow for the recovery of strings in encrypted messages that are repeated in multiple messages. One example would be the BREACH attacks against HTTP compression.

<img src="/img/plantuml/41ea6ca0990bcaf9081318f983ef4208426beae62c11d94ac9952c2d2248994e.svg" class="svg">


**Update 1:** Added the correct variant of Online XSS; renamed the one that was previously there to "Precomputed proofs"; added "Exfiltration from Otherwise Secure Channel". Thanks, Neil!