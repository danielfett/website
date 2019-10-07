---
title: Cross-Browser Payment Initiation Attack
type: Technical Report
layout: publication
links:
    - name: Document
      type: external-link
      href: https://bitbucket.org/openid/fapi/src/master/TR-Cross_browser_payment_initiation_attack.md
---

**Abstract**: This document describes a possible attack on payment
flows utilizing a browser-based redirect flow to authenticate the user
and gather her consent to initiate the payment. It is based on a
security threat analysis of several PSD2 API standards conducted by
OpenID Foundation's [Financial-grade API (FAPI) Working Group](https://openid.net/wg/fapi/).

In the cross-browser payment initiation attack, Bob wants to make
Alice pay for the goods he ordered at the web site of some merchant.

The causes for this vulnerability are

  * the lack of binding between the browser which initiated payment
    transaction (Bob's browser) and the browser where the transaction
    was authorized (Alice's browser) and
  * the fact the transaction is automatically initiated when the user
    authorized it before such a lack of binding could be detected.
  
This allows the attacker to prepare a transaction and remotely trick
the victim into executing it. Since the attacker has all the details,
it can benefit from the successful execution. That's why this kind of
attack is typically referred to as "session fixation".

For more details, see the [technical report on the Cross-Browser Payment Initiation Attack by the OpenID Foundation](https://bitbucket.org/openid/fapi/src/master/TR-Cross_browser_payment_initiation_attack.md).
