---
layout: publication
title: 'The Web SSO Standard OpenID Connect: In-Depth Formal Security Analysis and Security Guidelines'
type: Paper
note: CSF 2017
links:
    - type: download
      name: paper
      href: https://sec.uni-stuttgart.de/_media/publications/FettKuestersSchmitz-CSF-2017.pdf
    - type: external-link
      name: technical report on arxiv.org
      href: https://arxiv.org/abs/1704.08539
---

**Abstract:** Web-based single sign-on (SSO) services such as Google Sign-In and Log In with Paypal are based on the OpenID Connect protocol. This protocol enables so-called relying parties to delegate user authentication to so-called identity providers. OpenID Connect is one of the newest and most widely deployed single sign-on protocols on the web. Despite its importance, it has not received much attention from security researchers so far, and in particular, has not undergone any rigorous security analysis.

In this paper, we carry out the first in-depth security analysis of OpenID Connect. To this end, we use a comprehensive generic model of the web to develop a detailed formal model of OpenID Connect. Based on this model, we then precisely formalize and prove central security properties for OpenID Connect, including authentication, authorization, and session integrity properties.

In our modeling of OpenID Connect, we employ security measures in order to avoid attacks on OpenID Connect that have been discovered previously and new attack variants that we document for the first time in this paper. Based on these security measures, we propose security guidelines for implementors of OpenID Connect. Our formal analysis demonstrates that these guidelines are in fact effective and sufficient. 
