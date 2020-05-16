---
title: Mix-Up, Revisited
tags:
  - draft
layout: publication
type: Analysis
---


- [Mix-Up, Revisited](#mix-up-revisited)
  - [Basic Mix-Up Example](#basic-mix-up-example)
    - [How to Defend Against Mix-Up?](#how-to-defend-against-mix-up)
  - [With OAuth Metadata](#with-oauth-metadata)
    - [Simple Mix-Up](#simple-mix-up)
    - [Mix-Up with Confidential Clients and PKCE](#mix-up-with-confidential-clients-and-pkce)
    - [Stealing Access Tokens](#stealing-access-tokens)
    - [Defending Against Mix-Up with Metadata](#defending-against-mix-up-with-metadata)
- [Mixup With PAR](#mixup-with-par)
- [Integrity of the Authorization Request with PAR](#integrity-of-the-authorization-request-with-par)
- [Mitigations](#mitigations)

A Mix-Up Attack on OAuth is an attack wherein the attacker manages to convince the client to send credentials (authorization code or access token) obtained from an "honest" authorization server to a server under the attacker's control.

## Basic Mix-Up Example
Assume that a user wants to start an OAuth flow using the malicious OAuth provider (OP) `attacker.com`. That OP might hide its true identity or, in a large ecosystem, may be an OP that has been compromised. 

Even if all connections are properly secured via TLS, the following attack can be mounted by `attacker.com`:



<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" contentScriptType="application/ecmascript" contentStyleType="text/css" height="543px" preserveAspectRatio="none" style="width:759px;height:543px;" version="1.1" viewBox="0 0 759 543" width="759px" zoomAndPan="magnify"><defs/><g><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="43" x2="43" y1="34.2969" y2="502.9531"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="329" x2="329" y1="34.2969" y2="502.9531"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="589.5" x2="589.5" y1="34.2969" y2="502.9531"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="699.5" x2="699.5" y1="34.2969" y2="502.9531"/><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="71" x="8" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="57" x="15" y="22.9951">Browser</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="71" x="8" y="501.9531"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="57" x="15" y="521.9482">Browser</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="85" x="287" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="71" x="294" y="22.9951">client.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="85" x="287" y="501.9531"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="71" x="294" y="521.9482">client.com</text><rect fill="#C3744B" height="30.2969" style="stroke: #C3744B; stroke-width: 1.5;" width="104" x="537.5" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="90" x="544.5" y="22.9951">attacker.com</text><rect fill="#C3744B" height="30.2969" style="stroke: #C3744B; stroke-width: 1.5;" width="104" x="537.5" y="501.9531"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="90" x="544.5" y="521.9482">attacker.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="97" x="651.5" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="83" x="658.5" y="22.9951">honest.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="97" x="651.5" y="501.9531"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="83" x="658.5" y="521.9482">honest.com</text><polygon fill="#375A7F" points="317.5,61.4297,327.5,65.4297,317.5,69.4297,321.5,65.4297" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="323.5" y1="65.4297" y2="65.4297"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="159" x="50.5" y="60.3638">Use https://attacker.com</text><polygon fill="#375A7F" points="54.5,166.2266,44.5,170.2266,54.5,174.2266,50.5,170.2266" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="328.5" y1="170.2266" y2="170.2266"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="225" x="60.5" y="89.4966">Location: https://attacker.com/auth</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="205" x="92.5" y="104.6294">?redirect_uri=https://client.com/</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="188" x="108.5" y="119.7622">&amp;client_id=client_at_attacker</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="186" x="108.5" y="134.895">&amp;code_challenge=sha256(n)</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="62" x="108.5" y="150.0278">&amp;state=s</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="23" x="108.5" y="165.1606">&amp;...</text><path d="M334,113.2617 L334,138.2617 L597,138.2617 L597,123.2617 L587,113.2617 L334,113.2617 " fill="#CEE1F5" style="stroke: #CEE1F5; stroke-width: 1.0;"/><path d="M587,113.2617 L587,123.2617 L597,123.2617 L587,113.2617 " fill="#CEE1F5" style="stroke: #CEE1F5; stroke-width: 1.0;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="242" x="340" y="130.3286">stored: AS to be used is attacker.com</text><polygon fill="#375A7F" points="577.5,195.3594,587.5,199.3594,577.5,203.3594,581.5,199.3594" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="583.5" y1="199.3594" y2="199.3594"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="211" x="50.5" y="194.2935">GET https://attacker.com/auth?...</text><polygon fill="#375A7F" points="54.5,285.0234,44.5,289.0234,54.5,293.0234,50.5,289.0234" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="588.5" y1="289.0234" y2="289.0234"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="421" x="60.5" y="223.4263">Location: https://honest.com/auth?redirect_uri=https://client.com/</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="74" x="108.5" y="238.5591">&amp;client_id=</text><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="105" x="182.5" y="238.5591">client_at_honest</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="121" x="108.5" y="253.6919">&amp;code_challenge=</text><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="7" x="229.5" y="253.6919">k</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="62" x="108.5" y="268.8247">&amp;state=s</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="23" x="108.5" y="283.9575">&amp;...</text><polygon fill="#375A7F" points="688,314.1563,698,318.1563,688,322.1563,692,318.1563" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="694" y1="318.1563" y2="318.1563"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="206" x="50.5" y="313.0903">GET https://honest.com/auth?....</text><polygon fill="#375A7F" points="54.5,343.2891,44.5,347.2891,54.5,351.2891,50.5,347.2891" style="stroke: #375A7F; stroke-width: 1.0;"/><polygon fill="#375A7F" points="688,343.2891,698,347.2891,688,351.2891,692,347.2891" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0; stroke-dasharray: 2.0,2.0;" x1="48.5" x2="694" y1="347.2891" y2="347.2891"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="216" x="60.5" y="342.2231">user authentication, authorization</text><polygon fill="#375A7F" points="54.5,372.4219,44.5,376.4219,54.5,380.4219,50.5,376.4219" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="699" y1="376.4219" y2="376.4219"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="306" x="60.5" y="371.356">Redirect to https://client.com/?code=c&amp;state=s</text><polygon fill="#375A7F" points="317.5,401.5547,327.5,405.5547,317.5,409.5547,321.5,405.5547" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="323.5" y1="405.5547" y2="405.5547"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="262" x="50.5" y="400.4888">GET https://client.com/?code=c&amp;state=s</text><polygon fill="#375A7F" points="577.5,445.8203,587.5,449.8203,577.5,453.8203,581.5,449.8203" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="329.5" x2="583.5" y1="449.8203" y2="449.8203"/><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="236" x="336.5" y="429.6216">GET /token?code_verifier=n&amp;code=c</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="0" x="352.5" y="444.7544"/><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="168" x="352.5" y="444.7544">&amp;state=s&amp;redirect_uri=...</text><path d="M594,462.8203 L594,487.8203 L726,487.8203 L726,472.8203 L716,462.8203 L594,462.8203 " fill="#FFCEB5" style="stroke: #FFCEB5; stroke-width: 1.0;"/><path d="M716,462.8203 L716,472.8203 L726,472.8203 L716,462.8203 " fill="#FFCEB5" style="stroke: #FFCEB5; stroke-width: 1.0;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="111" x="600" y="479.8872">Attack successful</text><!--MD5=[20e4fed6490476b028b1232dbd524111]
@startuml
hide stereotype
skinparam shadowing false
skinparam sequence {
ArrowColor #375a7f
LifeLineBorderColor #ccc

ParticipantBorderColor #375a7f
ParticipantBackgroundColor #375a7f
ParticipantFontColor #fff
ParticipantFontName Roboto
ParticipantFontSize 14

ParticipantBorderColor<<Attacker>> #C3744B
ParticipantBackgroundColor<<Attacker>> #C3744B
}

skinparam note {
BackgroundColor #CEE1F5
BorderColor #CEE1F5
FontColor #000

BackgroundColor<<warning>> #FFCEB5
BorderColor<<warning>> #FFCEB5

BackgroundColor<<ok>> #C6EAA6
BorderColor<<ok>> #C6EAA6
}

participant Browser
participant client.com
participant attacker.com <<Attacker>>
participant honest.com

Browser -> client.com: Use https://attacker.com
client.com -> Browser: Location: https://attacker.com/auth\n        ?redirect_uri=https://client.com/\n            &client_id=client_at_attacker\n            &code_challenge=sha256(n)\n            &state=s\n            &...
note right: stored: AS to be used is attacker.com

Browser -> attacker.com: GET https://attacker.com/auth?...
attacker.com -> Browser: Location: https:~//honest.com/auth?redirect_uri=https://client.com/\n            &client_id=<font color=red>client_at_honest\n            &code_challenge=<font color=red>k</font>\n            &state=s\n            &...
Browser -> honest.com: GET https:~//honest.com/auth?....
Browser <- -> honest.com: user authentication, authorization
honest.com -> Browser: Redirect to https://client.com/?code=c&state=s
Browser -> client.com: GET https://client.com/?code=c&state=s
client.com -> attacker.com: <font color=red>GET /token?code_verifier=n&code=c\n    <font color=red>&state=s&redirect_uri=...

note<<warning>> right attacker.com 
    Attack successful
end note
@enduml

PlantUML version 1.2020.08(Sun Apr 26 14:08:22 UTC 2020)
(GPL source distribution)
Java Runtime: OpenJDK Runtime Environment
JVM: OpenJDK 64-Bit Server VM
Java Version: 1.8.0_252-b09
Operating System: Linux
Default Encoding: UTF-8
Language: en
Country: null
--></g></svg>

In the attack, the attacker's authorization server redirects the user to an honest OP's authorization server. The attacker replaces the `client_id` provided by the client with the one that the client uses for `honest.com` and replaces the `code_challenge` parameter with a different value.

After the uses authorizes access, the attacker is able to capture the code that was used in this flow, as it is sent to the attacker's token endpoint.

The code is bound to the PKCE challenge known to the attacker. If the attacker has chosen k to be a value from another flow with the same client and honest.com as AS, the attacker can inject the code in that flow. (This requires an "online" attack, i.e., the attacker cannot collect codes first and then redeem them.)

(This shows the authorization code grant, but the attack is applicable as well to the Implicit Grant.)


### How to Defend Against Mix-Up?

The guiding principle in defending against Mix-Up Attacks is that the authorization server must make its identity clear to the relying party. Since a successful Mix-Up Attack necessarily involves an honest authorization server, this defence does not rely on the honesty of the attacker.

The following two approaches can be used for this:

 * An `iss` parameter in the authorization response could tell client.com about the identity of the authorization server that was used. 

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" contentScriptType="application/ecmascript" contentStyleType="text/css" height="505px" preserveAspectRatio="none" style="width:785px;height:505px;" version="1.1" viewBox="0 0 785 505" width="785px" zoomAndPan="magnify"><defs/><g><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="43" x2="43" y1="34.2969" y2="465.6875"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="390" x2="390" y1="34.2969" y2="465.6875"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="615.5" x2="615.5" y1="34.2969" y2="465.6875"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="725.5" x2="725.5" y1="34.2969" y2="465.6875"/><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="71" x="8" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="57" x="15" y="22.9951">Browser</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="71" x="8" y="464.6875"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="57" x="15" y="484.6826">Browser</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="85" x="348" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="71" x="355" y="22.9951">client.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="85" x="348" y="464.6875"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="71" x="355" y="484.6826">client.com</text><rect fill="#C3744B" height="30.2969" style="stroke: #C3744B; stroke-width: 1.5;" width="104" x="563.5" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="90" x="570.5" y="22.9951">attacker.com</text><rect fill="#C3744B" height="30.2969" style="stroke: #C3744B; stroke-width: 1.5;" width="104" x="563.5" y="464.6875"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="90" x="570.5" y="484.6826">attacker.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="97" x="677.5" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="83" x="684.5" y="22.9951">honest.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="97" x="677.5" y="464.6875"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="83" x="684.5" y="484.6826">honest.com</text><polygon fill="#375A7F" points="378.5,61.4297,388.5,65.4297,378.5,69.4297,382.5,65.4297" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="384.5" y1="65.4297" y2="65.4297"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="159" x="50.5" y="60.3638">Use https://attacker.com</text><polygon fill="#375A7F" points="54.5,166.2266,44.5,170.2266,54.5,174.2266,50.5,170.2266" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="389.5" y1="170.2266" y2="170.2266"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="225" x="60.5" y="89.4966">Location: https://attacker.com/auth</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="205" x="92.5" y="104.6294">?redirect_uri=https://client.com/</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="188" x="108.5" y="119.7622">&amp;client_id=client_at_attacker</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="186" x="108.5" y="134.895">&amp;code_challenge=sha256(n)</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="62" x="108.5" y="150.0278">&amp;state=s</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="23" x="108.5" y="165.1606">&amp;...</text><path d="M395,113.2617 L395,138.2617 L586,138.2617 L586,123.2617 L576,113.2617 L395,113.2617 " fill="#CEE1F5" style="stroke: #CEE1F5; stroke-width: 1.0;"/><path d="M576,113.2617 L576,123.2617 L586,123.2617 L576,113.2617 " fill="#CEE1F5" style="stroke: #CEE1F5; stroke-width: 1.0;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="170" x="401" y="130.3286">stored: AS is attacker.com</text><polygon fill="#375A7F" points="603.5,195.3594,613.5,199.3594,603.5,203.3594,607.5,199.3594" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="609.5" y1="199.3594" y2="199.3594"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="211" x="50.5" y="194.2935">GET https://attacker.com/auth?...</text><polygon fill="#375A7F" points="54.5,285.0234,44.5,289.0234,54.5,293.0234,50.5,289.0234" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="614.5" y1="289.0234" y2="289.0234"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="421" x="60.5" y="223.4263">Location: https://honest.com/auth?redirect_uri=https://client.com/</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="74" x="108.5" y="238.5591">&amp;client_id=</text><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="105" x="182.5" y="238.5591">client_at_honest</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="121" x="108.5" y="253.6919">&amp;code_challenge=</text><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="7" x="229.5" y="253.6919">k</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="62" x="108.5" y="268.8247">&amp;state=s</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="23" x="108.5" y="283.9575">&amp;...</text><polygon fill="#375A7F" points="714,314.1563,724,318.1563,714,322.1563,718,318.1563" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="720" y1="318.1563" y2="318.1563"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="206" x="50.5" y="313.0903">GET https://honest.com/auth?....</text><polygon fill="#375A7F" points="54.5,343.2891,44.5,347.2891,54.5,351.2891,50.5,347.2891" style="stroke: #375A7F; stroke-width: 1.0;"/><polygon fill="#375A7F" points="714,343.2891,724,347.2891,714,351.2891,718,347.2891" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0; stroke-dasharray: 2.0,2.0;" x1="48.5" x2="720" y1="347.2891" y2="347.2891"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="216" x="60.5" y="342.2231">user authentication, authorization</text><polygon fill="#375A7F" points="54.5,372.4219,44.5,376.4219,54.5,380.4219,50.5,376.4219" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="725" y1="376.4219" y2="376.4219"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="306" x="60.5" y="371.356">Redirect to https://client.com/?code=c&amp;state=s</text><text fill="#0000FF" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="160" x="366.5" y="371.356">&amp;iss=https://honest.com</text><polygon fill="#375A7F" points="378.5,401.5547,388.5,405.5547,378.5,409.5547,382.5,405.5547" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="384.5" y1="405.5547" y2="405.5547"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="163" x="50.5" y="400.4888">GET https://client.com/?...</text><text fill="#0000FF" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="160" x="213.5" y="400.4888">&amp;iss=https://honest.com</text><line style="stroke: #375A7F; stroke-width: 1.0;" x1="390.5" x2="432.5" y1="434.6875" y2="434.6875"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="432.5" x2="432.5" y1="434.6875" y2="447.6875"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="391.5" x2="432.5" y1="447.6875" y2="447.6875"/><polygon fill="#375A7F" points="401.5,443.6875,391.5,447.6875,401.5,451.6875,397.5,447.6875" style="stroke: #375A7F; stroke-width: 1.0;"/><text fill="#0000FF" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="211" x="397.5" y="429.6216">iss does not match attacker.com</text><path d="M620,422.0547 L620,447.0547 L738,447.0547 L738,432.0547 L728,422.0547 L620,422.0547 " fill="#C6EAA6" style="stroke: #C6EAA6; stroke-width: 1.0;"/><path d="M728,422.0547 L728,432.0547 L738,432.0547 L728,422.0547 " fill="#C6EAA6" style="stroke: #C6EAA6; stroke-width: 1.0;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="97" x="626" y="439.1216">Attack stopped</text><!--MD5=[4bb5f44e06010230c3803c0ac918ae2f]
@startuml
hide stereotype
skinparam shadowing false
skinparam sequence {
ArrowColor #375a7f
LifeLineBorderColor #ccc

ParticipantBorderColor #375a7f
ParticipantBackgroundColor #375a7f
ParticipantFontColor #fff
ParticipantFontName Roboto
ParticipantFontSize 14

ParticipantBorderColor<<Attacker>> #C3744B
ParticipantBackgroundColor<<Attacker>> #C3744B
}

skinparam note {
BackgroundColor #CEE1F5
BorderColor #CEE1F5
FontColor #000

BackgroundColor<<warning>> #FFCEB5
BorderColor<<warning>> #FFCEB5

BackgroundColor<<ok>> #C6EAA6
BorderColor<<ok>> #C6EAA6
}

participant Browser
participant client.com
participant attacker.com <<Attacker>>
participant honest.com

Browser -> client.com: Use https://attacker.com
client.com -> Browser: Location: https://attacker.com/auth\n        ?redirect_uri=https://client.com/\n            &client_id=client_at_attacker\n            &code_challenge=sha256(n)\n            &state=s\n            &...
note right: stored: AS is attacker.com

Browser -> attacker.com: GET https://attacker.com/auth?...
attacker.com -> Browser: Location: https:~//honest.com/auth?redirect_uri=https://client.com/\n            &client_id=<font color=red>client_at_honest\n            &code_challenge=<font color=red>k</font>\n            &state=s\n            &...
Browser -> honest.com: GET https:~//honest.com/auth?....
Browser <- -> honest.com: user authentication, authorization
honest.com -> Browser: Redirect to https://client.com/?code=c&state=s<font color=blue>&iss=https:~//honest.com
Browser -> client.com: GET https://client.com/?...<font color=blue>&iss=https:~//honest.com
client.com -> client.com: <font color=blue>iss does not match attacker.com
note<<ok>> right
    Attack stopped
end note
@enduml

PlantUML version 1.2020.08(Sun Apr 26 14:08:22 UTC 2020)
(GPL source distribution)
Java Runtime: OpenJDK Runtime Environment
JVM: OpenJDK 64-Bit Server VM
Java Version: 1.8.0_252-b09
Operating System: Linux
Default Encoding: UTF-8
Language: en
Country: null
--></g></svg>


 * Encoding the authorization server's identity in the redirect_uri can help as well. In this case, the client compares the redirection endpoint where it expects the user to land with the one registered for the expected authorization server.


<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" contentScriptType="application/ecmascript" contentStyleType="text/css" height="521px" preserveAspectRatio="none" style="width:814px;height:521px;" version="1.1" viewBox="0 0 814 521" width="814px" zoomAndPan="magnify"><defs/><g><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="43" x2="43" y1="34.2969" y2="480.8203"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="424" x2="424" y1="34.2969" y2="480.8203"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="644.5" x2="644.5" y1="34.2969" y2="480.8203"/><line style="stroke: #CCCCCC; stroke-width: 1.0; stroke-dasharray: 5.0,5.0;" x1="754.5" x2="754.5" y1="34.2969" y2="480.8203"/><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="71" x="8" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="57" x="15" y="22.9951">Browser</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="71" x="8" y="479.8203"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="57" x="15" y="499.8154">Browser</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="85" x="382" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="71" x="389" y="22.9951">client.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="85" x="382" y="479.8203"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="71" x="389" y="499.8154">client.com</text><rect fill="#C3744B" height="30.2969" style="stroke: #C3744B; stroke-width: 1.5;" width="104" x="592.5" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="90" x="599.5" y="22.9951">attacker.com</text><rect fill="#C3744B" height="30.2969" style="stroke: #C3744B; stroke-width: 1.5;" width="104" x="592.5" y="479.8203"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="90" x="599.5" y="499.8154">attacker.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="97" x="706.5" y="3"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="83" x="713.5" y="22.9951">honest.com</text><rect fill="#375A7F" height="30.2969" style="stroke: #375A7F; stroke-width: 1.5;" width="97" x="706.5" y="479.8203"/><text fill="#FFFFFF" font-family="Roboto" font-size="14" lengthAdjust="spacingAndGlyphs" textLength="83" x="713.5" y="499.8154">honest.com</text><polygon fill="#375A7F" points="412.5,61.4297,422.5,65.4297,412.5,69.4297,416.5,65.4297" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="418.5" y1="65.4297" y2="65.4297"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="159" x="50.5" y="60.3638">Use https://attacker.com</text><polygon fill="#375A7F" points="54.5,166.2266,44.5,170.2266,54.5,174.2266,50.5,170.2266" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="423.5" y1="170.2266" y2="170.2266"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="225" x="60.5" y="89.4966">Location: https://attacker.com/auth</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="205" x="92.5" y="104.6294">?redirect_uri=https://client.com/</text><text fill="#0000FF" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="95" x="297.5" y="104.6294">as/honest.com</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="188" x="108.5" y="119.7622">&amp;client_id=client_at_attacker</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="186" x="108.5" y="134.895">&amp;code_challenge=sha256(n)</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="62" x="108.5" y="150.0278">&amp;state=s</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="23" x="108.5" y="165.1606">&amp;...</text><path d="M429,113.2617 L429,138.2617 L620,138.2617 L620,123.2617 L610,113.2617 L429,113.2617 " fill="#CEE1F5" style="stroke: #CEE1F5; stroke-width: 1.0;"/><path d="M610,113.2617 L610,123.2617 L620,123.2617 L610,113.2617 " fill="#CEE1F5" style="stroke: #CEE1F5; stroke-width: 1.0;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="170" x="435" y="130.3286">stored: AS is attacker.com</text><polygon fill="#375A7F" points="632.5,195.3594,642.5,199.3594,632.5,203.3594,636.5,199.3594" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="638.5" y1="199.3594" y2="199.3594"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="211" x="50.5" y="194.2935">GET https://attacker.com/auth?...</text><polygon fill="#375A7F" points="54.5,285.0234,44.5,289.0234,54.5,293.0234,50.5,289.0234" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="643.5" y1="289.0234" y2="289.0234"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="421" x="60.5" y="223.4263">Location: https://honest.com/auth?redirect_uri=https://client.com/</text><text fill="#0000FF" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="95" x="481.5" y="223.4263">as/honest.com</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="74" x="108.5" y="238.5591">&amp;client_id=</text><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="105" x="182.5" y="238.5591">client_at_honest</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="121" x="108.5" y="253.6919">&amp;code_challenge=</text><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="7" x="229.5" y="253.6919">k</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="62" x="108.5" y="268.8247">&amp;state=s</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="23" x="108.5" y="283.9575">&amp;...</text><polygon fill="#375A7F" points="743,314.1563,753,318.1563,743,322.1563,747,318.1563" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="749" y1="318.1563" y2="318.1563"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="206" x="50.5" y="313.0903">GET https://honest.com/auth?....</text><polygon fill="#375A7F" points="54.5,343.2891,44.5,347.2891,54.5,351.2891,50.5,347.2891" style="stroke: #375A7F; stroke-width: 1.0;"/><polygon fill="#375A7F" points="743,343.2891,753,347.2891,743,351.2891,747,347.2891" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0; stroke-dasharray: 2.0,2.0;" x1="48.5" x2="749" y1="347.2891" y2="347.2891"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="216" x="60.5" y="342.2231">user authentication, authorization</text><polygon fill="#375A7F" points="54.5,372.4219,44.5,376.4219,54.5,380.4219,50.5,376.4219" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="48.5" x2="754" y1="376.4219" y2="376.4219"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="188" x="60.5" y="371.356">Redirect to https://client.com/</text><text fill="#0000FF" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="95" x="248.5" y="371.356">as/honest.com</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="118" x="343.5" y="371.356">?code=c&amp;state=s</text><polygon fill="#375A7F" points="412.5,401.5547,422.5,405.5547,412.5,409.5547,416.5,405.5547" style="stroke: #375A7F; stroke-width: 1.0;"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="43.5" x2="418.5" y1="405.5547" y2="405.5547"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="144" x="50.5" y="400.4888">GET https://client.com/</text><text fill="#0000FF" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="95" x="194.5" y="400.4888">as/honest.com</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="118" x="289.5" y="400.4888">?code=c&amp;state=s</text><line style="stroke: #375A7F; stroke-width: 1.0;" x1="424.5" x2="466.5" y1="449.8203" y2="449.8203"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="466.5" x2="466.5" y1="449.8203" y2="462.8203"/><line style="stroke: #375A7F; stroke-width: 1.0;" x1="425.5" x2="466.5" y1="462.8203" y2="462.8203"/><polygon fill="#375A7F" points="435.5,458.8203,425.5,462.8203,435.5,466.8203,431.5,462.8203" style="stroke: #375A7F; stroke-width: 1.0;"/><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="190" x="431.5" y="429.6216">issuer encoded in redirect URI</text><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="0" x="447.5" y="444.7544"/><text fill="#FF0000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="190" x="447.5" y="444.7544">does not match attacker.com</text><path d="M649,429.6211 L649,454.6211 L767,454.6211 L767,439.6211 L757,429.6211 L649,429.6211 " fill="#C6EAA6" style="stroke: #C6EAA6; stroke-width: 1.0;"/><path d="M757,429.6211 L757,439.6211 L767,439.6211 L757,429.6211 " fill="#C6EAA6" style="stroke: #C6EAA6; stroke-width: 1.0;"/><text fill="#000000" font-family="sans-serif" font-size="13" lengthAdjust="spacingAndGlyphs" textLength="97" x="655" y="446.688">Attack stopped</text><!--MD5=[915c0ee6f96fef8c832c05131939eb4c]
@startuml
hide stereotype
skinparam shadowing false
skinparam sequence {
ArrowColor #375a7f
LifeLineBorderColor #ccc

ParticipantBorderColor #375a7f
ParticipantBackgroundColor #375a7f
ParticipantFontColor #fff
ParticipantFontName Roboto
ParticipantFontSize 14

ParticipantBorderColor<<Attacker>> #C3744B
ParticipantBackgroundColor<<Attacker>> #C3744B
}

skinparam note {
BackgroundColor #CEE1F5
BorderColor #CEE1F5
FontColor #000

BackgroundColor<<warning>> #FFCEB5
BorderColor<<warning>> #FFCEB5

BackgroundColor<<ok>> #C6EAA6
BorderColor<<ok>> #C6EAA6
}


participant Browser
participant client.com
participant attacker.com <<Attacker>>
participant honest.com

Browser -> client.com: Use https://attacker.com
client.com -> Browser: Location: https://attacker.com/auth\n        ?redirect_uri=https://client.com/<font color=blue>as/honest.com</font>\n            &client_id=client_at_attacker\n            &code_challenge=sha256(n)\n            &state=s\n            &...
note right: stored: AS is attacker.com

Browser -> attacker.com: GET https://attacker.com/auth?...
attacker.com -> Browser: Location: https:~//honest.com/auth?redirect_uri=https://client.com/<font color=blue>as/honest.com</font>\n            &client_id=<font color=red>client_at_honest\n            &code_challenge=<font color=red>k</font>\n            &state=s\n            &...
Browser -> honest.com: GET https:~//honest.com/auth?....
Browser <- -> honest.com: user authentication, authorization
honest.com -> Browser: Redirect to https://client.com/<font color=blue>as/honest.com</font>?code=c&state=s
Browser -> client.com: GET https://client.com/<font color=blue>as/honest.com</font>?code=c&state=s
client.com -> client.com: <font color=red>issuer encoded in redirect URI\n    <font color=red>does not match attacker.com
note<<ok>> right
    Attack stopped
end note
@enduml

PlantUML version 1.2020.08(Sun Apr 26 14:08:22 UTC 2020)
(GPL source distribution)
Java Runtime: OpenJDK Runtime Environment
JVM: OpenJDK 64-Bit Server VM
Java Version: 1.8.0_252-b09
Operating System: Linux
Default Encoding: UTF-8
Language: en
Country: null
--></g></svg>

**Why does that work?**

If OAuth Metadata or OpenID Connect Configuration are *not* used, one can expect that the client lives in an ecosystem where there is a clear connection between the selected OAuth Provider and the authorization server through some out-of-band mechanism. For example, a client could have multiple OAuth providers configured manually using a simple table as follows:

| Provider       | Authorization Endpoint       | Token Endpoint               | Resource Server            |
| -------------- | ---------------------------- | ---------------------------- | -------------------------- |
| Awesome OAuth  | https://awesome.auth/authz   | https://awesome.auth/token   | https://awesome.auth/api   |
| Other Provider | https://some.other.idp/login | https://some.other.idp/te    | https://some.other.idp/    |
| Malicious OP   | https://malicious.auth/auth  | https://malicious.auth/token | https://malicious.auth/res |
| ...            | ...                          | ...                          | ...                        |

*(Assumption here: There is an effective mechanism to stop the malicious OP from registering one of the benign authorization servers at the client.)*

This means that the client knows whether a particular authorization server belongs to a particular OAuth Provider (there is often a 1:1 mapping). The provider is identified using some internal mechanism. Therefore, if the client starts a flow using a particular provider, the authorization endpoint's identity is enough to check whether that authorization server belongs to the expected provider.

**Is there a need to tie the code and the iss parameter together in the authorization response?**

This is not needed if the authorization response is sent from the authorization server via the user's browser to the client and that there is no opportunity for the attacker to modify the response.

If the attacker can modify the response, [JARM](https://openid.net/specs/openid-financial-api-jarm-ID1.html#jwt-based-response-mode) could prevent tampering. The catch is that with metadata (see below), the attacker can control the keys used for signature verification. Therefore, there is no value in adding JARM.

However, if the attacker can modify the response, he can also read the authorization code. For Mix-Up attacks targeting the authorization code, we can therefore assume that the attacker cannot modify the response, because otherwise, there would be no need for the attacker to mount a mix-up attack. For Mix-Up attacks targeting the access token, this is not so clear.





## With OAuth Metadata

### Simple Mix-Up

Assume that an attacker sets up the following OAuth Metadata:

```json
{
    "issuer": "https://attacker.com",
    "authorization_endpoint": "https://honest.com/authorize",
    "token_endpoint": "https://attacker.com/token"
}
```

(This is the setup presented in https://arxiv.org/pdf/1508.04324.pdf)

In this case, the attack as above works as well. The client will send the user to the honest authorization endpoint, but then send the code to the manipulated token endpoint. The attacker can redeem the code for an access token at the token endpoint if the client is a public client.

### Mix-Up with Confidential Clients and PKCE

That is nice, but if the client is a confidential client, the attacker cannot redeem the code for an authorization token. One way around this limitation is a [Code Injection Attack](https://tools.ietf.org/id/draft-ietf-oauth-security-topics-14.html#rfc.section.4.5). This attack is normally [protected against with PKCE](https://tools.ietf.org/id/draft-ietf-oauth-security-topics-14.html#rfc.section.4.5.3). 

Here, however, there is a way for the attacker to change the PKCE Challenge that is used for the authorization flow. To conduct this attack, the attacker uses his own endpoint in the Metadata:

```json
{
    "issuer": "https://attacker.com",
    "authorization_endpoint": "https://attacker.com/authorize",
    "token_endpoint": "https://attacker.com/token"
}
``` 
When a user arrives at that endpoint, attacker starts an OAuth session with the *same* confidential client. From his session, the attacker extracts the PKCE Challenge and then redirects the user that arrived at the attacker's authorization endpoint  just as in the first example but replaces the PKCE Challenge by the one from his own session with the client.

The attacker can then inject the code acquired from the user's session into his own session with the client. This attack is called a [PKCE Chosen Challenge Attack](https://datatracker.ietf.org/meeting/105/materials/slides-105-oauth-sessa-oauth-security-topics-00)).

### Stealing Access Tokens

It is possible to steal the access token as well using the following configuration:

```json
{
    "issuer": "https://attacker.com",
    "authorization_endpoint": "https://honest.com/authorize",  # or attacker.com and then redirect
    "token_endpoint": "https://honest.com/token",
    "userinfo_endpoint": "https://attacker.com/userinfo"
}
```

### Defending Against Mix-Up with Metadata

The difference to the scenario without metadata is that the client now has an issuer URI and resolves the authorization server using the issuer URI. An attacker can, as shown, assign the honest authorization server to his own issuer. It is therefore necessary that the authorization server signals for which issuers it may be used, as that implies the issuer configurations and thereby the token and userinfo endpoints that are being used.

Importantly, it is not enough that the autorization server identifies *itself* (i.e., using its URL or a redirection URI that is unique to itself), but it needs to identify the *issuer*.

> **Recommendation:** The security BCP needs to make clear that *per-AS* redirect URIs are only sufficient if OAuth Metadata is not used to resolve multiple issuers. Otherwise, *per-Issuer* redirect URIs or the `iss` parameter MUST be used.

# Mixup With PAR

What if put PAR into the mix? It complicates things.

```json
{
    "issuer": "https://attacker.com",
    "pushed_authorization_request_endpoint": "https://attacker.com/par",
    "authorization_endpoint": "https://attacker.com/authorize",
    "token_endpoint": "https://attacker.com/token",
    "userinfo_endpoint": "https://attacker.com/userinfo"
}
``` 

We now have four endpoints that can be either set to the honest server's endpoints or the attacker's own endpoints. This makes 16 possible combinations.

The following table lists the 16 possible combinations (`H`=honest server's endpoint, `A`=attacker's endpoint). The potential attacks that arise are referenced in the table, separated for public and confidential clients, and listed below.

| PAR   | Authz | Tok   | UInfo | Attacks for public clients         | for confidential clients              |
| ----- | ----- | ----- | ----- | ---------------------------------- | ------------------------------------- |
| `H`   | `H`   | `H`   | `H`   | no mix-up attack                   | *                                     |
| `H`   | `H`   | `H`   | `Att` | [token to UInfo]                   | *                                     |
| `H`   | `H`   | `Att` | `H`   | [code to Tok-PC] [token injection] | * [code to Tok-NCI] [token injection] |
| `H`   | `H`   | `Att` | `Att` | [code to Tok-PC]                   | * [code to Tok-NCI]                   |
| `H`   | `Att` | `H`   | `H`   | no mix-up attack                   | * same                                |
| `H`   | `Att` | `H`   | `Att` | [token to UInfo]                   | * same                                |
| `H`   | `Att` | `Att` | `H`   | [code to Tok-PC] [token injection] | * [code to Tok*] [token injection]    |
| `H`   | `Att` | `Att` | `Att` | [code to Tok-PC]                   | * [code to Tok*]                      |
| `Att` | `H`   | `H`   | `H`   | no mix-up attack                   | -                                     |
| `Att` | `H`   | `H`   | `Att` | [token to UInfo]                   | same                                  |
| `Att` | `H`   | `Att` | `H`   | [code to Tok-PC] [token injection] | [code to Tok] [token injection]       |
| `Att` | `H`   | `Att` | `Att` | [code to Tok-PC]                   | [code to Tok]                         |
| `Att` | `Att` | `H`   | `H`   | no mix-up attack                   | same                                  |
| `Att` | `Att` | `H`   | `Att` | [token to UInfo]                   | same                                  |
| `Att` | `Att` | `Att` | `H`   | [code to Tok-PC]                   | [code to Tok]                         |
| `Att` | `Att` | `Att` | `Att` | [code to Tok-PC]                   | [code to Tok]                         |


[*] or no mix-up depending on deployment - client credentials might not match the ones that need to be presented

Mix-Up Attacks:

 * [token to UInfo]: Token is sent to attacker's endpoint as shown above.
 * [code to Tok-PC]: Code is sent to attacker's endpoint as shown above. Code is readily usable by the attacker as it is not issued for a confidential client.
 * [code to Tok-NCI]: Code is sent to attacker's endpoint as shown above. Code injection is prevented as the    attacker cannot exchange the PKCE Challenge.
 * [code to Tok]: Code is sent to attacker's endpoint as shown above. Attacker can inject the stolen code using code injection with PKCE Chosen Challenge as shown above.
 * [code to Tok*]: Code is sent to attacker's endpoint as shown above. If the authorization server accepts non-PAR requests, the attacker can inject the stolen code using code injection with PKCE Chosen Challenge as shown above.
 * [token injection]: The attacker can send an access token to the client that is then used by the client for the resource server. This can defeat sender-constrained tokens, [as described in this paper](https://arxiv.org/abs/1901.11520).
 * [authz-mitm]: The attacker can change all contents of the authorization request.
 
Other attacks:

 * If the authorization endpoint points to the attacker, the attacker can break session integrity, i.e., logging in the user under a different identity.
 * If the UserInfo endpoint points to the attacker, the attacker can send spoofed user information to the client.
 * PAR promises integrity for the authorization request. This can be undermined in certain conditions, see below.


# Integrity of the Authorization Request with PAR

PAR with client authentication promises integrity for the authorization request by sending all the data of the authorization request via the backend.

 1. If the PAR endpoint does not point to an attacker's endpoint, PAR protects against attack variants where the attacker exchanges the PKCE Challenge. The attacker can, however, still forward the whole authorization request with the `request_uri` to the victim, and if the victim authorizes the request, the attacker can  grab the code. 
 1. If the PAR endpoint points to the attacker, the attacker has the option of taking the parameters from the PAR request, changing them into URL parameters (and maybe manipulating them), and creating an authorization request URL from them. If the authorization endpoint also points to an endpoint of the attacker, the attacker can just forward the user to the newly created authorization request URL at the honest server. If the authorization endpoint is not under the control of the attacker, the attacker can try to use HTTP request parameter pollution to influence the authorization request the client sends to the authorization server.


> Recommendation: PAR-enabled authorization servers can **protect the integrity better** and **protect against Mix-Up Attacks better** if they ONLY accept PAR requests.

# Mitigations

 * Adding an `iss` parameter to the PAR request will probably not solve the problem; the AS can still be mixed-up.
 * The `iss` parameter in the authorization response (and a check performed by the client) solves all mix-up variants listed above.
 * A per-issuer-redirect uri can be confused with a per-AS-redirect URI, the latter would not solve mix-up.

> Recommendation: Emphasize importance of `iss` parameter (or `issuer`) in authorization response. Maybe introduce this parameter in the security BCP or another document?

 * As described above, there is probably no value in adding JARM to protect the issuer parameter in the authorization response. 
 * Attacks where the token endpoint is at the honest AS and the userinfo endpoint or another resource is at the attacker can be mitigated by using sender-constrained access tokens. An attacker would not be able to replay the token at another endpoint.

> Sender-constrained access tokens rock.

> Sender-constraining the authorization code (PAR + PAR-DPoP?) might be worth looking into.
