---
title: Mix-Up, Revisited
layout: publication
type: Analysis
toc: yes
---

A Mix-Up Attack on OAuth is an attack wherein the attacker manages to convince the client to send credentials (authorization code or access token) obtained from an "honest" authorization server to a server under the attacker's control.

In this analysis, I revisit simple mix-up attacks and mix-up attacks with OAuth Metadata and try to find out what happens if we put Pushed Authorization Requests (PAR) into the mix.


<div class="alert alert-info" role="alert">
  <b>Disclaimer:</b> This document discusses theoretical or practical attacks on OAuth or OpenID Connect. Nonetheless, both standards can be used securely as shown by, among others, formal analyses. With the appropriate security mechanisms, both are even suitable for high-risk environments. As with any security protocol, a careful evaluation of potential threats and the required security mechanisms is indispensable when designing a solution based on OAuth/OpenID Connect.
</div>

# Basic Mix-Up Example
Assume that a user wants to start an OAuth flow using the malicious OAuth provider (OP) `attacker.com`. That OP might hide its true identity or, in a large ecosystem, may be an OP that has been compromised. 

Even if all connections are properly secured via TLS, the following attack can be mounted by `attacker.com`:


```plantumlcode

participant Browser
participant client.com
participant attacker.com <<Attacker>>
participant honest.com

Browser -> client.com: Use https://attacker.com
client.com -> Browser: Location: https://attacker.com/auth\n\
        ?redirect_uri=https://client.com/\n\
            &client_id=client_at_attacker\n\
            &code_challenge=sha256(n)\n\
            &state=s\n\
            &...
note right: stored: AS to be used is attacker.com

Browser -> attacker.com: GET https://attacker.com/auth?...
attacker.com -> Browser: Location: https:~//honest.com/auth?redirect_uri=https://client.com/\n\
            &client_id=<font color=red>client_at_honest\n\
            &code_challenge=<font color=red>k</font>\n\
            &state=s\n\
            &...
Browser -> honest.com: GET https:~//honest.com/auth?....
Browser <--> honest.com: user authentication, authorization
honest.com -> Browser: Redirect to https://client.com/?code=c&state=s
Browser -> client.com: GET https://client.com/?code=c&state=s
client.com -> attacker.com: <font color=red>GET /token?code_verifier=n&code=c\n\
    <font color=red>&state=s&redirect_uri=...

note<<warning>> right attacker.com 
    Attack successful
end note

```

In the attack, the attacker's authorization server redirects the user to an honest OP's authorization server. The attacker replaces the `client_id` provided by the client with the one that the client uses for `honest.com` and replaces the `code_challenge` parameter with a different value.

After the uses authorizes access, the attacker is able to capture the code that was used in this flow, as it is sent to the attacker's token endpoint.

The code is bound to the PKCE challenge known to the attacker. If the attacker has chosen k to be a value from another flow with the same client and honest.com as AS, the attacker can inject the code in that flow. (This requires an "online" attack, i.e., the attacker cannot collect codes first and then redeem them.)

(This shows the authorization code grant, but the attack is applicable as well to the Implicit Grant.)


## How to Defend Against Mix-Up?

The guiding principle in defending against Mix-Up Attacks is that the authorization server must make its identity clear to the relying party. Since a successful Mix-Up Attack necessarily involves an honest authorization server, this defence does not rely on the honesty of the attacker.

The following two approaches can be used for this:

 * An `iss` parameter in the authorization response could tell client.com about the identity of the authorization server that was used. 

```plantumlcode

participant Browser
participant client.com
participant attacker.com <<Attacker>>
participant honest.com

Browser -> client.com: Use https://attacker.com
client.com -> Browser: Location: https://attacker.com/auth\n\
        ?redirect_uri=https://client.com/\n\
            &client_id=client_at_attacker\n\
            &code_challenge=sha256(n)\n\
            &state=s\n\
            &...
note right: stored: AS is attacker.com

Browser -> attacker.com: GET https://attacker.com/auth?...
attacker.com -> Browser: Location: https:~//honest.com/auth?redirect_uri=https://client.com/\n\
            &client_id=<font color=red>client_at_honest\n\
            &code_challenge=<font color=red>k</font>\n\
            &state=s\n\
            &...
Browser -> honest.com: GET https:~//honest.com/auth?....
Browser <--> honest.com: user authentication, authorization
honest.com -> Browser: Redirect to https://client.com/?code=c&state=s<font color=blue>&iss=https:~//honest.com
Browser -> client.com: GET https://client.com/?...<font color=blue>&iss=https:~//honest.com
client.com -> client.com: <font color=blue>iss does not match attacker.com
note<<ok>> right
    Attack stopped
end note

```


 * Encoding the authorization server's identity in the redirect_uri can help as well. In this case, the client compares the redirection endpoint where it expects the user to land with the one registered for the expected authorization server.


```plantumlcode


participant Browser
participant client.com
participant attacker.com <<Attacker>>
participant honest.com

Browser -> client.com: Use https://attacker.com
client.com -> Browser: Location: https://attacker.com/auth\n\
        ?redirect_uri=https://client.com/<font color=blue>as/honest.com</font>\n\
            &client_id=client_at_attacker\n\
            &code_challenge=sha256(n)\n\
            &state=s\n\
            &...
note right: stored: AS is attacker.com

Browser -> attacker.com: GET https://attacker.com/auth?...
attacker.com -> Browser: Location: https:~//honest.com/auth?redirect_uri=https://client.com/<font color=blue>as/honest.com</font>\n\
            &client_id=<font color=red>client_at_honest\n\
            &code_challenge=<font color=red>k</font>\n\
            &state=s\n\
            &...
Browser -> honest.com: GET https:~//honest.com/auth?....
Browser <--> honest.com: user authentication, authorization
honest.com -> Browser: Redirect to https://client.com/<font color=blue>as/honest.com</font>?code=c&state=s
Browser -> client.com: GET https://client.com/<font color=blue>as/honest.com</font>?code=c&state=s
client.com -> client.com: <font color=red>issuer encoded in redirect URI\n\
    <font color=red>does not match attacker.com
note<<ok>> right
    Attack stopped
end note

```

**Why does that work?**

If OAuth Metadata or OpenID Connect Configuration are *not* used, one can expect that the client lives in an ecosystem where there is a clear connection between the selected OAuth Provider and the authorization server through some out-of-band mechanism. For example, a client could have multiple OAuth providers configured manually using a simple table as follows:

| Provider       | Authorization Endpoint       | Token Endpoint               | Resource Server            |
| -------------- | ---------------------------- | ---------------------------- | -------------------------- |
| Awesome OAuth  | https://awesome.auth/authz   | https://awesome.auth/token   | https://awesome.auth/api   |
| Other Provider | https://some.other.idp/login | https://some.other.idp/te    | https://some.other.idp/    |
| Malicious OP   | https://malicious.auth/auth  | https://malicious.auth/token | https://malicious.auth/res |
| ...            | ...                          | ...                          | ...                        |

*(Assumption here: There is an effective mechanism to stop the malicious OP from registering one of the benign authorization servers at the client.)*

This means that the client knows whether a particular authorization server belongs to a particular OAuth Provider (there is often a 1:1 mapping). The provider is identified using some internal mechanism. Therefore, if the client starts a flow using a particular provider, the authorization endpoint's identity is enough to check whether that authorization server belongs to the expected provider.

**Is there a need to tie the code and the iss parameter together in the authorization response?**

This is not needed if the authorization response is sent from the authorization server via the user's browser to the client and that there is no opportunity for the attacker to modify the response.

If the attacker can modify the response, [JARM](https://openid.net/specs/openid-financial-api-jarm-ID1.html#jwt-based-response-mode) could prevent tampering. The catch is that with metadata (see below), the attacker can control the keys used for signature verification. Therefore, there is no value in adding JARM.

However, if the attacker can modify the response, he can also read the authorization code. For Mix-Up attacks targeting the authorization code, we can therefore assume that the attacker cannot modify the response, because otherwise, there would be no need for the attacker to mount a mix-up attack. For Mix-Up attacks targeting the access token, this is not so clear.





# With OAuth Metadata

## Simple Mix-Up

Assume that an attacker sets up the following OAuth Metadata:

```json
{
    "issuer": "https://attacker.com",
    "authorization_endpoint": "https://honest.com/authorize",
    "token_endpoint": "https://attacker.com/token"
}
```

(This is the setup presented in https://arxiv.org/pdf/1508.04324.pdf)

In this case, the attack as above works as well. The client will send the user to the honest authorization endpoint, but then send the code to the manipulated token endpoint. The attacker can redeem the code for an access token at the token endpoint if the client is a public client.

## Mix-Up with Confidential Clients and PKCE

That is nice, but if the client is a confidential client, the attacker cannot redeem the code for an authorization token. One way around this limitation is a [Code Injection Attack](https://tools.ietf.org/id/draft-ietf-oauth-security-topics-14.html#rfc.section.4.5). This attack is normally [protected against with PKCE](https://tools.ietf.org/id/draft-ietf-oauth-security-topics-14.html#rfc.section.4.5.3). 

Here, however, there is a way for the attacker to change the PKCE Challenge that is used for the authorization flow. To conduct this attack, the attacker uses his own endpoint in the Metadata:

```json
{
    "issuer": "https://attacker.com",
    "authorization_endpoint": "https://attacker.com/authorize",
    "token_endpoint": "https://attacker.com/token"
}
``` 
When a user arrives at that endpoint, attacker starts an OAuth session with the *same* confidential client. From his session, the attacker extracts the PKCE Challenge and then redirects the user that arrived at the attacker's authorization endpoint  just as in the first example but replaces the PKCE Challenge by the one from his own session with the client.

The attacker can then inject the code acquired from the user's session into his own session with the client. This attack is called a [PKCE Chosen Challenge Attack](https://datatracker.ietf.org/meeting/105/materials/slides-105-oauth-sessa-oauth-security-topics-00)).

## Stealing Access Tokens

It is possible to steal the access token as well using the following configuration:

```json
{
    "issuer": "https://attacker.com",
    "authorization_endpoint": "https://honest.com/authorize",  
    "token_endpoint": "https://honest.com/token",
    "userinfo_endpoint": "https://attacker.com/userinfo"
}
```
(or use attacker.com for the authorization endpoint and then redirect)

## Defending Against Mix-Up with Metadata

The difference to the scenario without metadata is that the client now has an issuer URI and resolves the authorization server using the issuer URI. An attacker can, as shown, assign the honest authorization server to his own issuer. It is therefore necessary that the authorization server signals for which issuers it may be used, as that implies the issuer configurations and thereby the token and userinfo endpoints that are being used.

Importantly, it is not enough that the autorization server identifies *itself* (i.e., using its URL or a redirection URI that is unique to itself), but it needs to identify the *issuer*.

> **Recommendation:** The security BCP needs to make clear that *per-AS* redirect URIs are only sufficient if OAuth Metadata is not used to resolve multiple issuers. Otherwise, *per-Issuer* redirect URIs or the `iss` parameter MUST be used.

## Mixup With Pushed Authorization Requests

What if put PAR into the mix? It complicates things.

```json
{
    "issuer": "https://attacker.com",
    "pushed_authorization_request_endpoint": "https://attacker.com/par",
    "authorization_endpoint": "https://attacker.com/authorize",
    "token_endpoint": "https://attacker.com/token",
    "userinfo_endpoint": "https://attacker.com/userinfo"
}
``` 

We now have four endpoints that can be either set to the honest server's endpoints or the attacker's own endpoints. This makes 16 possible combinations.

The following table lists the 16 possible combinations (`H`=honest server's endpoint, `A`=attacker's endpoint). The potential attacks that arise are referenced in the table, separated for public and confidential clients, and listed below.

| PAR   | Authz | Tok   | UInfo | Attacks for public clients         | for confidential clients              |
| ----- | ----- | ----- | ----- | ---------------------------------- | ------------------------------------- |
| `H`   | `H`   | `H`   | `H`   | no mix-up attack                   | *                                     |
| `H`   | `H`   | `H`   | `Att` | _token to UInfo_                   | *                                     |
| `H`   | `H`   | `Att` | `H`   | _code to Tok-PC_ _token injection_ | * _code to Tok-NCI_ _token injection_ |
| `H`   | `H`   | `Att` | `Att` | _code to Tok-PC_                   | * _code to Tok-NCI_                   |
| `H`   | `Att` | `H`   | `H`   | no mix-up attack                   | * same                                |
| `H`   | `Att` | `H`   | `Att` | _token to UInfo_                   | * same                                |
| `H`   | `Att` | `Att` | `H`   | _code to Tok-PC_ _token injection_ | * _code to Tok2_ _token injection_    |
| `H`   | `Att` | `Att` | `Att` | _code to Tok-PC_                   | * _code to Tok2_                      |
| `Att` | `H`   | `H`   | `H`   | no mix-up attack                   | no mix-up attack                      |
| `Att` | `H`   | `H`   | `Att` | _token to UInfo_                   | same                                  |
| `Att` | `H`   | `Att` | `H`   | _code to Tok-PC_ _token injection_ | _code to Tok_ _token injection_       |
| `Att` | `H`   | `Att` | `Att` | _code to Tok-PC_                   | _code to Tok_                         |
| `Att` | `Att` | `H`   | `H`   | no mix-up attack                   | same                                  |
| `Att` | `Att` | `H`   | `Att` | _token to UInfo_                   | same                                  |
| `Att` | `Att` | `Att` | `H`   | _code to Tok-PC_                   | _code to Tok_                         |
| `Att` | `Att` | `Att` | `Att` | _code to Tok-PC_                   | _code to Tok_                         |


_*_ no mix-up depending on deployment - client credentials might not match the ones that need to be presented

Legend:

 * _token to UInfo_: Token is sent to attacker's endpoint as shown above.
 * _code to Tok-PC_: Code is sent to attacker's endpoint as shown above. Code is readily usable by the attacker as it is not issued for a confidential client.
 * _code to Tok-NCI_: Code is sent to attacker's endpoint as shown above. Code injection is prevented as the    attacker cannot exchange the PKCE Challenge.
 * _code to Tok_: Code is sent to attacker's endpoint as shown above. Attacker can inject the stolen code using code injection with PKCE Chosen Challenge as shown above.
 * _code to Tok2_: Code is sent to attacker's endpoint as shown above. If the authorization server accepts non-PAR requests, the attacker can inject the stolen code using code injection with PKCE Chosen Challenge as shown above.
 * _token injection_: The attacker can send an access token to the client that is then used by the client for the resource server. This can defeat sender-constrained tokens, [as described in this paper](https://arxiv.org/abs/1901.11520).
 * _authz-mitm_: The attacker can change all contents of the authorization request.
 
Other attacks:

 * If the authorization endpoint points to the attacker, the attacker can break session integrity, i.e., logging in the user under a different identity.
 * If the UserInfo endpoint points to the attacker, the attacker can send spoofed user information to the client.
 * PAR promises integrity for the authorization request. This can be undermined in certain conditions, see below.


## Integrity of the Authorization Request with PAR

PAR with client authentication promises integrity for the authorization request by sending all the data of the authorization request via the backend.

 1. If the PAR endpoint does not point to an attacker's endpoint, PAR protects against attack variants where the attacker exchanges the PKCE Challenge. The attacker can, however, still forward the whole authorization request with the `request_uri` to the victim, and if the victim authorizes the request, the attacker can  grab the code. 
 1. If the PAR endpoint points to the attacker, the attacker has the option of taking the parameters from the PAR request, changing them into URL parameters (and maybe manipulating them), and creating an authorization request URL from them. If the authorization endpoint also points to an endpoint of the attacker, the attacker can just forward the user to the newly created authorization request URL at the honest server. If the authorization endpoint is not under the control of the attacker, the attacker can try to use HTTP request parameter pollution to influence the authorization request the client sends to the authorization server.


> **Recommendation:** PAR-enabled authorization servers can **protect the integrity better** and **protect against Mix-Up Attacks better** if they ONLY accept PAR requests.

# Mitigations

 * Adding an `iss` parameter to the PAR request will probably not solve the problem; the AS can still be mixed-up.
 * The `iss` parameter in the authorization response (and a check performed by the client) solves all mix-up variants listed above.
 * A per-issuer-redirect uri can be confused with a per-AS-redirect URI, the latter would not solve mix-up.

> **Recommendation:** Emphasize importance of `iss` parameter (or `issuer`) in authorization response. Maybe introduce this parameter in the security BCP or another document?

 * As described above, there is probably no value in adding JARM to protect the issuer parameter in the authorization response. 
 * Attacks where the token endpoint is at the honest AS and the userinfo endpoint or another resource is at the attacker can be mitigated by using sender-constrained access tokens. An attacker would not be able to replay the token at another endpoint.

> **Note:** Sender-constrained access tokens rock.

> **Recommendation:** Sender-constraining the authorization code (PAR + PAR-DPoP?) might be worth looking into.
