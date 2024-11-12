---
layout: home
title: Touhou
category: shrine
---

<menu role="tablist" id="tablist" style="margin-top: 20px">
    <li role="tab" aria-selected="true" data-tab="characters">Favourite Chars</li>
    <li role="tab" aria-selected="false" data-tab="fumo">My Fumos</li>
</menu>
<div class="window tabpanel-container">
    <div id="characters" class="window-body tabpanel" role="tabpanel" aria-hidden="false">
        <fieldset class="shrine-field">
            <legend>Cirno</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/cirno.png" | relative_url }}" alt="">
                <p>
                    Baka fairy.
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Saigyouji Yuyuko</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/yuyuko.png" | relative_url }}" alt="">
                <p>
                    Hungry ghost.
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Patchouli Knowledge</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/patchouli.png" | relative_url }}" alt="">
                <p>
                    Asthma witch.
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Remilia Scarlet</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/remilia.png" | relative_url }}" alt="">
                <p>
                    Smug vampire.
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Komeiji Koishi</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/koishi.png" | relative_url }}" alt="">
                <p>
                    Schizo hat.
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Reisen Udongein Inaba</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/reisen.png" | relative_url }}" alt="">
                <p>
                    Funny bnuuy.
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Kirisame Marisa</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/marisa.png" | relative_url }}" alt="">
                <p>
                    Kleptomaniac witch.
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Chen</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/chen.webp" | relative_url }}" alt="">
                <p>
                    Honk-honk cat.
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Yagokoro Eirin</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/eirin.png" | relative_url }}" alt="">
                <p>
                    Help me, Eirin!
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Konpaku Youmu</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/youmu.png" | relative_url }}" alt="">
                <p>
                    Myon-na!
                </p>
            </div>
        </fieldset>
        <fieldset class="shrine-field">
            <legend>Koakuma</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/koakuma.png" | relative_url }}" alt="">
                <p>
                    Silly demon.
                </p>
            </div>
        </fieldset>
    </div>
    <div id="fumo" class="window-body tabpanel" role="tabpanel" aria-hidden="true" style="">
        <fieldset class="shrine-field" style="width: 196px">
            <legend>Cirnu</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/cirno_fumo.jpg" | relative_url }}" alt="">
            </div>
        </fieldset>
        <fieldset class="shrine-field" style="width: 196px">
            <legend>Udonge</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/reisen_fumo.jpg" | relative_url }}" alt="">
            </div>
        </fieldset>
        <fieldset class="shrine-field" style="width: 196px">
            <legend>Patche</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/patchouli_fumo.jpg" | relative_url }}" alt="">
            </div>
        </fieldset>
        <fieldset class="shrine-field" style="width: 196px">
            <legend>Yukari</legend>
            <div class="field-row">
                <img src="{{ "/assets/imgs/touhou/yukari_fumo.jpg" | relative_url }}" alt="">
            </div>
        </fieldset>
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