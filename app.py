import json
from flask import Flask, render_template, request, g, redirect, url_for
import markdown
import os
import glob

from flask_frozen import Freezer

app = Flask(__name__, static_folder="static")
freezer = Freezer(app)

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'


def load_from_json(filename):
    with open(f'static/json/{filename}', encoding="utf8") as file:
        return json.load(file)


def load_from_markdown(filename):
    with open(f'static/entries/{filename}', encoding="utf8") as file:
        return markdown.markdown(file.read())


def load_file(filename):
    with open(f'static/entries/{filename}', encoding="utf8") as file:
        return file.read()


@app.before_request
def before_request():
    g.site_title = "ZetsuNET"
    g.version = "b2.⛩"

    g.static = "/static/"
    g.debug = app.debug

    apex_domain = "zetsuboushii.site/"
    image_subdomain = "https://images."
    g.img_host = image_subdomain + apex_domain + "dnd/"
    g.img_host_resized = image_subdomain + apex_domain + "resized/dnd/"


@app.route('/')
def index():
    home_json = load_from_json("home.json")
    content_md = load_from_markdown("home.md")

    return render_template('index.html', home=home_json, content=content_md)


@app.route('/about')
def about():
    intro_md = load_from_markdown("about/about.md")
    interests_md = load_from_markdown("about/interests.md")
    return render_template('about.html', intro=intro_md, interests=interests_md)


@app.route('/collection')
def collection():
    return render_template('collection.html')


@app.route('/gamelog')
def gamelog():
    return render_template('gamelog.html')


@app.route('/japan')
def japan():
    blog_entries = glob.glob(os.path.join("static/entries/blog/japan-3", "*.md"))
    entries = []

    for entry in blog_entries:
        with open(entry, encoding="utf8") as file:
            entries.append((os.path.splitext(os.path.basename(entry))[0], file.read()))

    return render_template('japan.html', entries=entries)


@app.route('/music')
def music():
    return render_template('music.html')


if __name__ == '__main__':
    app.run(debug=True)
