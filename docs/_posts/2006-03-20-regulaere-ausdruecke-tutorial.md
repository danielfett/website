---
title: Reguläre Ausdrücke
type: Tutorial
layout: publication_toc
redirect_from: 
  - /de/tutorials/tutorial-regulare-ausdrucke/
  - /en/tutorials/tutorial-regulare-ausdrucke/
---

<p class="intro">"Reguläre Ausdrücke" sind eine Art Sprache, die beim Programmieren für diverse Problemlösungen verwendet werden kann, insbesondere dann, wenn es darum geht, Zeichenketten (Strings) zu bearbeiten, zu prüfen oder in ihnen etwas zu suchen.</p>

<p>Und weil der Name "Reguläre Ausdrücke" etwas unhandlich ist, heißen die "Regular Expressions" auch oft einfach nur "RegEx(en)".</p>

<h2 id="Einfhrung">Einführung</h2>

<p>Hier gibts ein kleines Tutorial zu diesen esoterisch anmutenden aber unglaublich mächtigen Zeichenketten, die beim unbedarften Betrachter Assoziationen eines kleinen Kindes und dessen ersten Versuchen an der Tastatur auslösen.</p>

<p><strong>Was sind reguläre Ausdrücke?</strong> Wie gesagt, können mit regulären Ausdrücken Zeichenketten auf eine bestimmte Zusammensetzung geprüft werden, wie dies z.B. bei Anwendungen wichtig ist, die Eingaben eines Benutzers erwarten.</p>

<p>Beispiele:</p>

<ul>
	<li>Schulnote</li>
	<li>Postleitzahl</li>
	<li>E-Mail-Adresse</li>
	<li>Bestellnummern</li>
</ul>

<h3 id="KonkreteAnwendung">Konkrete Anwendung</h3>

<p>Populäre Stellen, an denen man auf reguläre Ausdrücke stoßen kann und an denen du dieses Wissen anbringen kannst:</p>

<ul>
	<li>Web-Anwendungen (z.B. in PHP, Perl)</li>
	<li>Unix-Skripte</li>
</ul>

<p>Im Folgenden wird davon ausgegangen, dass du eine entsprechende Stelle vorliegen hast und dich bereits informiert hast, wie reguläre Ausdrücke in der Umgebung deiner Wahl verwendet werden. In PHP geschieht dies z.B. mit den Funktionen <a href="http://www.php.net/preg_match" target="_blank"> preg_match</a> (Prüfen von Strings, finden von Zeichenketten) und <a href="http://www.php.net/preg_replace" target="_blank"> preg_replace</a> (Ersetzen von Zeichenketten).</p>

<p>Am besten testest du deinen Ausdruck zuerst "auf dem Trockenen". Dazu kannst du ein Onlinetool wie <a href="https://regex101.com/" class=" ">regex 101</a> oder den <a href="http://www.weitz.de/regex-coach/" target="_blank"> Regex-Coach</a> benutzen.</p>

<h3 id="GuterStil">Guter Stil</h3>

<p>Oft wirst du feststellen, dass es zu einem Problem viele verschiedene Lösungen gibt. Dabei stehen sich dann gegenüber</p>

<ul>
	<li><span class="div"><strong>Eine <em>genaue</em> Lösung und eine <em>allgemeinere</em>.</strong> Besteht die Gefahr, dass die genaue Lösung zu "restriktiv" ist (und damit vielleicht ein Benutzer frustriert aufgibt, wenn seine richtige Eingabe nicht akzeptiert wird), nimm lieber die allgemeine. Ist das Problem aber sehr "eindeutig", nimm lieber die genaue. </span></li>
	<li><span class="div"><strong>Eine <em>genaue</em> Lösung und eine <em>schnelle</em>.</strong> Lange reguläre Ausdrücke können viel Zeit für die Verarbeitung in Anspruch nehmen. Auch hier musst du abwägen, was dir wichtiger ist. Es könnte Benutzer ärgern, wenn die Prüfung einer Eingabe sehr lange dauert. </span></li>
	<li><span class="div"><strong>Eine <em>einfache</em> Lösung und eine <em>"elegante"</em>.</strong> Du kannst in 10 Zeichen ausdrücken, was andere nicht in 60 schaffen? Prima, aber denk dran dass du vielleicht später nochmal was ändern willst! Und das kann schwerer werden, als man denkt. Daher nimm lieber die einfachere Variante oder kommentiere komplizierte Ausdrücke. </span></li>
</ul>

<h3 id="Probleme">Probleme</h3>

<p>Wenn dein regulärer Ausdruck Probleme macht, du dir aber ziemlich sicher bist dass er richtig ist, schau dir zunächst mal weiter unten die <a href="#SpezielleZeichenWeitereZeichen">Sonderzeichen</a> an und was man mit ihnen machen muss, um sie zu benutzen. Dabei sind Sonderzeichen schon so "banale" Sachen wie ein Punkt.</p>

<p>Außerdem solltest du ihn dringend im o.g. RegEx-Coach testen! Dieser fördert manchmal geradezu unglaubliche irreguläre Verhaltensweisen zutage ;-)</p>

<p>Dann darfst du als nächstes Google benutzen ;-) Da findet man sehr viele Informationen, viele Vorlagen um diverse Problemstellungen regulär auszudrücken und auch die Google-Groups sind immer hilfreich.</p>

<h3 id="Konventionen">Konventionen</h3>

<p>In diesem Tutorial werden folgende Farben für Texte (Strings) verwendet: <code class="block">Regulärer Ausdruck, den du theoretisch so verwenden kannst, mit<br>
<span class="new">markierten neuen Teilen</span><br>
<span class="wrong">Absichtlich fehlerhafter Code</span> </code> Öfters verwende ich mal den Programmierern nicht fremden "String" (ich spar mir den Unterwäsche-Witz) für ein Textstück. Außerdem gilt: ein Ausdruck "trifft" = "beschreibt einen Text genau" = "erledigt die gewünschte Funktion" = "matcht" = "frisst (etwas)"</p>

<h2 id="EinfacheAusdrcke">Einfache Ausdrücke</h2>

<p> </p>

<h3 id="EinElementigeregulreAusdrcke">Ein-Elementige reguläre Ausdrücke</h3>

<p>Fangen wir mal klein an. Wir wollen prüfen, ob eine Eingabe einer Schulnote von 1-6 entspricht. <code class="block"><span class="new">[123456]</span> </code> erledigt das für uns. Du siehst: in eckigen Klammern folgt eine Auflistung von Zeichen, die erlaubt sind. Insgesamt steht der gesamte geklammerte Ausdruck aber nur für ein Zeichen: 1 <em>oder</em> 2 <em>oder</em> ... <em>oder</em> 6.</p>

<p>Da unsere Zahlen von 1 bis 6 so schön aufeinanderfolgen, können wir auch schreiben <code class="block"><span class="new">[1-6]</span> </code> was die Sache etwas übersichtlicher macht. Genau so könnte man z.b. prüfen, ob eine Eingabe einem Gleis auf einem Bahnhof entspricht: <code class="block"><span class="new">[1-9]</span> </code> für einen Bahnhof mit 9 Gleisen. Auf unserem Bahnhof sei heute Gleis 4 gesperrt, also als Eingabe nicht erlaubt: <code class="block">[1-3<span class="new">5-9</span>] </code> Wir haben den Eingabebereich also aufgeteilt in zwei Bereiche 1-3 und 5-9. Du siehst: Die beiden Bereiche werden einfach hintereinander geschrieben. Das ist am Anfang gewöhnungsbedürftig (intuitiv möchte man vielleicht ein Leerzeichen machen), aber das wird uns noch öfter begegnen.</p>

<h3 id="MehrelementigeregulreAusdrcke">Mehrelementige reguläre Ausdrücke</h3>

<p>Was ist, wenn auf unserem Bahnhof jetzt angebaut wird? Sagen wir, er wird auf 12 Gleise erweitert: <code class="block"><span class="wrong">[1-12]</span> </code> (Gleis 4 sei wieder geöffnet ;-) ). <strong>Aber Vorsicht, hier ist ein Fehler drin!</strong></p>

<p>Wie oben erwähnt, steht der <em>gesamte</em> Ausdruck in den eckigen Klammern nur für <em>ein</em> Zeichen. "12" enthält aber zwei Zeichen. Der Code oben wird nicht funktionieren: Er bedeutet "1 bis 1" <em>oder</em> "2". Den Umgang mit Bahnhöfen mit mehr als 9 Gleisen demonstrieren wir später.</p>

<p>Für den Moment wollen wir etwas anderes Prüfen: Bahnsteige 1-9 haben noch jeweils Abschnitt "a" und "b". Wir wollen also auf 1a,1b,2a,...,9a,9b prüfen: <code class="block">[1-9]<span class="new">[ab]</span> </code> Will heißen: Eine Zahl 1-9 gefolgt von einem Buchstaben a oder b.</p>

<p>Mehrere rechteckige Klammern entsprechen also mehreren Zeichen. Soll ein Ausdruck mehrere Zeichen beschreiben, werden diese einfach hintereinander gehangen. Dann wird die Eingabe von links nach rechts mit deinem Ausdruck verglichen.</p>

<p>Selbstverständlich müssen auch nicht immer alle Buchstaben aufgeführt werden: <code class="block">[1-9][<span class="new">a-d</span>] </code> trifft jetzt auch z.B. 4d.</p>

<p>Zu beachten ist, dass Groß- und Kleinschreibung getrennt behandelt wird. Eine sinnvolle Erweiterung wäre also z.B. <code class="block">[1-9][a-d<span class="new">A-D</span>] </code></p>

<h3 id="Optionen">Optionen</h3>

<p>Schauen wir uns die Eingabe einer Hausnummer an. Diese können aus einer oder mehreren (bis zu 3) Ziffern bestehen und ein a-z am Ende haben. Müssen aber nicht. <code class="block">[1-9][0-9]<span class="new">?</span>[0-9]<span class="new">?</span>[a-z]<span class="new">?</span> </code> Das Fragezeichen hinter einem Element (und [1-9] ist <em>ein</em> Element!) besagt: Das vorhergehende Element <em>kann</em> vorkommen, muss aber nicht.</p>

<p>Der letzte Code heißt also: Eine Ziffer (1-9), optional zwei weitere Ziffern (0-9), optional ein Buchstabe.</p>

<p>Stellt man sich solch eine Konstruktion mit z.B. 10 Ziffern vor, kann man sich leicht ausmalen, dass sie schnell sehr lang wird. Daher gibt es eine andere Schreibweise, wenn man ein Element mehr als ein mal erlauben will: <code class="block">a<span class="new">{1,3}</span>h </code> Trifft auf "ah" genau so wie auf "aaah". Die Angabe in Klammern steht also für die {minimale, maximale} Anzahl an Zeichen. Daher können wir unsere Hausnummern auch so formulieren: <code class="block">[1-9][0-9]<span class="new">{0,2}</span>[a-z]? </code> und dann auch ohne Probleme für längere Straßen (USA ;-) ) umschreiben: <code class="block">[1-9][0-9]<span class="new">{1,4}</span>[a-z]? </code> erlaubt jetzt auch Hausnummern im fünfstelligen Bereich, fordert aber mindestens eine zweistellige (beachte die Änderung vor dem Komma).</p>

<p>Eine Konstruktion wie <code class="block">[0-9]<span class="new">{5}</span> </code> (also eine Klammer mit nur einer Angabe) verlangt eine genau x-malige Wiederholung des davorstehenden Ausdrucks. In unserem Fall 5 mal: Dieser reguläre Ausdruck wäre geeignet, um (deutsche) Postleitzahlen zu prüfen.</p>

<p>Wir könne auch ein "mindestens" ausdrücken: <code class="block">[0-9]<span class="new">{3,}</span> </code> fordert mindestens 3 Ziffern.</p>

<h3 id="BeliebigeWiederholungen">Beliebige Wiederholungen</h3>

<p>Bisher mussten wir immer wissen, wieviele Zeichen gefunden werden sollen. Es gibt aber durchaus Fälle, in denen sich ein Zeichen beliebig oft wiederholen darf.</p>

<p>Schauen wir uns die Prüfung von Telefonnummern an. Wenn man einen regulären Ausdruck schreibt, empfiehlt es sich oft, zunächst einmal zu notieren, auf was dieser alles treffen soll. Unsere Telefonnummern sollen von diesem Format sein dürfen:</p>

<ul>
	<li>0651/55541-36</li>
	<li>0049 160 555678</li>
	<li>0180.23.555.63</li>
</ul>

<p>Es können neben Zahlen also auch Bindestriche, Querstriche, Leerzeichen und Punkte vorkommen. <em>Ein</em> gültiges Element wäre also <code class="block"><span class="wrong">[0-9/. -]</span> </code> (Also: Dieses <em>eine</em> Zeichen besteht aus einer Zahl zwischen 0 und 9 <em>oder</em> einem Slash <em>oder</em> einem Punkt <em>oder</em> einem Leerzeichen <em>oder</em> einem Minus.) Doch Vorsicht! Wie du siehst, kommen in den Klammern zwei Bindestriche vor: ein mal in einer speziellen Funktion, um einen Zahlenbereich anzudeuten und ein mal als "echter" Bindestrich, der so auftauchen darf. Um Verwechslungen auszuschließen müssen wir letzteren maskieren, also zeigen dass er hier keine spezielle Funktion hat. Das geht mit einem vorangestellten Backslash: <code class="block">[0-9/. <span class="new">\</span>-] </code> Und dann wollen wir ja noch mitteilen, dass diese Zeichen beliebig oft vorkommen dürfen: <code class="block">[0-9/. \-]<span class="new">+</span> </code> Das Plus bedeutet: ein oder mehrmals das davor befindliche Zeichen, also mindestens ein mal. Wollen wir auch eine leere Telefonnummer zulassen (der Mathematiker würde sagen: Die Nullnummer), so gibt es dazu ein anderes Zeichen: <code class="block">[0-9/. \-]<span class="new">*</span> </code> trifft jetzt auch auf "" (leere Zeichenkette) und natürlich unsere Telefonnummern.</p>

<p>Dieser Ausdruck ist jetzt natürlich ein sehr allgemeiner Ausdruck (siehe die Diskussion oben). Er erlaubt auch Telefonnummern, die offensichtlich nicht korrekt sind, wie <code class="block">--..//123 </code> Möchte man das weiter einschränken, muss man einen komplizierteren Ausdruck entwickeln.</p>

<p>Also nochmal zusammengefasst: Das + steht für eine mindestens einmalige Wiederholung. * heißt: keinmal oder beliebig oft.</p>

<h3 id="Platzhalter">Platzhalter</h3>

<p>Gehen wir zu einem anderen Beispiel über: Wir möchten in einer Bibliothek nach einem Autor suchen, wissen aber nicht, ob er evtl. einen zweiten Vornamen hat. Nach dem Vornamen können also <strong>beliebige Zeichen</strong> kommen und danach dann erst der Nachname. Eine mögliche Lösung sieht so aus: <code class="block">Marius <span class="new">.</span>*Osterhase </code> Die im Einzelnen bedeutet: "Marius", danach ein Leerzeichen gefolgt von einem beliebigen Zeichen (dafür steht der Punkt!) beliebig oft (also evtl. auch gar keins) und anschließend der Nachname. Das trifft auf "Marius Osterhase" genau so wie auf "Marius Müller Osterhase".</p>

<p>Genau so kann man dem Punkt natürlich auch ein Plus folgen lassen, um mindestens ein beliebiges Zeichen zu fordern.</p>

<p>Der Punkt "frisst" normalerweise zwar fast alles, aber keine Zeilenumbrüche. Wie du ihn dazu bringst, findest du unter <a href="#Modifikatoren">Modifikatoren</a>.</p>

<p>Dem "aufmerksamen Leser" wird nicht entgangen sein, dass wir oben auch schon einen Punkt hatten, und zwar innerhalb der eckigen Klammern. Wie bei <strong>vielen</strong>, aber nicht allen Sonderzeichen müssen diese zwar außerhalb von eckigen Klammern als solche maskiert werden (Backslash davor), aber nicht innerhalb.</p>

<h3 id="Zeichenklassennegieren">Zeichenklassen negieren</h3>

<p>Angenommen wir wüssten den zweiten Vornamen des Autors nicht genau, aber können uns daran erinnern, dass er kein q und kein z enthält. Auch kein Problem: <code class="block">Marius <span class="new">[^</span>qz<span class="new">]+</span> Osterhase </code> verlangt nach einem zweiten Vornamen (deswegen das Plus) und lässt dazu ein beliebiges Zeichen zu, das <strong>nicht</strong> q oder z ist. Das ^ negiert also eine Zeichenklasse und gilt genau bis zur schließenden Klammer.</p>

<h3 id="Klammern">Klammern</h3>

<p>Klammern können dazu benutzt werden, längere Ausdrücke zu einem Element zusammenzufassen und es damit zu ermöglichen, das oben gelernte auch auf Teilausdrücke anzuwenden: <code class="block">Marius <span class="new">(</span>Müller <span class="new">)?</span>Osterhase </code> trifft genau auf "Marius Müller Osterhase" oder "Marius Osterhase" und auf nichts anderes: Das Fragezeichen bezieht sich - dank der Klammern - auf den kompletten zweiten Vornamen und das folgende Leerzeichen.</p>

<p>Ebenso lässt sich schreiben: <code class="block">Ba<span class="new">(</span>na<span class="new">)*</span>ne </code> Was jetzt sowohl für dieses gelbe Ding als auch z.B. für "Banananane" steht. Auch hier lässt sich die Notation mit den geschweiften Klammern anwenden: <code class="block">Ba<span class="new">(</span>na<span class="new">){2,5}</span>ne </code> was jetzt natürlich eine entsprechend andere Bedeutung hat.</p>

<h3 id="Alternativen">Alternativen</h3>

<p>Mit Klammern kann man aber auch noch andere Sachen machen, z.B. Alternativen zu einem Teilausdruck angeben: <code class="block">Das Wetter ist <span class="new">(</span>toll<span class="new">|</span>richtig schlecht<span class="new">)</span> </code> In diesem Beispiel dürfen als letzte Worte "toll" <em>oder</em> "richtig schlecht" vorkommen, aber nicht beide.</p>

<h3 id="Modifikatoren">Modifikatoren</h3>

<p>In allen RegEx-Varianten kannst du sogenannte Modifikatoren setzen und damit das genaue Verhalten des Ausdrucks kontrollieren. In Java kannst du dies z.B. bei der Konstruktion eines matcher-Objektes erledigen, bei PHP hat ein regulärer Ausdruck immer die Syntax <code class="block">[Begrenzungszeichen][RegEx][Begrenzungszeichen][Modifikator(en)] </code> also z.B. <code class="block">/(Mein|Ausdruck)/im </code> Dabei sind die Slashes die Begrenzungszeichen (andere sind hier denkbar, z.B. ~), und "i" und "m" in diesem Fall Modifikatoren. Gängige Modifikatoren sind unter anderem:</p>

<ul>
	<li><strong>i</strong> Case-Insensitivity (die Nichtbeachtung von Groß- und Kleinschreibung) einschalten</li>
	<li><strong>s</strong> Punkt wird multilinefähig: Der Punkt frisst auch Zeilenumbrüche, dies ist standardmäßig nicht so.</li>
	<li><strong>m</strong> Zeilenmodus: Die Zeichen ^ und $ matchen auch auf Zeilenanfänge bzw. -enden. Ohne den Modifikator passen sie nur auf Anfang und Ende der gesamten Zeichenkette.</li>
</ul>

<p>Modifikatoren beziehen sich immer auf den ganzen Ausdruck und sind daher eine leicht übersehene Fehlerquelle.</p>

<h2 id="KompliziertereAusdrcke">Kompliziertere Ausdrücke</h2>

<h3 id="Verschachtelungen">Verschachtelungen</h3>

<p>Selbstverständlich dürfen auch diverse Klammern ineinander geschachtelt werden, wie z.B. in folgendem Ausdruck: <code class="block">(VW (Golf|Polo)|Fiat (Punto|Panda)) </code> welcher auf "VW Golf", "VW Polo", "Fiat Punto" und "Fiat Panda" trifft. Dies ermöglich zwar recht kurze Ausdrücke für lange Zeichenketten, kann aber auch viel Zeit zur Verarbeitung in Anspruch nehmen.</p>

<p>Genau so lassen sich auch diese Alternativen wiederholen: <code class="block">(10|01)<span class="new">+</span> </code> Beschreibt eine Folge aus Nullen und Einsen, in der maximal 2 Nullen oder Einsen aufeinander folgen. (Falls das jetzt nicht direkt klar wird: einfach mal überlegen, was man aus "10" und "01" zusammensetzen kann.)</p>

<h3 id="GierigeAusdrcke">Gierige Ausdrücke</h3>

<p>Ein Beispiel aus der Praxis: Der folgende, etwas längerer Code soll uns aus einer HTML-Datei die Links bzw. deren Zieladressen heraussuchen. Ein Link in einem HTML-Quellcode hat i.d.R. ein Format wie dieses: <code class="block">&lt;a href="[...Zieladresse...]" [...weitere Angaben...]&gt; </code> z.B. <code class="block">&lt;a href="http://www.example.org/" target="_blank"&gt; </code> Ein möglicher Ausdruck dafür ist recht schnell gefunden: <code class="block"><span class="wrong">&lt;a href=".*".*&gt;</span> </code> Sieht gut aus, klappt aber nicht. Warum?</p>

<p>Der Autor hat sich zwar <em>gedacht</em> der Ausdruck würde an der zu dem Link gehörenden schließenden Klammer aufhören, er tut es aber nicht. Im folgenden ein Ausschnitt aus einer HTML-Datei mit markiertem Treffer: <code class="block">&lt;BODY&gt; Bla Blubb 1 2 3 <span class="match">&lt;a href="http://www.example.org/" target="_blank"&gt; Linktext &lt;/a&gt; Viel, viel weiterer &lt;i&gt;Text&lt;/i&gt;</span> Blubb 42 </code> Das geht eindeutig zu weit! Der zweite Punkt ist zu "gierig" und frisst alle Zeichen sogar über mehrere schließende spitze Klammern hinweg. In anderen Situationen wäre es denkbar, dass der erste Punkt ähnlich amokläuft.</p>

<p>Für unseren Fall gibt es zwei Lösungsmöglichkeiten. Oft bleibt jedoch nur eine davon, daher stelle ich beide vor:</p>

<ul>
	<li><span class="div"><strong>Den Punkt ersetzen</strong> durch etwas was keine spitzen Klammern mehr frisst: <code class="block"><span class="wrong">&lt;a href=".*"[^&gt;]*&gt;</span> </code> Das ist eine oft anzuwendende Methode (überlege dir, welche Zeichen das Ende markieren und schließe diese von dem zu treffenden aus). Das ganze muss jetzt natürlich noch analog für den ersten Punkt gemacht werden: <code class="block">&lt;a href="<span class="new">[^"]</span>*"<span class="new">[^&gt;]</span>*&gt; </code> </span>

	<p> </p>
	</li>
	<li><span class="div"><strong>Den Punkt "umerziehen"</strong> (bzw. * genügsam machen) so dass beide zusammen nur noch so viel fressen, wie unbedingt nötig ist. Dies tut ein angehängtes Fragezeichen, was dann natürlich nicht mehr die bisher bekannte Funktion hat: <code class="block">&lt;a href=".*<span class="new">?</span>".*<span class="new">?</span>&gt; </code> Natürlich funktioniert diese Sonderbenutzung des Fragezeichens auch hinter einem Pluszeichen.</span></li>
</ul>

<h3 id="Gruppen">Gruppen</h3>

<p>So gut wie alle RegEx-Dialekte erlauben das Bilden von Gruppen und deren Speicherung für spätere Verwendung. Auch dazu können Klammern dienen.</p>

<p><strong>Spätere Verwendung</strong> kann z.B. heißen, dass ein Ausdruck zwar auf eine längere Zeichenkette treffen soll, aber nur ein Teil davon wirklich verwendet werden soll.</p>

<p>Soetwas wäre in Verbindung mit dem obigen Ausdruck sehr nützlich, um alle Zieladressen aus einer HTML-Seite zu filtern.</p>

<p>Wie genau du an die Inhalte der Gruppen kommst, steht in der Anleitung der von dir verwendeten Sprache. Bei PHP findest du es z.B. bei <a href="http://www.php.net/preg_match" target="_blank"> preg_match</a> und Java soweit ich mich erinnern kann irgendwo in der Nähe von regex.matcher. Google sollte da mehr zu wissen. <code class="block">&lt;a href="<span class="new">(</span>.*?<span class="new">)</span>".*?&gt; </code> Der erste Punkt und seine "Vervielfacher" sind eingeklammert. In der ersten Gruppe befindet sich jetzt also die URL.</p>

<p>Beachte, dass bei der Nummerierung der Gruppen die Reihenfolge der öffnenden Klammer zählt. Das ist wichtig zu beachten bei verschachtelten Klammern. Außerdem zählen normalerweise <strong>alle Klammern</strong>, auch wenn sie nur zur Ausweisung von Alternativen (s.o.) verwendet werden.</p>

<h3 id="Referenzen">Referenzen</h3>

<p>Es gibt noch einen anderen, sehr nützlichen Verwendungszweck für Gruppen. Stell dir vor, du willst in einer Folge von Zahlen (sagen wir sie seien mit einem Leerzeichen voneinander getrennt) all die Zahlen finden, die mit der selben Ziffer beginnen und enden.</p>

<p>Wir haben also <code class="block">129 337873 78324 43938 9388 824998 349734 </code> Dazu können wir solch einen Ausdruck verwenden: <code class="block"> <span class="new">(</span>[0-9]<span class="new">)</span>[0-9]*<span class="new">\1</span> </code> wobei das \1 auf den Inhalt der <em>ersten Klammer</em> verweist (referenziert) und daher an der Stelle von \1 das selbe stehen muss wie in dieser Klammer. Das erste und letzte Zeichen <em>unseres Ausdrucks</em> ist jeweils ein Leerzeichen, um damit das Ende und den Anfang einer Zahl zu kennzeichnen.</p>

<p>Schauen wir uns an, auf was er trifft: <code class="block">129<span class="match"> 337873 </span>78324 43938 9388<span class="match"> 824998 </span>349734 </code> Wie du siehst, zählt das erste und letzte Leerzeichen auch immer noch zu dem jeweiligen Treffer dazu. Das ist auch kein Wunder, schließlich steht vor und hinter unserem Ausdruck auch jeweils ein Leerzeichen. Das ist nicht wirklich gut, wenn uns dieses Leerzeichen eigentlich gar nicht interessiert. Daher stellt die RegEx-Sprache auch hier ein Mittel zur Verfügung, welches auch funktioniert, wenn wir keine Gruppen benutzen möchten oder können:</p>

<h3 id="SpezielleZeichenWortgrenzen">Spezielle Zeichen: Wortgrenzen</h3>

<p>Es gibt Zeichen, die stehen zwar im regulären Ausdruck, aber nicht in dem Text, der nachher gematcht wird. Das sagt dir jetzt nichts? Naja, schauen wir uns als ein Beispiel an, wie man obigen Ausdruck ohne die Leerzeichen schreibt: <code class="block"><span class="new">\b</span>([0-9])[0-9]*\1<span class="new">\b</span> </code> Dieses "\b" ist ein zusammengehöriges Element und kennzeichnet ein Wortanfang oder ein Wortende (also eine Wortgrenze). Kennst du die in Textverarbeitungsprogrammen und Editoren oft verwendete Möglichkeit "Nur ganzes Wort suchen" in der Suchfunktion? Wählst du diese aus, werden z.B. bei einer Suche nach "Kai" statt diesen Treffern <code class="block"><span class="match">Kai</span> fährt nach<br>
<span class="match">Kai</span>serslautern </code> nur noch dieser Treffer gefunden: <code class="block"><span class="match">Kai</span> fährt nach<br>
Kaiserslautern </code> Letzteres ließe sich in regulären Ausdrücken so umsetzen bzw. ausdrücken: <code class="block"><span class="new">\b</span>Kai<span class="new">\b</span> </code> Also "Kai" nur, wenn es von Wortgrenzen umgeben ist. Was genau ist überhaupt eine Wortgrenze? Eine Wortgrenze tritt zwischen einem Wort-Zeichen und einem Nichtwortzeichen auf. Hä? (Erklärung folgt!)</p>

<h3 id="SpezielleZeichenWeitereZeichen">Spezielle Zeichen: Weitere Zeichen</h3>

<p>Es gibt - Überraschung! - noch mehr Sonderzeichen, die du verwenden kannst und die einen RegEx schön abkürzen können. Diese bestehen immer aus einem Backslash gefolgt von einem weiteren Zeichen (Buchstaben). Übrigens steht ein großer Buchstabe dabei immer für das Gegenteil eines kleinen. <code class="block">\w  \W </code> Ein Wort-Zeichen (kleines w) steht genau für [a-zA-Z0-9] und ein Nichtwortzeichen (großes W) steht genau für alles andere, also [^a-zA-Z0-9]. <code class="block">\d  \D </code> Ein Digit, also eine Ziffer von 0-9. Entspricht damit [0-9] und in der Großschreibung [^0-9]. <code class="block">\b  \B </code> Die "kleine" Variante hast du ja oben schon kennengelernt. Ein großes B steht dementsprechend für alle Stellen, an denen keine Wortgrenze auftritt. <code class="block">\s  \S </code> Die Kleine Variante steht für alle Whitespaces: Das sind so gut wie alle Zeichen, die man nicht sieht. Also Return (bzw. Enter), Leertaste (Space), Tab(ulator). <code class="block">\\ </code> Wenn man mit Backslash, wie du gesehen hast, Sonderzeichen anfängt, muss man ja auch den Backslash selbst irgendwie fabrizieren können, wenn man genau diesen meint. Dies macht man einfach durch einen doppelten solchen. Man sagt: der erste "maskiert" den zweiten. <code class="block">\.  \+  \*  \(  \)  \[  \]  \-  \$  \| </code> Der Punkt und viele andere Zeichen haben, wie du oben gesehen hast, eine Sonderfunktion. Daher werden sie mittels eines Backslashs von dieser Sonderfunktion abgehalten ("maskiert"). Dies gilt für das Minuszeichen nur innerhalb von Zeichenklassen, dafür darfst du in selbigen bei vielen anderen Zeichen die Backslashs weglassen.</p>

<h3 id="AnfangsundEndezeichen">Anfangs- und Endezeichen</h3>

<p>Stell dir vor, du willst ein Datum prüfen, sagen wir mit <code class="block">1\.3\.2004 </code> Und diesen Ausdruck lässt du auf <code class="block">11.3.2004 </code> los. Was kommt raus? Dein Ausdruck wird dir melden, dass er trifft. Ist ja auch irgendwo klar, schließlich steht, wenn man eine Eins weglässt, dein Datum da. Du willst aber, dass das gesamte Datum wie deins aussieht? Gibt's da nicht was von Ratiodingsbums? Doch gibts: <code class="block"><span class="new">^</span>1\.3\.2004<span class="new">$</span> </code> Dieses Dach am Anfang sagt: Treffe nur, wenn hier der zu durchsuchende String anfängt. Und das Dollarzeichen steht für: Treffe nur, wenn genau hier der zu durchsuchende String endet.</p>

<p>Selbstverständlich kann man beide auch einzeln einsetzen; Als Beispiel schauen wir uns zwei reguläre Ausdrücke an: Der erste trifft auf einen String, der mit einer Zahl endet. Der zweite trifft auf einen String, der mit einer öffnenden Klammer beginnt. Dabei benutzen wir die oben angegebene Maskierung für die Klammer. <code class="block">\d<span class="new">$</span><br>
<span class="new">^</span>\( </code></p>

<h3 id="PositiveLookaheadsundLookbehinds">Positive Lookaheads und Lookbehinds</h3>

<p>Du hast jetzt Möglichkeiten kennengelernt, wie du Wortgrenzen feststellen kannst, ohne sie selbst wirklich mitzufressen. Es gibt auch eine universelle Möglichkeit.</p>

<p>Als Beispiel soll folgende Zahlenfolge dienen: <code class="block">000566403580000345050052301078906040092800100001007680 </code> Aus dieser Zahlenfolge sollen alle jene Folgen herausgefischt werden, die drei Ziffern ungleich Null enthalten und von einer Null an jeder Seite begrenzt werden. In unserem Fall also "358", "345", "523", "789", "928" und "768". Dazu kannst du folgenden Code benutzen: <code class="block"><span class="new">(?&lt;=0)</span>[1-9]{3}<span class="new">(?=0)</span> </code> Keine Panik! Zur Erklärung, und wir fangen in der Mitte an: das [1-9]{3} sollte klar sein (3 Ziffern ungleich Null). Davor findest du die Klammer (?&lt;=0). Die Zeichen ?&lt;= musst du "en bloc" betrachten und sie kennzeichnen eine Sonderfunktion für die Klammer. Diese steht damit für "vornedran eine Null". Und weil "vornedran" in der normalen Leserichtung der westlichen Welt bedeutet, dass die Klammer "rückwärts" schaut, heißt diese Funktion "positive lookbehind".</p>

<p>Genauso mit den Zeichen "?=", diese weisen der Klammer die Sonderfunktion "hintendran muss ... kommen" zu, in unserem Fall also "hintendran eine Null". Das ganze nennt sich "positive lookahead", weil die Klammer "nach vorne" schaut.</p>

<p>Unser "\b"-Beispiel von oben könnten wir also auch folgendermaßen ausdrücken, wenn wir unser Wissen über "\W" benutzen: <code class="block"><span class="new">(?&lt;=\W)</span>(\d)\d*\1<span class="new">(?=\W)</span> </code> Zur Erklärung fangen wir wieder in der Mitte an: Da steht der von oben bekannte Code (Eine Ziffer, beliebig viele weitere Ziffern und eine weitere Ziffer, die die gleiche wie die erste ist). Die allererste Klammer fordert vor der ersten Ziffer ein Nichtwortzeichen und die allerletzte Klammer ein Nichtwortzeichen hinter der letzten Ziffer.</p>

<p>Selbstverständlich können lookaheads und lookbehinds auch einzeln in einem regulären Ausdruck vorkommen und sogar mehrfach. Das einzige, was <em>nicht</em> geht, ist ein lookbehind mit einer unbekannten Anzahl von Zeichen. (also so Dingern wie *, + und {0,4})</p>

<p>Alles klar? Wenn nicht, dann zurück zum Anfang dieses Abschnitts, gehe nicht über "Los" und ziehe keine 200 RegExen ein.</p>

<h3 id="NegativeLookaheadsundLookbehinds">Negative Lookaheads und Lookbehinds</h3>

<p>Du hast das kompliziert gefunden und siehst so langsam ein, <strong>wie</strong> voodoo reguläre Ausdrücke sind? Es kommt noch besser.</p>

<p>Dazu noch ein Beispiel: Du willst eine E-Mail-Adresse prüfen, die aber nicht aus Frankreich stammen soll. Zunächst schauen wir uns eine einfache E-Mail-Adressen-Prüfung ohne die Einschränkung an: <code class="block">[^@]+@.+\.[^.]+ </code> (Ein Zeichen ungleich dem @-Zeichen, gefolgt von einem @-Zeichen, beliebigen Zeichen (aber mindestens eins), einem Punkt und dahinter beliebige Zeichen, aber kein Punkt mehr. Trifft auf toll@example.com genau so wie auf viele_.Zeichen@noch.mehr.Punkte.example.com.) Wichtig: das letzte Paar von eckigen Klammern frisst immer den letzten Teil (die Top-Level-Domain, im Beispiel "com") der E-Mail-Adresse.</p>

<p>Jetzt fügen wir eine Beschränkung ein und wollen "fr" an dieser Stelle ausschließen. Auf den Punkt darf also nicht "fr" folgen. <code class="block">[^@]+@.+\.<span class="new">(?!fr)</span>[^.]+ </code> erledigt das für uns. ?! kennzeichnet eine Klammer also als "hier darf <em>nicht</em> folgen".</p>

<p>Damit könnte man auch eine besondere Suche nach einem Wort gestalten. <code class="block">\bF<span class="new">(?!</span>eta\b<span class="new">)</span>.*\b </code> trifft auf alle Wörter, die mit "F" anfangen, aber ungleich "Feta" sind. Im folgenden Text sind alle Strings markiert, die getroffen werden: <code class="block"><span class="match">Fett</span> Feta <span class="match">Falsch</span> <span class="match">Feucht</span> <span class="match">Fuffziger</span> </code> Das war der "negative lookahead".</p>

<p>Und weils so schön war, leg ich noch einen drauf, den "negative lookbehind": <code class="block">.*<span class="new">(?&lt;!</span>Müll<span class="new">)</span>eimer </code> trifft auf alle Eimer, in die kein Müll gehört, meint also: "treffe an dieser Stelle, wenn davor kein "Müll" steht".</p>

<p>Ich hoffe, dieses kleine Tutorial hat dir etwas durch den Zeichendschnungel der Regulären Ausdrücke geholfen. Falls jetzt noch Fragen offen sind, empfehle ich die oben genannten Websites als Nachschlagewerke. Wenn du das Tutorial hilfreich fandest, würde ich mich auch über eine Spende freuen:</p>

<p><a href="https://paypal.me/dfett42" target="_blank"><img src="/img/paypal.png"></a></p>
