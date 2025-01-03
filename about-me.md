---
layout: default
title: About the Webmaster
permalink: /about-me/
header: true
---

<div style="text-align: center; margin-bottom: 10px">
    <img src="{{ "/assets/gifs/const001.gif" | relative_url }}" alt="">
</div>

<menu role="tablist" id="tablist" style="margin-top: 20px">
    <li role="tab" aria-selected="true" data-tab="dev">Development</li>
    <li role="tab" aria-selected="false" data-tab="consoles">Console restauration</li>
    <li role="tab" aria-selected="false" data-tab="music">Music</li>
    <li role="tab" aria-selected="false" data-tab="japan">Japanese pop culture</li>
    <li role="tab" aria-selected="false" data-tab="oldweb">Oldweb</li>
    <li role="tab" aria-selected="false" data-tab="publictrans">Public transit</li>
    <li role="tab" aria-selected="false" data-tab="dnd">D&D</li>
</menu>
<div class="window tabpanel-container">
    <div id="dev" class="window-body tabpanel" role="tabpanel" aria-hidden="false">
        Besonders faszinierend finde ich, wie es Entwicklern in der NES-, SNES- und N64-Ära gelungen ist, komplexe
        Spiele auf extrem eingeschränkter Hardware zu erschaffen. Diese Herausforderung und die damit verbundene
        Notwendigkeit zur Optimierung haben mich stark beeinflusst. Ich versuche, diesen Ansatz in meiner eigenen Arbeit
        zu verfolgen: Code sollte effizient und einfach sein. Leider führt die nahezu unbegrenzte Rechenleistung
        moderner Geräte oft dazu, dass der Fokus auf Code-Optimierung verloren geht, und viele Entwickler greifen
        schnell zu Frameworks und trivialen Bibliotheken. Ein Zitat von Terry A. Davis, dem Entwickler von TempleOS, hat
        mich dabei besonders geprägt: “An idiot admires complexity, a genius admires simplicity.” (Ich distanziere mich
        jedoch ausdrücklich von den problematischen Aussagen, die Davis durch seine Schizophrenie getätigt hat.) Für
        mich gilt der Leitsatz: Einfachheit ist das ultimative Ziel.
    </div>
    <div id="consoles" class="window-body tabpanel" role="tabpanel" aria-hidden="true" style="">
        Das Restaurieren alter Nintendo-Konsolen ist für mich nicht nur eine technische Herausforderung, sondern auch
        eine Herzensangelegenheit. Die Geräte meiner Kindheit, wie der Game Boy und das SNES, wieder funktionsfähig zu
        machen, ist für mich eine Kombination aus Nostalgie, technischer Fertigkeit und Kreativität. Jede Konsole hat
        ihre eigene Geschichte, und es ist ein erfüllendes Gefühl, diese Geschichte fortzuführen, indem ich den Geräten
        neues Leben einhauche. Besonders spannend finde ich dabei, wie die Technik hinter diesen Konsolen funktioniert,
        und ich liebe es, diese alten Technologien zu verstehen.
    </div>
    <div id="music" class="window-body tabpanel" role="tabpanel" aria-hidden="true" style="">
        Musik spielt eine wichtige Rolle in meinem Leben. Seit meinem sechsten Lebensjahr spiele ich Klavier, und ich
        habe eine besondere Vorliebe für Videospiel- und Anime-Soundtracks. Diese Stücke sind oft emotional, komplex und
        erzählen eigene Geschichten, was mich immer wieder inspiriert. Besonders die Soundtracks von Nintendo haben mich
        stark geprägt, da frühe Komponisten wie Koji Kondo den unverwechselbaren Stil der Nintendo-Musik etabliert
        haben, der mich durch meine gesamte Kindheit begleitet hat. Darüber hinaus höre ich überwiegend japanische Pop-
        und Rockmusik. Der einzigartige Stil vieler japanischer Künstler und die Vielfalt der Genres faszinieren mich.
        Im Vergleich dazu finde ich, dass sich Pop- und Rockmusik in Deutschland oft wie Massenware anhört. Für einen
        genaueren Einblick: Mein Spotify-Profil ist im Footer dieser Seite verlinkt.
    </div>
    <div id="japan" class="window-body tabpanel" role="tabpanel" aria-hidden="true" style="">
        Ich interessiere mich sehr für die japanische Popkultur, insbesondere für Anime und Manga. Meine ersten Anime
        waren “ Steins;Gate” und “Detektiv Conan”, die beide bis heute zu meinen absoluten Favoriten zählen. Ich liebe
        es, in die unterschiedlichen Welten der Geschichten einzutauchen und finde es unglaublich faszinierend, wie
        vielfältig und kreativ die Inhalte der japanischen Popkultur sind. Auch die oben genannten Musikrichtungen
        begleiten mich jeden Tag, und ich genieße es, mich damit zu befassen.
    </div>
    <div id="oldweb" class="window-body tabpanel" role="tabpanel" aria-hidden="true" style="">
        Ich finde das Internet der 90er und frühen 2000er unfassbar nostalgisch, auch wenn das noch vor meiner Geburt
        war. Besonders spannend finde ich die Internetkultur rund um Seiten wie 2chan und NicoNicoDouga, die außerhalb
        Japans fast schon unbekannt sind. Diese Subkulturen haben eine einzigartige Atmosphäre, die mich fasziniert und
        mich daran erinnert, wie anders und experimentell das Internet in seiner frühen Phase war.
    </div>
    <div id="publictrans" class="window-body tabpanel" role="tabpanel" aria-hidden="true" style="">
        Meine Arbeit bei der DB Systel bietet mir die Möglichkeit, an einer nachhaltigen Mobilitätslösung für die
        Zukunft mitzuwirken. Ich glaube fest daran, dass der Ausbau öffentlicher Verkehrsmittel der richtige Weg zu
        einer umweltfreundlichen und effizienten Mobilität ist. Es motiviert mich, Teil dieser Vision zu sein und daran
        zu arbeiten, den öffentlichen Verkehr effizienter und nutzerfreundlicher zu gestalten. Mobilität sollte für
        jeden zugänglich, umweltfreundlich und gemeinschaftlich sein – und ich bin stolz darauf, durch meine Arbeit
        meinen Teil dazu beizutragen.
    </div>
    <div id="dnd" class="window-body tabpanel" role="tabpanel" aria-hidden="true" style="">
        Ich spiele und leite hauptsächlich als Dungeon Master Dungeons & Dragons. Mein Hauptfokus liegt zurzeit auf
        einer massiven Kampagne, zu der ich auch ein eigenes Wiki und eine interaktive Karte geschrieben habe. Ich liebe
        es, mir Welten, Charaktere und Konflikte auszudenken und anschließend meine Spieler mit allem interagieren und
        sich in der Welt immersieren zu sehen.
    </div>
</div>

<script>
    document.addEventListener("DOMContentLoaded", () => {
        const tabs = document.querySelectorAll('[role="tab"]');
        const panels = document.querySelectorAll('.tabpanel');

        tabs.forEach((tab) => {
            tab.addEventListener("click", () => {
                tabs.forEach((t) => t.setAttribute("aria-selected", "false"));
                panels.forEach((p) => p.setAttribute("aria-hidden", "true"));

                tab.setAttribute("aria-selected", "true");
                const tabId = tab.getAttribute("data-tab");
                document.getElementById(tabId).setAttribute("aria-hidden", "false");
            });
        });
    });
</script>