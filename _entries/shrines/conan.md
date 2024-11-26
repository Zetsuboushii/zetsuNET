---
layout: default
title: Detektiv Conan
category: shrine
---

<div class="sunken-panel" style="width: 634px">
    <table style="width: 630px">
        <thead>
        <tr>
            <th style="width: 100px">Episode</th>
            <th>Fall</th>
            <th>Score</th>
        </tr>
        </thead>
        <tbody>
        {% assign conan_posts = site.entries | where: "category", "Conan" %}
        {% for post in conan_posts %}
            <tr>
                <td>
                    {% if post.ep %}
                        {{ post.ep }}
                        {% if post.to %}
                            - {{ post.to }}
                        {% endif %}
                    {% endif %}
                    {% if post.film %}
                        Film {{ post.film }}
                    {% endif %}
                </td>
                <td><a href="{{ post.url | relative_url }}">{{ post.title }}</a></td>
                <td style="text-align: center;">{{ post.judgement | escape }} / 10</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
</div>