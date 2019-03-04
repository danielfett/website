---
title: New OAuth Security Recommendations
type: Overview
layout: publication
---

The new [OAuth Security BCP](https://tools.ietf.org/html/draft-ietf-oauth-security-topics) contains a number of new and updated recommendations on the usage of OAuth 2.0. I recommend reading the whole document to understand the threats and attacks that lead to these guidelines. As a quick reference, the following table shows an overview of the most important new recommendations:

| New Recommendation                                                                                       | Reason                                                                        |
|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| AS MUST use exact matching of client redirect URIs against pre-registered URIs                           | prevention of leakage of authorization codes and access tokens; detect mix-up |
| Clients SHOULD avoid open redirectors                                                                    | prevent open redirector attacks                                               |
| Clients MUST use one-time use state nonce bound to user agent                                            | prevent CSRF                                                                  |
| Clients MUST memorize combination of AS and user agent and ensure subsequent messages match this binding | prevent mix-up attacks                                                        |
| Auth Code Grant: MUST use PKCE (all kinds of clients)                                                    | detect and prevent auth code replay                                           |
| Auth Code Grant: Use PKCE or client credentials to authenticate client in token request                  | detect and prevent auth code replay                                           |
| Prevent leakage of code through referrer headers, request logs, and browser history                      | prevent auth code replay                                                      |
| Implicit Grant: SHOULD NOT be used unless tokens can be sender-constrained                               | prevent leakage and replay of access tokens                                   |
| AS SHOULD use TLS-based methods for sender-constraining access tokens                                    | prevent token replay                                                          |
| access tokens SHOULD be associated with a minimum of privileges                                          | prevent misuse of privileges                                                  |
| access tokens SHOULD be restricted to certain RS                                                         | prevent misuse of access tokens                                               |
| AS MUST NOT use HTTP 307 redirect (if user credentials could be redirected)                              | prevent leakage of credentials                                                |
| AS MUST use sender-constrained refresh tokens or refresh token rotation                                  | detect and prevent refresh token replay                                       |


