---
layout: publication
title: How (Not) to Use OAuth
type: Talk
venue: Froscon 2019
links:
    - type: download
      name: download
      href: /download/froscon-2019-how-not-to-use-oauth.pdf
    - type: play
      name: watch (media.ccc.de)
      href: https://media.ccc.de/v/froscon2019-2334-how_not_to_use_oauth
    - type: play
      name: watch (youtube)
      href: https://www.youtube.com/watch?v=sdpWVizuS70
redirect_from:
  - /publications/2019-08-10-how-not-to-use-oauth/
---

<i>I am coauthoring the new security recommendations RFC for OAuth 2.0
in the IETF OAuth Working Group. In this talk, I will walk you through
the MUSTs, MUST NOTs, and SHOULDs of the new recommendations.</i>

OAuth is the most important framework for federated authorization on
the web. It also serves as the foundation for federated authentication
using OpenID Connect. While RFC6749 and RFC6819 give advice on
securing OAuth deployments, many subtle and not-so-subtle ways to
shoot yourself in the foot remain. One reason for this situation is
that OAuth today is used in much more dynamic setups than originally
anticipated. Another challenge is that OAuth today is used in
high-stakes environments like financial APIs and strong identity
proving.

To address these challenges, the IETF OAuth working group is working
towards a
new
[Security Best Current Practice (BCP)](/publications/2018-12-28-oauth-bcp/) RFC
that aims to weed out insecure implementation patterns based on
lessons learned in practice and
from
[formal security analyses](/publications/2018-10-19-an-expressive-formal-web-model) of
OAuth and OpenID Connect. The BCP gives concrete advice to defend
against attacks discovered recently (like the AS mix-up attack) and
discourages the use of less-secure grant types such as the Implicit
Grant.

This talk will outline the challenges faced by OAuth in dynamic and
high-stakes environments and go into the details of the MUSTs, MUST
NOTs, and SHOULDs in the new Security BCP.


Note: Some animation steps were lost during the PDF export.
