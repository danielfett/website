---
title: "PKCE vs. Nonce: Equivalent or Not?"
layout: publication
toc: yes
type: Analysis
---


Traditionally, the `state` parameter is used to provide protection against Cross-Site Request Forgery (CSRF) attacks on OAuth. The newer mechanisms [PKCE (RFC7636)](https://tools.ietf.org/html/rfc7636) and the [OpenID Connect parameter nonce](https://openid.net/specs/openid-connect-core-1_0.html) not only protect against CSRF, but they also provide some level of protection against [Code Injection](https://elib.uni-stuttgart.de/bitstream/11682/10214/1/%27An%20Expressive%20Formal%20Model%20of%20the%20Web%20Infrastructure.pdf) attacks.

In this  document, I evaluate (informally) the differences in the provided protection levels of `state`, PKCE, and Nonce against CSRF and misuse of stolen codes.
<!--more-->

<div class="alert alert-info" role="alert">
  <b>Disclaimer:</b> This document discusses theoretical or practical attacks on OAuth or OpenID Connect. Nonetheless, both standards can be used securely as shown by, among others, formal analyses. With the appropriate security mechanisms, both are even suitable for high-risk environments. As with any security protocol, a careful evaluation of potential threats and the required security mechanisms is indispensable when designing a solution based on OAuth/OpenID Connect.
</div>

## The Mechanics

Let's start with a quick recap on the technical details of PKCE and Nonce.

### PKCE

PKCE is defined in [RFC7636](https://tools.ietf.org/html/rfc7636). Here, I only consider the SHA256 code challenge method, which works as follows: The client selects a fresh random number (nonce). It hashes the nonce and sends it in the `code_challenge` parameter to the authorization server. In the token request, the client sends the original nonce in the `code_verifier` parameter. The authorization server compares the hash of the `code_verified` to the `code_challenge` and responds with the access token iff and only if they match.

PKCE was originally designed for the use with public clients, but can be used for all OAuth authorization code grants independent of the client type.

<img src="/img/plantuml/d076e74ea24966c9642b65c355fff8f27d47e1828194be9aefcaef47ad3364df.svg" class="svg">

### Nonce

The nonce parameter and ID token claim is defined in [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html). As with PKCE, the client again selects a fresh random value at the start of the flow. This value is sent to the server in the `nonce` parameter. The server embeds the nonce into the ID tokens issued in the authorization response and/or in the token response. The client compares the `nonce` in the ID Token(s) to the one sent in the authorization request and only proceeds if they match.

ID tokens are signed and optionally encrypted. If ID tokens are only returned from the token endpoint, they may be signed using the "none" algorithm, which provides no integrity protection.

<img src="/img/plantuml/f395d98e4107bb60c69956977caed64705c4e43b5ac4bec7e7f7451265c530e3.svg" class="svg">

The usage of nonce is mandated by OpenID Connect Core for some flows:

| Flow                    | `response_type`                                                      | Nonce    |
| ----------------------- | -------------------------------------------------------------------- | -------- |
| authorization code flow | `code`                                                               | OPTIONAL |
| implicit flow           | `id_token` &middot; `id_token token`                                 | REQUIRED |
| hybrid flow             | `code id_token` &middot; `code token` &middot; `code id_token token` | OPTIONAL |

Of course, to have an effect against CSRF and Code Injection, Nonce must be used even if it is optional in OpenID Connect.

#### Binding between ID Token and Authorization Code

ID tokens can contain a `c_hash` claim containing a hash of the code issued in the flow. The `c_hash` claim must be included in the ID token and checked by the client "if the ID Token is issued from the Authorization Endpoint" (along with a code):


| `response_type`                                                            | `c_hash` |
| -------------------------------------------------------------------------- | -------- |
| `code` &middot; `code token` &middot; `id_token` &middot; `id_token token` | OPTIONAL |
| `code id_token` &middot; `code id_token token`                             | REQUIRED |

#### Binding between ID Token and Access Token

Similar to `c_hash`, ID tokens can contain the claim `at_hash` to bind the access token to the ID token. 

The `at_hash` claim must be included in the ID token and checked by the client according to the following table:


| `response_type`                                                           | `at_hash` |
| ------------------------------------------------------------------------- | --------- |
| `code` &middot; `code token` &middot; `id_token` &middot; `code id_token` | OPTIONAL  |
| `code id_token token` &middot; `id_token token`                           | REQUIRED  |

`c_hash`  and `at_hash` MAY be omitted from the id token returned in the token response.

## Cross-Site Request Forgery

In a Cross-Site Request Forgery (CSRF) attack, an attacker tries to inject an authorization response into a user's browser, for example, by redirecting the victim's browser to a crafted authorization response URL pointing to the OAuth client. 


### Network Attacker Setting
The standard [web attacker model](https://tools.ietf.org/html/draft-ietf-oauth-security-topics) is normally sufficient to perform CSRF attacks. Here, we assume that all connections are properly protected using TLS and therefore apply the stronger network attacker model. (See, for example, [our OAuth paper](https://danielfett.de/publications/2016-01-06-oauth-security-analysis/) for a more detailed description of the attacker model.) 

#### PKCE & CSRF

PKCE protects against the network attacker because the attacker would need to inject a code that is bound to the same code challenge that was used initially by the client. While the attacker can create codes bound to arbitrary code challenges (by using the client and authorzation server) the attacker cannot know the code challenge in this case.

> **Attack mitigated:** The AS will reject the token request if the attacker tries to inject a code via CSRF.

#### Nonce & CSRF

For the Nonce mechanism, it is useful to distinguish the flows by the endpoints where ID tokens are issued.

##### ID Token only in Token Response

First, let's assume that  a client uses Nonce and the response types `code` or `code token` (i.e., without an ID token in the authorization response). In this case, the attacker needs to inject a code that causes the AS to return (from the token endpoint) an ID token containing the nonce that was used in the authorization request. The attacker would need to know the original nonce to generate this code (via the original client and the AS). As above, the attacker cannot know the nonce.

> **Note:** At this point, the client has already received data that may have incurred expenses at the authorization server and that the client must not use. 

> **Note:** The use of nonce is optional in these flows. The client must not skip the check for the nonce parameter if none is provided in the ID token.

##### ID Token only in Authorization Response

For the implicit grant response types (`id_token` and `id_token token`), the client already gets an ID token in the authorization response. 

Since the ID token must be signed, an attacker would need to know the nonce used in the authorization request to generate an ID token via the authorization server. As above, this effectively prevents CSRF.

##### ID Token in Authorization Response and Token Response

In essence, the same considerations as above apply. 

Even if the client only checks the nonce in one ID token, the attacker would still need to provide a code and an ID token referring to or containing the correct nonce. 

> **Note:** The use of nonce is optional in these flows. The client must not skip the check for the nonce parameter if none is provided in the ID token.

### Attacker with Access to the Authorization Request

If a web attacker has the ability to read the authorization request contents, neither PKCE nor Nonce provide protection against CSRF attacks: The attacker can simply start a new authorization flow using the same client and same authorization server and use the code generated by the AS in this flow to inject it into the victim's session.

### Attacker with Access to the Authorization Response

Under (very rare) circumstances, the protection provided by Nonce can be circumvented to launch a CSRF attack. The attacker needs the following abilities:

#### Variant 1: ID Token in Front Channel

 * Reading the authorization response, e.g., through a Referer header sent from the client's web site
 * Being able to read the nonce claim from an ID token in the authorization response (i.e., unencrypted ID tokens plus response type `id_token`, `id_token token`, `id_token code` or `code id_token token`)
 * Being able to either intercept the ID token before it is processed by the client or having a client that accepts multiple authorization responses in the same session

To launch the attack, the attacker would read the nonce from the ID token, generate a new ID token using the same client and inject the new ID token (potentially together with a new authorization code or access token) into the user's browser.

#### Variant 2: Without ID Token in Front Channel
If no ID token is sent in the front-channel (i.e., response type `code` or `code token`) or the ID token is encrypted, the attacker cannot read the nonce from the ID token. If the client is a public client, the attacker can, however, use the token endpoint of the AS as an oracle: By sending the captured code to the token endpoint, the attacker might be able to learn the nonce needed to create a spoofed authorization response. (This only works if the `nonce` claim is contained in the ID token sent from the token endpoint.)

Neither of these variants are possible with PKCE, as the code challenge or verifier are not exposed in the authorization response. Variant 1, however, applies if the `state` parameter is used for CSRF protection.

### Special Case: Error Responses

When `state` is used for CSRF protection, OAuth error responses from the authorization endpoint must contain this parameter as well, providing protection against attacker-forged error responses. If only PKCE or Nonce are used for CSRF protection, error responses can be spoofed. 

> **Recommendation:** Although the value of this attack seems to be limited, it might be worthwhile to think about proper defense mechanisms. One way would be to return the `code_challenge` or `nonce` in the error response to the client. Since it is already important that code challenges/verifiers and nonces must not be reused, there does not seem to be much value in hashing the `code_challenge` or `nonce` parameter before returning them to the client. 

### Downgrade Attack on PKCE

If an authorization server does not enforce PKCE, but instead detects client support by checking for a `code_challenge` parameter in the response, downgrade CSRF attacks are possible, as [pointed out by Nov Matake](https://mailarchive.ietf.org/arch/msg/oauth/qrLAf3nWRt8HAFkO49qGrPRuelo/). 

To conduct the attack, an attacker would just start an authorization flow with the targeted client, but remove the `code_challenge` parameter from the authorization request. If the authorization server allows for flows without PKCE, it will create a code that is not bound to a code challenge. The attacker can then inject this code into the user's session with the authorization server, even if PKCE was used in that session.


The following figure shows the attack:

<img src="/img/plantuml/b936c9ccd8c1ca76156cef40d4262ba1fa929fc43214cf2549d44176ba5b458b.svg" class="svg">

### CSRF: Summary

| Setting                                | Protection by `state` | by PKCE | by Nonce |
| -------------------------------------- | --------------------: | ------: | -------: |
| Network Attacker                       |                     ✔️ |       ✔️ |        ✔️ |
| Network Attacker + Authz Request Read  |                     ❌ |       ❌ |        ❌ |
| Network Attacker + Authz Response Read |                     ❌ |       ✔️ |      ✔️/❌ |
| Network Attacker (Error Response Case) |                     ✔️ |       ❌ |        ❌ |

## Misuse of Stolen Codes
If an attacker (web or network attacker) can acquire an authorization code from a user's session, there are in general two ways that the attacker could use this code.

 * If the client that was used by the victim does not have a form of client authentication (public client), the attacker can send the code to the token endpoint of the authorization server that issued the code. The authorization endpoint will exchange the code for an access token that the attacker can use to access the protected resources.
 * If the client is a confidential client, the attacker needs to use a technique called code injection: The attacker starts a new session with the same client that was used by the victim *on his own device*. In this session, the attacker replaces the code generated by the authorization server for the attacker's account by the stolen code. The client will therefore use the stolen code in the attacker's session and the attacker gets access to the victim's resources (via the client).


Since both attacks have very different security properties, I will evaluate them separately.

### Public Clients

First, assume that a code was stolen from an OAuth flow initiated by a public client.

Without any additional security measures, the attacker can just redeem the code at the token endpoint. Note that `state` does not prevent any form of this attack.

#### PKCE

When PKCE is used, the attacker would need to know the `code_verifier` that matches the `code_challenge` sent in the authorization request. The only party that can know the `code_verifier` is the client, where the value is securely bound to the user's session. As long as the attacker does not learn the user's session identifier with the client, there is no way for the attacker to make use of the code.


#### Nonce

Since Nonce is checked on the client, the attacker can just redeem the code himself at the token endpoint. Therefore, Nonce does not mitigate code misuse for public clients.

### Confidential Clients

Now, let's consider confidential clients where an attacker might be forced to use code injection to have the client redeem the code for him.

This figure shows a code injection attack (note again that the client and authorization server are the same in both sessions):

<img src="/img/plantuml/65d627f6be98213e441611b4f369788662d86ea4fce7a98817eaaa9ace0bfb22.svg" class="svg">

> **Note:** When a client uses dynamic client registration, for example on a mobile device of a user, an attacker might be unable to conduct a code injection attack even without further protection mechanisms, as he does not have access to the client that was used to create the code. This protection only works as long as an attacker is not able to conduct a [Mix-Up attack](https://danielfett.de/2020/05/04/mix-up-revisited/) in which he provides, in a metadata document, an attacker-controlled authorization endpoint but the original authorization server's token endpoint to the client.

#### PKCE

With PKCE, the same protection as for public clients kicks in: The attacker cannot use the code himself and cannot inject the code into a client, as there is not session where the client would use the correct `code_verfier` except the session between the user's browser and the client.

#### Nonce

For flows with Nonce, the attacker might already know the `nonce` parameter that is bound to the code: If an unencrypted ID token was issued in the front channel, it is likely that it leaked to the attacker in the same way as the code.

As far as I can see, however, this does not help the attacker. He would still need to get the (confidential!) client to expect the same nonce as the one bound to the code. In a sane client implementation, there is no way for the attacker to achieve this.

### Nonce/PKCE Sidestep Attack
PKCE and Nonce seem to be safe choices in defending against code injection attacks for confidential clients. Also, a combination of the two is safe (i.e., client and AS always use/expect both PKCE and Nonce). For public clients, PKCE must be used.

A circumvention of both mechanisms, however, is possible if an AS allows a client to choose between PKCE and Nonce and the client makes use of this freedom. I propose to call this attack the **Nonce/PKCE Sidestep Attack**.

Assume that the client uses PKCE for some flows (e.g., pure-OAuth flows) and Nonce for other flows (e.g., those using OpenID Connect) at the same authorization server. Now, an attacker who has stolen an authorization code that was bound to a Nonce could inject this code into a pure-OAuth authorization flow that uses PKCE. The client will send the code, along with a (now not matching) `code_verifier` to the server. The server will ignore the `code_verifier` (as it was not expected) and send back an access token and ID token to the client. The client will ignore the ID token (since it was not expected) but use the access token.


<img src="/img/plantuml/cfe0028cd6d8684230db3f609f0fd357ee3e516b0f58ecd8529d59f2c6eacb8a.svg" class="svg">
The root cause for the attack is that the client and the server allow for a dynamic switch between PKCE and Nonce flows.


> **Recommendation:** To avoid the Nonce to PKCE Sidestep Attack, clients **must not** switch between using only PKCE and only Nonce (but may use both in parallel, or switch between using only PKCE and PKCE+Nonce). Authorization servers **must enforce PKCE** unless they know that the client uses Nonce for **all** of its flows (and checks the Nonce value). The presence of a `nonce` parameter in the authorization request is **not sufficient** to determine if a client actually checks the `nonce` claim in the ID token.


### Side Note: Stronger Attacker Model
PKCE uses SHA256 to create the `code_challenge`. This is intended to prevent misuse of the stolen code even is an attacker can read the authorization request. Depending of the exact attack scenario, it might be a small step from reading the authorization request to actually injecting a new authorization request into the user's browser, although many details depend on the concrete deployment.

In this expanded attacker model (i.e., the attacker can inject the authorization request and read the authorization response), we have the same situation as in the PKCE Chosen Challenge attack described in our [paper on the security of FAPI](https://danielfett.de/publications/2019-02-01-openid-fapi-formal-analysis/) and [presented at IETF 105](https://datatracker.ietf.org/doc/slides-105-oauth-sessa-oauth-security-topics/). This can be considered a special case of code injection.

The same attack applies if Nonce is used to protect the flow. 

On the one hand, it is hard or impossible to protect any redirect-based protocols against these attacks. On the other hand, to perform the attack in practice, the attacker needs good timing and ideally some side-channel information about the user (e.g., knowing when the user wants to start an authorization flow).

### Misuse of Stolen Codes: Summary

For public clients, only PKCE provides sufficient protection. For confidential clients, always using PKCE or always using Nonce are safe choices. In any case, PKCE can be combined with Nonce. However, a dynamic switch between "PKCE-only" and "Nonce-only" flows must be avoided. 


| Client Type  | Protection by PKCE | by Nonce |
| ------------ | -----------------: | -------: |
| Public       |                  ✔️ |        ❌ |
| Confidential |                  ✔️ |        ✔️ |

## Conclusion 

In terms of protection against CSRF and code misuse, PKCE and Nonce provide similar levels of security. Secondary criteria not analyzed here should be taken into consideration, such as deployment complexity, use cases, robustness against implementation errors, etc. 

To avoid sidestepping or downgrading the PKCE and Nonce checks, authorization servers and clients need to agree on and continuously use one of the methods. For deployments with both OAuth and OIDC flows, PKCE should always be used and Nonce can be used additionally for OIDC flows.

> **Update 1 (2020-05-19):** Clarified reference to PKCE Chosen Challenge attack, now in the subsection "Side Note: Stronger Attacker Model" (thanks for the feedback, [Aaron](https://aaronparecki.com/)) and added description of the PKCE Downgrade attack (thanks to [Nov](https://matake.jp/)).