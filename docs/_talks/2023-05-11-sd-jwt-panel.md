---
layout: publication
title: "Current Work and Future Trends in Selective Disclosure"
type: Panelist
venue: EIC 2023
links:
    - type: external-link
      name: more information (kuppingercole.com)
      href: https://www.kuppingercole.com/sessions/5319/1
    - type: download
      name: slides (extract - only my material on SD-JWT)
      href: /download/sd-jwt-panel-eic-2023.pdf
---

**Panel with Kristina Yasuda, Mike Jones, Tobias Looker, David Waite**

There’s a lot of foundational work happening in the space of Selective Disclosure (SD) right now. Selective Disclosure enables you to have a token with many claims (say, an ISO Mobile Drivers’ License (mDL)), and only release the claims necessary to the interaction – for instance, your birthdate but not your home address.  Selective Disclosure enables Minimal Disclosure.  This is sometimes realized using Zero Knowledge Proofs (ZKPs) but that’s not always necessary.

In decentralized identity ecosystems, users hold their own credentials to share them with others when needed. One key requirement for these credentials is selective disclosure: instead of sharing the entire credential, users should be able to share only the minimal amount of information necessary for a given use case. This is where SD-JWT comes in.

SD-JWT (Selective Disclosure JWT) is a new format for enabling selective disclosure in JWTs. It is based on the JOSE family of standards for signing and encryption, making it easy to understand and implement.

Developed by the IETF OAuth Working Group, SD-JWT is not limited to verifiable credentials, but can be used universally to provide selective disclosure for any JWT.

Due to its simplicity, SD-JWT has quickly gained traction, with several implementations already available and ongoing adoption as an important building block in both commercial and public projects. In this talk, we will introduce the concepts behind SD-JWT and provide a detailed overview of its capabilities and benefits. We will also discuss the current state of SD-JWT adoption and future directions for its development.

*Description from kuppingercole.com/Mike Jones.*
