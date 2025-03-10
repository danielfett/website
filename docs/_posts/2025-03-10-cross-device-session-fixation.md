---
title: "Cross-Device Session Fixation and how the DC API solves it"
layout: publication
type: Analysis
toc: yes
---

In the context of digitial credential ecosystems and specifically the EU Digitial Identity (EUDI) Wallet, there have been discussions recently whether to adopt the W3C Digital Credentials API (DC API) or not. While the API promises various improvements (e.g., wallet selection) and brings drawbacks in other areas, it is important to understand a specific type of security issue that can **only** be solved by an integration with the browser and operating system as provided by the DC API. In this post, I'll describe the problem and discuss potential mitigations.
<!--more-->

## The Problem: Session Fixation

It is clear that a user of an EUDI Wallet must always **know the identity of the Verifier** they are interacting with. This is often referred to as "RP/Verifier Authentication" or similar. However, as shown in the following, this is not sufficient for a secure interaction.

For many interactions, it is additionally crucial that the user knows **in what (session) context** they are presenting a credential. 

These are two **separate** properties, as illustrated in the following attack:

1. An attacker has set up a phishing website `e-gov.example`, mimicking the real `egov.example` website, an online e-government portal providing various services. 
2. As soon as a user comes to the attacker's website `e-gov.example` and tries to log in, the attacker does the following:
    1. The attacker opens the "real" website `egov.example` on the attacker's own device.
    1. The attacker clicks on the "login with EUDI Wallet" button and is provided with either a link that takes them directly into a Wallet app on the same device or a QR code that they can scan with a second device.
    2. Instead of following the link/QR code, the attacker extracts the link or QR code and replays it on the phishing website `e-gov.example`.
3. The user will now follow the link or scan the QR code and their Wallet will open.
4. The user will be prompted by their Wallet app to present, for example, a PID credential for identification. The wallet will show them that the request originates from and is signed by the "Official E-Government Portal" and is for the purpose of "Log in to the portal". This aligns with the user's expectations, so they click "proceed".
5. The Wallet app will send the credential presentation to the real website `egov.example` using properly authenticated and encrypted channels.
6. Since the credential request was created on the attacker's device (Step 2.2 above), the presentation will be bound to that same session. **The attacker's session with `egov.example` will therefore be logged in under the user's identity.**

There are various names for this kind of attacks, including *Session Fixation*, which describes the problem quite well: While the request is authentic, the attacker forwarded it to the victim, who doesn't know in what session context the login is happening.

What exactly is the problem? In Steps 2.1 and 2.2, the attacker started a web session with the real website `egov.example`. Within this session, the `egov.example` Verifier created the presentation request, which contains a unique value (usually a nonce) bound to the web session in the browser. When the presentation arrives back at the Verifier in Step 6, the Verifier sees the same nonce (it is usually signed over by the Wallet in the presentation). Unless any of the mitigations below are applied, the Verifier will look up the nonce, find that it was tied to the web session started in Steps 2.1/2.2, and will assume that the user from this session presented the credential.

**Q: Isn't this a Man-in-the-Middle (MitM) attack?** 
A: Yes and no: MitM often implies breaking into (encrypted or unencrypted) communication channels. That does not really happen in this attack. The original website provides the attacker with a piece of information (QR code or link) in a completely benign and correct manner. The attacker forwards this information to the victim over a properly encrypted and authenticated channel.

**Q: So it's a replay attack?**
A: Yes, it is a kind of replay attack, but that name doesn't capture the gist of the attack.

**Q: Is this a new attack? What technologies are affected?**
A: This is a very fundamental problem that comes from the nature of redirect-based flows and cross-device flows. As such, it has been known for a very long time. Without mitigations (as described below), it would affect **all redirect-based protocols** and **cross-device protocols**, including but not limited to: SAML, OAuth, OpenID Connect, OpenID4VP, ISO/IEC 23220-4 RestAPI protocol, and others.

## Mitigations

In principle, there are always two points in the protocols where this attack can be mitigated:

1. When the request is sent from the Verifier to the Wallet.
2. When the presentation is sent back.

If, at either of these points, it is ensured that the request was not forwarded by an attacker, the attack is prevented.

The actual, practical mitigations are different for same-device flows (where the website is opened on the same device as the Wallet app) and for cross-device flows. While the one is a solved problem, the other didn't have a good solution until recent.

### Same-Device Flows

As long as the interaction remains on the same device, the usual mitigation leverages point (2.) above: Ensuring that the presentation can only be completed on the same device on which it was started.

This is usually done by enforcing that the Wallet app needs to jump back into the same browser to complete the presentation. A piece of information (either the whole presentation or a reference to it) is provided in this jump back into the browser. The Verifier can then check that the web session in which the request was started matches the nonce in the presentation.

In the attack above and with this mitigation, if an attacker would forward the link to a victim, the Wallet would jump back into the victim's browser (as the attacker cannot intercept the jump back). That browser would not know the web session, and the Verifier would reject the presentation.

**Redirect-based same-device protocols usually implement this defense or variants of it and are therefore secure against session fixation when implemented correctly.** For example, details for OpenID4VP can be found [here](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#name-session-fixation).

It must be noted that this kind of defense, while robust, can easily be implemented incorrectly, so the defense that the DC API provides (described below) would still provide some advantage—but that is not the main point here.


### Cross-Device Flows

In cross-device flows, the picture is a different one: A jump back into the same browser is often not practical (the victim would need to scan a second QR code with the Verifier device) or could be intercepted by the attacker. It is therefore hard to ensure that *the same user* started the interaction on one device and finished it on another device.

In the following, I'll briefly list some mitigations that are often proposed, but don't solve the problem:

- **One-time use QR codes:** In the attack above, the QR code is already one-time use.
- **Time-based changing QR codes:** The attacker can easily replay changing QR codes to the victim, it just requires a little more effort on the attacker's side.
- **Short-lived QR codes:** The attacker's step would be performed completely automatically within a second or so. Short-lived QR codes would not help.
- **Signed QR codes/links:** The attack already assumes that the QR code is signed and its authenticity can be verified by the Wallet using some trust framework. **The problem remains that the QR code itself is authentic and not modified by the attacker.** However, there is no technology available to ensure that QR codes cannot be replayed or that a QR code signed by Party A cannot be displayed on the website of Party B.
- **Website Authentication:** Using some form of website authentication, e.g., EV certificates or QWACs, does not help. Even if `egov.example` uses, e.g., a QWAC, and if the EUDI Wallet ecosystem were to enforce the use of QWACs on every single communication link within the ecosystem, an attacker at `e-gov.example` could still replay the QR code. Users will have a hard time noticing the *absence* of a QWAC on `e-gov.example` before they scan the QR code. Even then, the Wallet will tell them that the presentation goes to "Official E-Government Portal" (checked by QWAC, maybe?), so they might approve the request.
- **Have the user compare domains:** Vigilant users might notice that `egov.example` displayed in their Wallet is not `e-gov.example` displayed in their browser. However, expecting users to always check for these kinds of mismatches has never worked reliable in practice and cannot be expected to work in a widely deployed ecosystem. Additionally, the caveat from the paragraph above applies: If the presentation goes to the right receiver, why not just accept the request?
- **Verification by external code:** The Verifier could display an additional code that the user must enter in the Wallet, or the Wallet may display an additional code for completing the presentation that must be entered on the Verifier website where the QR code was scanned to complete the presentation. This will not solve the problem, as these codes can easily be captured and replayed by the attacker.
- **Presentation as QR code:** The Wallet could display the credential presentation as a QR code (containing the issuer-signed part and a transaction-specific part). If a Verifier website can capture this presentation, so can an attacker website.

Other potential mitigations are discussed in [Section 6 of the OAuth Cross-Device Security BCP](https://www.ietf.org/archive/id/draft-ietf-oauth-cross-device-security-09.html#name-mitigating-against-cross-de), which applies very similarly to other protocols and technologies.

The only promising mitigation that can actually help to prevent session fixation attacks is by providing a secure channel for cross-device session transfer. This needs support by the operating system and/or browser in order to work.

The only practical approach to this that is specified right now is the [W3C Digitial Credentials API](https://wicg.github.io/digital-credentials/) (DC API). The idea of this API is as following:
- The Verifier can create a request,
- call the browser API with the request,
- the API forwards the request to a Wallet on the same device or on another device,
- the Wallet will be provided both with the request and **a verified origin of the caller website** (e.g., `https://e-gov.example`),
- so that the Wallet can check that the creator (signer) of the request is the same as the caller (origin provided by the API).*

By providing the verified origin, the mismatch between `https://e-gov.example` and `https://egov.example`) could be detected and phishing effectively prevented. The Wallet can trust this origin, as it can check that it comes directly from the API and cannot be influenced by an attacker.

While the implementation details of the API are left open in the current draft, the basic idea to secure cross-device flows using this API is that both sides can, for example, use a bluetooth channel to ensure proximity between the devices after establishing a channel via a QR code. This would make it infeasible for an attacker to forward the request to a random user unless the attacker happens to be in the immediate proximity of the victim.

**Q: Why does this need browser and/or operating system support?** 
A: Using the "origin" as a trust boundary is a long-established security principle in the web. Code provided by a website cannot be trusted to prove its own origin, it needs to be the browser who does that. Additionally, to ensure that the bluetooth proximity check cannot be forwarded, this part needs to be implemented on a lower level, i.e., the browser or operating system.

**Q: Why should I trust my browser?** 
A: Browsers already today take on absolutely critical tasks in securing the web. No single interaction on the web would be secure without the various checks that browsers perform. Therefore, trusting the browser is a requirement for using the web.

(* This is a bit simplified for brevity here. In particular, the Wallet can also include the origin of the caller in the signed presentation, so that the Verifier can check that the request was not forwarded.)