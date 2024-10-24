---
title: "Cross-Device Flows: Security Best Current Practice"
type: IETF RFC
tag: Work in Progress
layout: publication
links:
    - name: IETF
      type: external-link
      href: https://tools.ietf.org/html/draft-ietf-oauth-cross-device-security
---

**Abstract**:
This document describes threats against cross-device flows along with
practical mitigations, protocol selection guidance, and a summary of
formal analysis results identified as relevant to the security of
cross-device flows.  It serves as a security guide to system
designers, architects, product managers, security specialists, fraud
analysts and engineers implementing cross-device flows.

**Introduction**:

Protocol flows that span multiple end-user devices are in widespread
use today.  These flows are often referred to as cross-device flows.
A common example is a user that uses their mobile phone to scan a QR
code from their smart TV, giving an app on the TV access to their
video streaming service.  Besides QR codes, other mechanisms are
often used such as PIN codes that the user has to enter on one of the
devices, or push notifications to a mobile app that the user has to
approve.

In all cases, it is up to the user to decide whether to grant
authorization or not.  However, the QR code or PIN are transferred
via an unauthorized channel, leaving it up to the user to decide in
which context an authorization is requested.  This may be exploited
by attackers to gain unauthorized access to a user's resources.

To accommodate the various nuances of cross-device flows, this
document distinguished between cases where the cross-device flow is
used to authorize access to a resource (cross-device authorization
flows) and cases where the cross-device flow is used to transfer an
existing session (cross-device session transfer flows).