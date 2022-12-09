---
title: Selective Disclosure for JWTs (SD-JWT)
type: RFC
tag: Work in Progress
layout: publication
links:
    - name: IETF Draft
      type: external-link
      href: https://tools.ietf.org/html/draft-fett-oauth-selective-disclosure-jwt
    - name: Source Repository
      type: external-link
      href: https://github.com/oauth-wg/oauth-selective-disclosure-jwt
---

**Abstract**: 
This document specifies conventions for creating JSON Web Token (JWT) documents that support selective disclosure of JWT claims.

**Introduction**: 
The JSON-based representation of claims in a signed JSON Web Token (JWT) is secured against modification using JSON Web Signature (JWS) digital signatures. A consumer of a signed JWT that has checked the signature can safely assume that the contents of the token have not been modified. However, anyone receiving an unencrypted JWT can read all of the claims and likewise, anyone with the decryption key receiving an encrypted JWT can also read all of the claims.

One of the common use cases of a signed JWT is representing a user's identity. As long as the signed JWT is one-time use, it typically only contains those claims the user has consented to disclose to a specific Verifier. However, there is an increasing number of use cases where a signed JWT is created once and then used a number of times by the user (the "Holder" of the JWT). In such cases, the signed JWT needs to contain the superset of all claims the user of the signed JWT might want to disclose to Verifiers at some point. The ability to selectively disclose a subset of these claims depending on the Verifier becomes crucial to ensure minimum disclosure and prevent Verifiers from obtaining claims irrelevant for the transaction at hand.

One example of such a multi-use JWT is a verifiable credential, a tamper-evident credential with a cryptographically verifiable authorship that contains claims about a subject. SD-JWTs defined in this document enable such selective disclosure of claims.

In an SD-JWT, claims can be hidden, but cryptographically protected against undetected modification. When issuing the SD-JWT to the Holder, the Issuer also sends the cleartext counterparts of all hidden claims, the so-called Disclosures, separate from the SD-JWT itself.

The Holder decides which claims to disclose to a Verifier and forwards the respective Disclosures together with the SD-JWT to the Verifier. The Verifier has to verify that all disclosed claim values were part of the original, Issuer-signed SD-JWT. The Verifier will not, however, learn any claim values not disclosed in the Disclosures.

While JWTs for claims describing natural persons are a common use case, the mechanisms defined in this document can be used for many other use cases as well.

This document also describes an optional mechanism for Holder Binding, or the concept of binding an SD-JWT to key material controlled by the Holder. The strength of the Holder Binding is conditional upon the trust in the protection of the private key of the key pair an SD-JWT is bound to.

This specification aims to be easy to implement and to leverage established and widely used data formats and cryptographic algorithms wherever possible.

