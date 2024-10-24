---
title: Selective Disclosure for JWTs (SD-JWT)
type: IETF RFC
tag: Work in Progress
layout: publication
links:
    - name: IETF Draft
      type: external-link
      href: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-selective-disclosure-jwt
    - name: Source Repository
      type: external-link
      href: https://github.com/oauth-wg/oauth-selective-disclosure-jwt
---

**Abstract**: 
This specification defines a mechanism for the selective disclosure of individual elements of a JSON-encoded data structure used as the payload of a JSON Web Signature (JWS). The primary use case is the selective disclosure of JSON Web Token (JWT) claims.

**Introduction**: 
JSON-encoded data structures for exchange between systems are often secured against modification using JSON Web Signatures (JWS). A popular application of JWS is JSON Web Token (JWT), a format that is often used to represent a user's identity. An ID Token as defined in OpenID Connect, for example, is a JWT containing the user's claims created by the server for consumption by a relying party. In cases where the JWT is sent immediately from the server to the relying party, as in OpenID Connect, the server can select at the time of issuance which user claims to include in the JWT, minimizing the information shared with the relying party who validates the JWT.

A new model is emerging that fully decouples the issuance of a JWT from its presentation. In this model, a JWT containing many claims is issued to an intermediate party, who holds the JWT (the Holder). The Holder can then present the JWT to different verifying parties (Verifiers), that each may only require a subset of the claims in the JWT. For example, the JWT may contain claims representing both an address and a birthdate. The Holder may elect to disclose only the address to one Verifier, and only the birthdate to a different Verifier.

Privacy principles of minimal disclosure in conjunction with this model demand a mechanism enabling selective disclosure of data elements while ensuring that Verifiers can still check the authenticity of the data provided. This specification defines such a mechanism for JSON-encoded payloads of JSON Web Signatures, with a primary use case being JWTs.

SD-JWT is based on an aproach called "salted hashes": For any data element that should be selectively disclosable, the Issuer of the SD-JWT does not include the cleartext of the data in the JSON-encoded payload of the JWS structure; instead, a hash digest of the data takes its place. For presentation to a Verifier, the Holder sends the signed payload along with the cleartext of those claims it wants to disclose. The Verifier can then compute the digest of the cleartext data and confirm it is included in the signed payload. To ensure that Verifiers cannot guess cleartext values of non-disclosed data elements, an additional salt value is used when creating the digest and sent along with the cleartext when disclosing it.

To prevent attacks in which an SD-JWT is presented to a Verifier without the Holder's consent, this specification additionally defines a mechanism for binding the SD-JWT to a key under the control of the Holder (Key Binding). When Key Binding is enforced, a Holder has to prove possession of a private key belonging to a public key contained in the SD-JWT itself. It usually does so by signing over a data structure containing transaction-specific data, herein defined as the Key Binding JWT. An SD-JWT with a Key Binding JWT is called SD-JWT+KB in this specification.