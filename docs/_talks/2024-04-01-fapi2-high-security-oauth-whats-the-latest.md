---
layout: publication
title: "High-Security and Interoperable OAuth 2: What's the latest? | FAPI 2.0"
type: Talk 
venue: OAuth Security Workshop 2024
links:
    - type: play
      name: watch (youtube)
      href: https://www.youtube.com/watch?v=DteFhWHE_tk
---

**Abstract:** OAuth is a widely used authorization framework that enables third-party applications to access resources on behalf of a user. However, it has historically been difficult to meet very high security and interoperability requirements when using OAuth. Daniel and Joseph have spent much of the last six years working to improve the state of the art and will present the latest developments in the field.

There are challenges when trying to achieve high security and interoperability with OAuth 2: There are many potential threats, some not part of the original OAuth threat model. For seamless authorizations, optionality must be minimized in OAuth itself and also in any extensions used.

Seven years ago, the IETF OAuth working group began work on the Security Best Current Practice document and more recently on OAuth 2.1. Meanwhile, the OpenID Foundation has created FAPI1 and FAPI2 security profiles.

We will help you understand the focus of each document and when to use which. We show how to achieve on-the-wire interoperability and security using techniques like asymmetric client authentication and sender-constraining via DPoP and MTLS, discussing the benefits and potential disadvantages of each. We highlight the benefits for implementers and the role of conformance testing tools.
