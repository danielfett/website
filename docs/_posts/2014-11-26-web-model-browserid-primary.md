---
layout: publication
title: Analyzing the BrowserID SSO System with Primary Identity Providers Using an Expressive Model of the Web
type: Paper
note: ESORICS 2015
links:
    - type: download
      name: paper
      href: https://sec.uni-stuttgart.de/_media/publications/FettKuestersSchmitz-ESORICS-2015.pdf
    - type: external-link
      name: technical report on arxiv.org
      href: https://arxiv.org/abs/1411.7210
---
**Abstract:**
BrowserID is a complex, real-world Single Sign-On (SSO) System for web applications recently developed by Mozilla. It employs new HTML5 features (such as web messaging and web storage) and cryptographic assertions to provide decentralized login, with the intent to respect users' privacy. It can operate in a primary and a secondary identity provider mode. While in the primary mode BrowserID runs with arbitrary identity providers (IdPs), in the secondary mode there is one IdP only, namely Mozilla's default IdP.

We recently proposed an expressive general model for the web infrastructure and, based on this web model, analyzed the security of the secondary IdP mode of BrowserID. The analysis revealed several severe vulnerabilities.

In this paper, we complement our prior work by analyzing the even more complex primary IdP mode of BrowserID. We do not only study authentication properties as before, but also privacy properties. During our analysis we discovered new and practical attacks that do not apply to the secondary mode: an identity injection attack, which violates a central authentication property of SSO systems, and attacks that break an important privacy promise of BrowserID and which do not seem to be fixable without a major redesign of the system. Some of our attacks on privacy make use of a browser side channel that has not gained a lot of attention so far.

For the authentication bug, we propose a fix and formally prove in a slight extension of our general web model that the fixed system satisfies all the requirements we consider. This constitutes the most complex formal analysis of a web application based on an expressive model of the web infrastructure so far.

As another contribution, we identify and prove important security properties of generic web features in the extended web model to facilitate future analysis efforts of web standards and web applications. 
