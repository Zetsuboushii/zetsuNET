---
layout: home
title: Music
permalink: /music/
header: true
category: music
---

{% assign music_posts = site.entries | sort: "date" | reverse %}

<div>
    {% for post in music_posts %}
        {% if post.category == "music" %}

            {% assign youtube_url = post.ytlink %}
            {% assign video_id = youtube_url | split: "youtu.be/" | last %}
            {% assign video_id = video_id | split: "?" | first %}

            <fieldset>
                <legend>{{ post.title }}</legend>
                <div class="field-row">
                    <a href="{{ post.ytlink }}"><img src="https://img.youtube.com/vi/{{ video_id }}/mqdefault.jpg"
                                                     alt=""></a>
                </div>
            </fieldset>

        {% endif %}

    {% endfor %}
</div>