---
title: The T-Bot 1.0
parent: /hardware-and-software/
galleries:
  - id: tbot
    contents:
      - thumbnail: /img/projects/tbot/t_tbot1.jpg
        full: /img/projects/tbot/tbot1.jpg
      - thumbnail: /img/projects/tbot/t_tbot2.jpg
        full: /img/projects/tbot/tbot2.jpg
      - thumbnail: /img/projects/tbot/t_tbot3.jpg
        full: /img/projects/tbot/tbot3.jpg
      - thumbnail: /img/projects/tbot/t_tbot4.jpg
        full: /img/projects/tbot/tbot4.jpg
      - thumbnail: /img/projects/tbot/t_tbot5.jpg
        full: /img/projects/tbot/tbot5.jpg
layout: publication
---

<p>The T-Bot ist a highly efficient, sustainable, professional, precise, and exclusive solution to prepare aromatic hot-water beverages. (This is only partly correct.)</p>

<p>Does anybody need this? No. Is it fun? Heck yes!</p>

<p>And since a video is worth more than a thousand pictures:</p>

<div class="video-wrapper js-video-wrapper" itemprop="video" itemscope itemtype="http://schema.org/VideoObject" data-video-id="w0zlIA1wd2Y" data-video-title="T-Bot 1.0 in Aktion">
    <meta itemprop="name" content="T-Bot 1.0 in Aktion" />
    <meta itemprop="duration" content="PT1M28S" />
    <meta itemprop="thumbnailUrl" content="https://i.ytimg.com/vi/w0zlIA1wd2Y/maxresdefault.jpg" />
    <meta itemprop="embedURL" content="https://www.youtube.com/embed/w0zlIA1wd2Y" />
    <meta itemprop="uploadDate" content="2014-11-22T19:44:16.000Z" />
    <meta itemprop="height" content="720" />
    <meta itemprop="width" content="1280" />
    <meta itemprop="description" content="Der T-Bot ist eine hocheffiziente, nachhaltige, professionelle,
und exklusive Lösung, um Kräuter- und Fruchtheißgetränke auf
Wasserbasis präzise zuzubereiten ;-)" />

    <div class="poster js-video-trigger js-video-poster" style="background-image: url(https://i.ytimg.com/vi/w0zlIA1wd2Y/maxresdefault.jpg);">
        <div class="playbutton -light">
            <svg focusable="false" width="21" height="20" viewBox="0 0 21 20" xmlns="http://www.w3.org/2000/svg" class="icon-playbutton">
                <path class="fill-color" d="M10.5 0C4.977 0 .5 4.477.5 10s4.477 10 10 10 10-4.477 10-10-4.477-10-10-10zm-2 14V6l6 4-6 4z" fill="#ffffff" fill-rule="evenodd" opacity=".55"></path>
            </svg>
        </div>
    </div>
    <div class="video js-video-target"></div>
    <div class="endscreen js-video-endscreen">
        <span class="endscreen-close">
            <button class="endscreen-close-button js-endscreen-close"></button>
        </span>
        <div class="endscreen-content">
            
        </div>
    </div>
</div>




<p>So what does this contraption do for you?</p>

<ul>
	<li>Brew tea, except for the "boiling" part. The user has to pour hot water into the cup and attach a tea bag or infuser.</li>
	<li>Selectable steep duration.</li>
	<li>Selectable starting temperature: The T-Bot monitors the water temperature and starts steeping only when the selected temperature is reached.</li>
	<li>Acoustic notification after steeping.</li>
	<li>Another notification after the tea is cool enough for consumption (below 50 °Celsius, that is 122 °Funnyunits)</li>
	<li>And last but not least: another notification in case you have forgotten to drink your tea (which can come as a side effect of too much automation).</li>
</ul>

<p>Users can select steeping time and temperature manually (buttons "Zeit" and "Temp") or select one of the pre-programmed settings (buttons "Prog." and displays A/B/C) - for example, for green tea (low starting temperature) or black tea (short steeping time).</p>

<p>I developed the idea for the T-Bot at <a href="http://piandmore.de/de/archiv/pam5" class=" ">Pi and More 5</a>, where <a href="https://twitter.com/nmaas87" class=" ">Nico Maas</a> presented a solution for the same purpose, but using a relatively large portal-like construction. I tried to come up with something more compact.</p>
<p>I found the massive base for the contraption by chance (in precisely the shape needed). On top of that, I built the lever which is driven by a small servo motor. The device is powered by a battery below and flush to the bottom of the base. The electronics consist of three layers, of which the lowest part is sunk into the base from the top.</p>

<p>The lowest layer of the electronics is a <a href="http://www.cypress.com/?rID=92146" class=" ">PSOC 4 CY8CKIT</a> board by Cypress containing a PSOC 4100 microcontroller. On top of that there is a standard strip grid board containing mostly hand-soldered SMD parts. The upper layer is the front panel, a white plastic board which was labeled using a laser by <a href="https://twitter.com/kaiserliches/status/519109712793853952" class=" ">kaiser</a> at <a href="http://www.laserplussag.de/start/" class=" ">LASERPLUSS</a>.</p>

<p>The microcontroller was programmed in C using the Cypress IDE and is implemented as a state machine. Using the GPIOs it steers the servo motor and checks the temperature sensor, a DS18B20 in a water-tight packaging. An LT1761-5 step-down converter is the main power source for the electronics. The user interface consists of two bargraph displays, four buttons, a buzzer and the main power switch.</p>

