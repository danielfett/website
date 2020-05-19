---
title: Writing RFCs with Markdown
type: Howto
layout: publication
---

[RFC7749][1] defines Version 2 of "xml2rfc", an XML-based format for authoring RFCs. The xml2rfc v2 format is the preferred format for uploading RFCs to the IETF. There is also the newer [Version 3][2] of xml2rfc, but it is not yet supported for IETF RFCs. (The Version 3 XML still looks similar to Version 2 XML, but supports more features, for example, figures in enumerations.)

As far as I can see, there are **no good cross-platform editors for xml2rfc** that support highlighting, source code formatting, and a preview of the generated files. For markdown, however, all this exists!
<!--more-->

[mmark][3] is a markdown processor, written in Go, that **translates markdown files into xml2rfc** (v2 or v3). It adds a special syntax for meta information (such as the status of the RFC) and supports other features, such as including other files, which is particularly handy for long RFCs. Markdown enjoys a good support in many editors, including online editors such as the one provided by GitHub. This makes writing RFCs significantly easier.

Using mmark is straightforward:

 1. Install mmark from [GitHub][3].
 2. Start writing the RFC in markdown. [Some examples][4] are shipped with mmark.
 3. Compile to XML and then to HTML, for example with ```./mmark -2 main.md > /tmp/xml-2; xml2rfc --html /tmp/xml-2```

For the work on the OAuth 2.0 Security BCP, I split up [the source files][5] into 

 * a main.md file that contains all the metadata and references to mainmatter.md and references.md,
 * the mainmatter.md file that contains that includes a separate markdown file for each section,
 * and the references.md file that contains the references - these are still in the XML format, as required by mmark.
 
This way, the metadata and the XML for the references, both of which can confuse syntax highlighting in editors, are separated into their own files. 

I recommend reading the [mmark syntax manual][6] to learn about the features supported by mmark.

If you are interested in starting a new draft using markdown, I
recommend taking a look at the [draft-dpop][7] repository and using
that as the starting point.

**Update 2019-03-28:** Added link to dpop draft repository.

[1]: https://xml2rfc.tools.ietf.org/rfc7749.html
[2]: https://xml2rfc.tools.ietf.org/rfc7991.html
[3]: https://github.com/mmarkdown/mmark
[4]: https://github.com/mmarkdown/mmark/tree/master/rfc
[5]: https://github.com/tlodderstedt/oauth2/tree/master/draft-ietf-oauth-security-topics
[6]: https://mmark.nl/post/syntax/
[7]: https://github.com/webhamster/draft-dpop
