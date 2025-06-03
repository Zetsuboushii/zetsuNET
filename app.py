import json
from flask import Flask, render_template, g, request
import markdown
import os
import glob
from flask_frozen import Freezer

app = Flask(__name__, static_folder="static")
freezer = Freezer(app)

app.config['FREEZER_DESTINATION_IGNORE'] = ['index']
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'


def load_from_json(filename):
    with open(f'static/entries/{filename}', encoding="utf8") as file:
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


@app.route('/')
def index():
    home_json = load_from_json("home.json")
    content_md = load_from_markdown("home.md")

    return render_template('index.html', home=home_json, content=content_md)


@app.route('/about.html')
def about():
    intro_md = load_from_markdown("about/about.md")
    interests_md = load_from_markdown("about/interests.md")
    favourites_md = load_from_markdown("about/favourites.md")
    favs = {
        "fav_characters": {
            "text": load_from_markdown("about/fav-characters.md"),
            "characters": load_from_json("about/fav-characters.json")
        },
        "fav_films": {
            "text": load_from_markdown("about/fav-films.md"),
            "films": load_from_json("about/fav-films.json")
        }
    }

    return render_template('about.html', intro=intro_md, interests=interests_md,
                           favourites=favourites_md, favs=favs)


@app.route('/collection.html')
def collection():
    return render_template('collection.html')


@app.route('/gamelog.html')
def gamelog():
    return render_template('gamelog.html')


@app.route('/blog.html')
def blog():
    return render_template('blog.html')


@app.route('/blog/<blog>.html')
def blog_entry(blog):
    entries = []

    heading = load_file(f'blog/{blog}/heading')
    blog_entries = glob.glob(os.path.join(f'static/entries/blog/{blog}', "*.md"))

    for entry in blog_entries:
        with open(entry, encoding="utf8") as file:
            entries.append((os.path.splitext(os.path.basename(entry))[0], file.read()))

    def sort_key(entry):
        name, _ = entry
        if name == "intro":
            return (1, "")
        try:
            return (0, name)
        except ValueError:
            return (2, name)

    entries = sorted(entries, key=sort_key, reverse=True)

    return render_template('blog.html', entries=entries, blog=blog, heading=heading)


@app.route('/music.html')
def music():
    intro_md = load_from_markdown("music/intro.md")
    playlists = {
        "daily": load_from_markdown("music/daily.md"),
        "vocaloid": load_from_markdown("music/vocaloid.md"),
        "schizo": load_from_markdown("music/schizo.md"),
        "citypopfusion": load_from_markdown("music/citypop-fusion.md"),
        "conan": load_from_markdown("music/conan.md"),
        "silly": load_from_markdown("music/silly.md"),
    }

    return render_template('music.html', intro=intro_md, playlists=playlists)


if __name__ == '__main__':
    app.run(debug=True)
    freezer.freeze()
