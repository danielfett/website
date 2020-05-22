---
title: Finding and Fixing TLS Misconfigurations with TLS Profiler
type: Howto
layout: publication
---

To secure data in transport for web services and web sites, TLS is indispensable. But just enabling TLS is not enough: Several different TLS versions and many dozens of options exist for their usage, and it is very hard to tell which combinations are secure and which are not, and which are compatible with certain browsers and devices. In this howto, I introduce TLS Profiler, a new open source tool to scan for TLS misconfigurations.

<!--more-->

## The Problem

To ensure the security of web servers, the [Qualys' SSL Labs service](https://www.ssllabs.com/) is often used. It runs a comprehensive test on various aspects of the TLS configuration of a web server on-demand. The service then derives a grade (e.g., "A+") from the results and shows details on potential problems found and the device/browser compatibility.

However, the Qualys service has a couple of **drawbacks**: 
 * It is not a good fit for environments where tests need to be run automatically. While Qualys provides a free API, I often ran into limitations with the API. For example, when scanning many hosts, I was often blocked by the rate limiting.
 * It is rather slow.
 * It is not suitable for scanning internal services.

There are of course free tools like [sslyze](https://github.com/nabla-c0d3/sslyze), but sslyze only finds out *how* a host is configured, not if the configuration is secure[^1] or compatible.

## TLS Profiler

To enable an **automated** testing of our servers at [yes®](https://www.yes.com/), I wrote [TLS Profiler](https://github.com/danielfett/tlsprofiler). **TLS Profiler a python package and command line tool that uses sslyze to scan a host for its TLS configuration** and compare the configuration to the [Mozilla TLS Profiles](https://wiki.mozilla.org/Security/Server_Side_TLS). 

![](/img/posts/mozilla_tls_profile.png)

These profiles contain recommendations for all aspects of the TLS configuration, from cipher suites to the maximum certificate lifetime. Three different profiles, modern, intermediate, and old, ensure compatibility with a known set of devices and browsers. 

> One **key difference** between SSL Labs and TLS Profiler is that the latter does not generate a grade. Instead, it shows you were the configuration deviates from Mozilla's profiles, in fact, **in both directions:** 
> 
> Of course it shows you when the scanned server is *less secure* than expected, for example, by having an old TLS version enabled; but it also shows you if the settings are *more secure* (but maybe less compatible) than Mozilla's recommendations, for example, if a key size is bigger than recommended.

Since all TLS scans using TLS Profiler are done from **your own device**, the only rate limiting are yours and the server's network connection and the tool is also suitable for security scans of internal networks.

You can **try the TLS Profiler tool yourself** using docker (the image is not optimized right now, so this is a rather large download, sorry!): 

```bash
docker run danielfett/tlsprofiler danielfett.de intermediate
```

TLS Profiler first runs several checks that come with sslyze. For example, it checks if the certificate (chain) presented is valid against common trust stores ("Validation Errors", "Certificate Warnings").

It then also checks for "Profile Errors", i.e., deviations from the given Mozilla profile. The profiles are downloaded from mozilla.org on every run and therefore kept up-to-date. You might see errors such as `client must choose the cipher suite, not the server (Protocol TLSv1.3)`. Where possible, the error descriptions are augmented with information that you need to fix the error, for example, `certificate lifespan too long (is 820, should be less than 730)`.

As part of his Bachelor's Thesis on the [yesses](https://github.com/danielfett/yesses) security scanner, Fabian Hauck extended TLS Profiler to cover all parameters in the Mozilla profiles. To this end, he also had to extend sslyze's features.

## Web TLS Profiler

 He also created a web interface which offers an [interface similar to Qualys'](https://tlsprofiler.danielfett.de/).

[![](/img/posts/webtlsprofiler.png)](https://tlsprofiler.danielfett.de/)

You can easily set up you own Web TLS Profiler instance using docker:

```bash
docker run -p 8000:8000 danielfett/webtlsprofiler
```

## Experience from Practice

Using TLS Profiler instead of Qualys has enabled us to find TLS misconfigurations faster and in an automated fashion. We use TLS Profiler as part of [yesses](https://github.com/danielfett/yesses) to scan for TLS bugs and many other things. 

Also, during the development of TLS Profiler, we noticed that some web servers and OpenSSL versions do not take all configuration parameters into account. That is why, even if you use [Mozilla's SSL Configuration Generator](https://ssl-config.mozilla.org/), a quick check using TLS Profiler is very useful.

[^1]: sslyze scans for specific attacks, like POODLE, but it does not grade or otherwise evaluate the TLS configuration.