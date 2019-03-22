---
layout: publication
title: An Expressive Formal Model of the Web Infrastructure
type: PhD Thesis
links: 
    - type: download
      href: https://elib.uni-stuttgart.de/bitstream/11682/10214/1/%27An%20Expressive%20Formal%20Model%20of%20the%20Web%20Infrastructure.pdf
      name: download thesis
    - type: download
      name: download slides
      href: /download/thesis-defense.pdf

---

**Abstract:** The World Wide Web is arguably the most important medium of our time. Billions of users
rely on the security of the web each day for tasks such as banking, shopping, and business and
private communication.

The web is a heterogeneous infrastructure developing at a high pace. The question of whether
the web infrastructure or certain web applications are secure is not easy to answer. Standards
and applications today are reviewed by experts before they are deployed, but all too often even
serious security vulnerabilities are simply overlooked.

In this thesis, we propose a formal model for the web infrastructure which enables a rigorous
formal analysis of security and privacy in the web. Our model is the most comprehensive
and expressive model of the web infrastructure to date. It facilitates accurate security and
privacy analyses of current web standards and applications, and can serve as a reference for
web security researchers, developers of new technologies and standards, and for teaching web
security concepts.

As a case study we analyze the security of two important standards for federated authorization
and authentication, OAuth 2.0 and OpenID Connect. Standardized by the IETF and OpenID
Foundation, respectively, they are among the most widely deployed single sign-on systems in
the web.

For our analysis, we develop detailed formal models for both systems based on our model
of the web infrastructure. These models then allow us to precisely define the security goals of
authentication, authorization and session integrity.

While proving security with respect to these goals, we found a total of five new attacks on
the two single sign-on systems, breaking all of the security goals. In particular OAuth 2.0 had
been analyzed many times before; the fact that we were able to find new attacks in OAuth 2.0
demonstrates the potential of rigorous analyses in our web infrastructure model.

We develop fixes against the underlying vulnerabilities and are then able to prove the security
of OAuth 2.0 and OpenID Connect. Since our results are based on a comprehensive model,
our proofs can exclude large classes of attacks against OAuth and OpenID Connect, including
yet unknown attack vectors. Our attacks and fixes led to the development of new security
recommendations by the standardization organizations.
