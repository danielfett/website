---
title: DPoP Attacker Model
layout: publication
type: Analysis
toc: yes
---

This document outlines attacker models considered for [DPoP](https://tools.ietf.org/html/draft-ietf-oauth-dpop). 

> **Note:** DPoP is still an IETF working group draft. This is not a normative document and the final attacker model for DPoP might look different to the one presented here!

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

<img src="/img/plantuml/5c161c080fe8a210ac7c45a2cf1aa838b53f55d3d16a55f2730dd3697d22e33e.svg" class="svg">


## Compromised/Malicious Resource Server

One of multiple resource servers can become compromised or act maliciously for other reasons.

<img src="/img/plantuml/9479dfbf4a3992fe996b83b57d83f5cadf5094002aca59d58c70a9ae1b5f18b9.svg" class="svg">

If TLS termination is done at a separate component at the resource server, that component can become compromised, for example by exploting a buffer overflow attack in the reverse proxy: 

<img src="/img/plantuml/4d7c16c317b52a0160ada12f2bbab290d20a795f278484a134dc47e2da0e884f.svg" class="svg">


## Stolen Token (XSS)

An attacker can leverage an XSS attack to exfiltrate the access token from a single page application. The attacker then tries to use the token. It is not required that the victim is still online for this attack.

<img src="/img/plantuml/12556c20452b9f5fe5d70fc66979105fc2d16e4af725af52d4f467763d71692f.svg" class="svg">


## XSS (Victim is Online)

If a user's browser is online and an attacker has injected JavaScript code into the client's SPA,  the attacker can use the token without exfiltrating it first. There is most likely no defense against this threat except preventing XSS.

<img src="/img/plantuml/acf60eb5a18b637e517ea8255c539e3f3e0b71cd8fb81a0f864735cbeb11bec2.svg" class="svg">

> **Note:** It is in general hard or impossible to defend against this threat. It should therefore be considered out of the scope of DPoP.


## Precomputed Proofs

If the attacker is able to precompute DPoP tokens, or is able to exfiltrate the secret key needed for generating DPoP proofs along with the access token, DPoP does not protect the access token if no server-generated nonce is used in the proof.

<img src="/img/plantuml/1c74e8f87f86bd3cd6e9affdf4247437aeaaf8c6e8e98d1590dfb6e1fb5a31fc.svg" class="svg">

> **Recommendation:** Requiring/allowing for a server-sent nonce via the WWW-Authenticate header would improve the security of DPoP.

## Exfiltration from Otherwise Secure Channel

Attacks on TLS might allow for the recovery of strings in encrypted messages that are repeated in multiple messages. One example would be the BREACH attacks against HTTP compression.

<img src="/img/plantuml/5fb7ede5171b7c491d8d070e1a291e359f8925b4f1d84704bc7f81b6c5176e93.svg" class="svg">


**Update 1:** Added the correct variant of Online XSS; renamed the one that was previously there to "Precomputed proofs"; added "Exfiltration from Otherwise Secure Channel". Thanks, Neil!