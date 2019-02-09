---
layout: publication
title: 'pidart: An Electronic Dart Board with Superpowers'
parent: /hardware-and-software/
galleries:
  - id: dartboard
    contents:
     - name: Connector (1)
       thumbnail: /img/projects/dartboard/t_connector.jpg
       full: /img/projects/dartboard/connector.jpg
     
     - name: Connector (2)
       thumbnail: /img/projects/dartboard/t_connector_2.jpg
       full: /img/projects/dartboard/connector_2.jpg
   
     - name: Sensor Matrix
       thumbnail: /img/projects/dartboard/t_voll.jpg
       full: /img/projects/dartboard/voll.jpg
   
---

<p>At our <a href="https://sec.uni-stuttgart.de" class=" ">research group</a> at the university, we used to play a round of darts every day during the lunch break. Initially, we used to use an cheap electronic dart board and entered the results manually into our "Dartabase" ("Dartenbank" in german). Obviously, this manual process is not very satisfying for a geek, so I created a Raspberry Pi driven electronic dart board (called, of course, "pidart"). </p>

<p>I started out from a standard electronic soft dart board and disassembled it. Then, I connected the sensors in the board and the buttons to an Arduino Mega microcontroller. The Arduino sends the dart hits and button presses on the board to the Raspberry Pi, where the pidart software runs. The Pi shows the current score and other data on a screen connected via HDMI and provides a web interface to control the software. I will provide a bit more technical background below. </p>

<img class="filer_image " alt="dartboard.png" src="/img/projects/dartboard/dartboard.png" />
<h2>Features</h2>

<p>The main feature of pidart is, of course, to keep track of the scores of each player and to enter the final results into our Dartabase. Apart from that, over the time, I added more features:</p>

<ul>
    <li>Skipping players: Sometimes, one of us takes a short break during the game or cannot attend the game from the very beginning. In this case, we can tell pidart to skip the player until he returns. The player can catch up the missed rounds later and even still win the game when the other players have checked out already (if he checks out in less rounds than them).</li>
    <li>The same feature also allows for sequential games, where each player plays a full game straight and the players play after each other.</li>
    <li>Text-to-speech: pidart uses a synthesized voice to give spoken comments for each throw of a dart.</li>
    <li>Background music: pidart plays different background music depending on the game situation. You might know that music from somewhere...</li>
    <li>Live ranking: Our Dartabase creates a ranking of the players based on the ELO system. The pidart software predicts the game's outcome during the game and shows the new Dartabase ranking.</li>
    <li>Web interface: Not only is a web browser the main GUI for pidart, it also allows for multiple clients to watch the current game in real time. Players can follow the game from anywhere (for example, on a smart phone).</li>
    <li>Post-fact editing of results: If the board registered something wrong or someone accidentally touched the board, the last frame can be edited manually.</li>
    <li>Adding and removing players dynamically: Players can leave the game (if they are allowed so by the other players ;-) ) and even join the game at any time without any disadvantage.</li>
</ul>

<h2>Video</h2>

<p>In the video, you can see the components of pidart (the Arduino and the Dartboard, and the Pi sitting under a table), and some scenes from a typical gameplay. Not shown are the "advanced" features, like skipping players. </p>

<div class="video-wrapper js-video-wrapper" itemprop="video" itemscope itemtype="http://schema.org/VideoObject" data-video-id="0lc08s65v6k" data-video-title="pidart: An Electronic Dart Board with Superpowers">
    <meta itemprop="name" content="pidart: An Electronic Dart Board with Superpowers" />
    <meta itemprop="duration" content="PT1M33S" />
    <meta itemprop="thumbnailUrl" content="https://i.ytimg.com/vi/0lc08s65v6k/maxresdefault.jpg" />
    <meta itemprop="embedURL" content="https://www.youtube.com/embed/0lc08s65v6k" />
    <meta itemprop="uploadDate" content="2014-03-17T18:35:54.000Z" />
    <meta itemprop="height" content="720" />
    <meta itemprop="width" content="1280" />
    <meta itemprop="description" content="pidart is a Raspberry Pi driven electronic dart board. For more information on the pidart project, see http://danielfett.de/privat,blog,electronic-dart-board

In this video, you can see the components of pidart (the Arduino and the Dartboard, and the Pi sitting under a table), and some scenes from a typical gameplay. Not shown are the &quot;advanced&quot; features, like skipping players." />

    <div class="poster js-video-trigger js-video-poster" style="background-image: url(https://i.ytimg.com/vi/0lc08s65v6k/maxresdefault.jpg);">
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





<h2>Some Technical Background</h2>

<p>The hardware interface to the dart board is not very complicated. First of all, electronic dart boards usually contain a two layer plastic sheet that has conductive lines printed on it.</p>

<p>When a segment of the dart board is pressed (e.g., because a dart hit it), one line of the upper layer is connected momentarily to one line on the lower layer. The lines (for example, 4 for the upper layer and 7 for the lower layer) form a matrix, like a <a href="http://www.dribin.org/dave/keyboard/one_html/" class=" ">classic key matrix</a>. The lines are connected to the GPIO pins of the Arduino Mega, which scans the matrix for presses. When it detects that a segment was pressed, it encodes the segment into one byte and sends this byte to the Raspberry Pi, which receives it over a virtual serial connection. Except for the dart board, all components needed can be bought online. In the next weeks, I will write follow-up posts with more details on the hardware. </p>

<p>The software is written in python using the <a href="https://pypi.python.org/pypi/circuits" class=" ">circuits framework</a>. This framework allows for loosely-coupled components that can be added and removed during run time. For example, there are components responsible for the sounds and background music. The sound theme can be switched by removing one component and adding another. </p>

<p>The web interface is based on the excellent <a href="https://angularjs.org/" class=" ">AngularJS</a> framework. It is updated dynamically and with very little overhead using websockets.</p>

<h2>Source Code</h2>

<p>The source code is available upon request (its not really useful currently unless adapted to your own board).</p>

