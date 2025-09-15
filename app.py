import json
from flask import Flask, render_template, g, Response
import markdown
import os
import glob
from flask_frozen import Freezer
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from email.utils import format_datetime
from pathlib import Path

app = Flask(__name__, static_folder="static")
freezer = Freezer(app)

app.config["FREEZER_DESTINATION_IGNORE"] = ["index"]
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False
app.config["FREEZER_DEFAULT_MIMETYPE"] = "text/html"


def rfc822(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("Europe/Berlin"))
    else:
        dt = dt.astimezone(ZoneInfo("Europe/Berlin"))
    return format_datetime(dt)


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def latest_mtime(paths: list[str]) -> datetime:
    mtimes = []
    for p in paths:
        for path in Path(".").glob(p):
            try:
                ts = path.stat().st_mtime
                mtimes.append(datetime.fromtimestamp(ts, tz=timezone.utc))
            except FileNotFoundError:
                pass
    return max(mtimes) if mtimes else datetime.now(timezone.utc)


SITE_TITLE = "ZetsuNET"
SITE_URL   = "https://zetsuboushii.site"
SITE_DESC  = "Updates ausgewählter Seiten"

MONITORED_PAGES = [
    {
        "title": "Tome of the Vastlands: Geißel der Gier",
        "url_path": "/totv-gdg.html",
        "sources": [
            "templates/totv_gdg.html",
            "static/pdfs/totv-gdg*.pdf",
        ],
        "summary": "Aktualisierte Version der PDF.",
    },
    {
        "title": "About the Webmaster",
        "url_path": "/about.html",
        "sources": [
            "templates/about.html",
            "static/entries/about/*.md",
            "static/entries/about/*.json",
        ],
        "summary": "Neue/aktualisierte Einträge.",
    },
    {
        "title": "Music",
        "url_path": "/music.html",
        "sources": [
            "templates/music.html",
            "static/entries/music/*.md",
        ],
        "summary": "Neue/aktualisierte Playlists.",
    },
    {
        "title": "Blog",
        "url_path": "/blog.html",
        "sources": [
            "templates/blog.html",
            "static/entries/blog/**/*",      
        ],
        "summary": "Neue/aktualisierte Blog-Einträge.",
    },
]


def get_git_hash() -> str:
    try:
        import subprocess

        params = ["/usr/bin/git", "rev-parse", "HEAD"]
        raw = subprocess.check_output(params)
        return raw.decode("ascii").strip()
    except Exception as e:
        print("failed to get git hash:", e, flush=True)
        return "unknown"


def load_from_json(filename):
    with open(f"static/entries/{filename}", encoding="utf8") as file:
        return json.load(file)


def load_from_markdown(filename):
    with open(f"static/entries/{filename}", encoding="utf8") as file:
        return markdown.markdown(file.read())


def load_file(filename):
    with open(f"static/entries/{filename}", encoding="utf8") as file:
        return file.read()


@app.before_request
def before_request():
    g.site_title = "ZetsuNET"
    g.version = "b4.4"
    g.git_hash = get_git_hash()

    g.static = "/static/"
    g.debug = app.debug


@app.route("/")
def index():
    home_json = load_from_json("home.json")
    content_md = load_from_markdown("home.md")

    return render_template("index.html", home=home_json, content=content_md)


@app.route("/about.html")
def about():
    intro_md = load_from_markdown("about/about.md")
    interests_md = load_from_markdown("about/interests.md")
    favourites_md = load_from_markdown("about/favourites.md")
    favs = {
        "fav_characters": {
            "text": load_from_markdown("about/fav-characters.md"),
            "characters": load_from_json("about/fav-characters.json"),
        },
        "fav_films": {
            "text": load_from_markdown("about/fav-films.md"),
            "films": load_from_json("about/fav-films.json"),
        },
    }

    return render_template(
        "about.html",
        intro=intro_md,
        interests=interests_md,
        favourites=favourites_md,
        favs=favs,
    )


@app.route("/totv-gdg.html")
def totv_gdg():
    return render_template("totv_gdg.html")


@app.route("/collection.html")
def collection():
    return render_template("collection.html")


@app.route("/gamelog.html")
def gamelog():
    return render_template("gamelog.html")


@app.route("/blog.html")
def blog():
    return render_template("blog.html")


@app.route("/blog/<blog>.html")
def blog_entry(blog):
    entries = []

    heading = load_file(f"blog/{blog}/heading")
    blog_entries = glob.glob(os.path.join(f"static/entries/blog/{blog}", "*.md"))

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

    return render_template("blog.html", entries=entries, blog=blog, heading=heading)


@app.route("/music.html")
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

    return render_template("music.html", intro=intro_md, playlists=playlists)


@app.route("/license.html")
def license():
    entry = os.path.join(f"LICENSE")

    with open(entry, encoding="utf8") as file:
        license_file = file.read()

    return render_template("license.html", license=license_file)


@app.route("/feed.xml")
def feed_xml():
    items = []
    for page in MONITORED_PAGES:
        updated = latest_mtime(page["sources"])
        link = SITE_URL.rstrip("/") + page["url_path"]
        items.append(
            {
                "title": page["title"],
                "link": link,
                "guid": link,  # permalink
                "summary": page.get("summary", ""),
                "updated": updated,
            }
        )

    items.sort(key=lambda x: x["updated"], reverse=True)
    last_build = items[0]["updated"] if items else datetime.now(timezone.utc)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<rss version="2.0">')
    lines.append("<channel>")
    lines.append(f"<title>{esc(SITE_TITLE)}</title>")
    lines.append(f"<link>{SITE_URL}</link>")
    lines.append(f"<description>{esc(SITE_DESC)}</description>")
    lines.append("<language>de-de</language>")
    lines.append(f"<lastBuildDate>{rfc822(last_build)}</lastBuildDate>")

    for it in items:
        lines.append("<item>")
        lines.append(f"<title>{esc(it['title'])}</title>")
        lines.append(f"<link>{it['link']}</link>")
        lines.append(f"<guid isPermaLink='true'>{it['guid']}</guid>")
        if it["summary"]:
            lines.append(f"<description>{esc(it['summary'])}</description>")
        lines.append(f"<pubDate>{rfc822(it['updated'])}</pubDate>")
        lines.append("</item>")

    lines.append("</channel></rss>")
    xml = "\n".join(lines)
    return Response(xml, mimetype="application/rss+xml; charset=utf-8")


if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc")