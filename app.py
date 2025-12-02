import json
from flask import Flask, render_template, g, Response, session, redirect, url_for, request, flash
import markdown
import os
import glob
from datetime import timezone
from zoneinfo import ZoneInfo
from email.utils import format_datetime
from pathlib import Path
import requests
import base64
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet

# -----------------------------------------------------------------------------
# Setup & Config
# -----------------------------------------------------------------------------

app = Flask(__name__, static_folder="static")

# app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")
app.secret_key = "baba"

app.config["FREEZER_DESTINATION_IGNORE"] = ["index"]
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False
app.config["FREEZER_DEFAULT_MIMETYPE"] = "text/html"

# -----------------------------------------------------------------------------
# Constants & Paths
# -----------------------------------------------------------------------------

SITE_TITLE = "ZetsuNET"
SITE_URL = "https://zetsuboushii.site"
SITE_DESC = "Updates ausgewählter Seiten"

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
        "title": "Tome of the Vastlands: Purpurne Rache",
        "url_path": "/totv-pr.html",
        "sources": [
            "templates/totv_pr.html",
            "static/pdfs/totv-pr*.pdf",
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

DIARY_DIR = Path("data/diary")
DIARY_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Auth Helpers
# -----------------------------------------------------------------------------

def is_logged_in() -> bool:
    return session.get("admin_logged_in", False)


def require_login(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)

    return wrapper


# -----------------------------------------------------------------------------
# Generic Helper Functions
# -----------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------
# Encryption & Storage
# -----------------------------------------------------------------------------

def get_fernet() -> Fernet:
    # secret = os.environ.get("DIARY_KEY")
    secret = "secret"
    if not secret:
        raise RuntimeError("DIARY_KEY env var not set")

    key_bytes = hashlib.sha256(secret.encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(key_bytes)
    return Fernet(key)


def encrypt_diary_entry(data: dict) -> bytes:
    f = get_fernet()
    payload = json.dumps(data).encode("utf-8")
    return f.encrypt(payload)


def decrypt_diary_entry(token: bytes) -> dict:
    f = get_fernet()
    decrypted = f.decrypt(token)
    return json.loads(decrypted.decode("utf-8"))


def save_diary_entry(entry_id: str, data: dict) -> None:
    token = encrypt_diary_entry(data)
    path = DIARY_DIR / f"{entry_id}.json.enc"
    with open(path, "wb") as f:
        f.write(token)


def load_diary_entry(entry_id: str) -> dict | None:
    path = DIARY_DIR / f"{entry_id}.json.enc"
    if not path.exists():
        return None
    with open(path, "rb") as f:
        token = f.read()
    return decrypt_diary_entry(token)


def list_diary_entries() -> list[dict]:
    entries = []
    for path in DIARY_DIR.glob("*.json.enc"):
        entry_id = path.stem.replace(".json", "")
        try:
            data = load_diary_entry(entry_id)
            data["id"] = entry_id
            entries.append(data)
        except Exception:
            continue

    def sort_key(e):
        return e.get("created_at", "")

    entries.sort(key=sort_key, reverse=True)
    return entries


# -----------------------------------------------------------------------------
# Request Hooks
# -----------------------------------------------------------------------------

@app.before_request
def before_request():
    g.site_title = "ZetsuNET"
    g.version = "b4.4"
    g.git_hash = get_git_hash()

    g.static = "/static/"
    g.debug = app.debug


# -----------------------------------------------------------------------------
# Public Pages
# -----------------------------------------------------------------------------

# --- Home Page ---

@app.route("/")
def index():
    home_json = load_from_json("home.json")
    content_md = load_from_markdown("home.md")

    response = requests.get("https://zetsuboushii.github.io/Zetsuboushii/README.md")
    response.raise_for_status()
    readme_text = response.text
    readme_html = markdown.markdown(
        readme_text, extensions=["fenced_code", "tables", "toc", "codehilite"]
    )

    plants = []
    plants_json = load_from_json("herbarium/herbarium.json")
    for p in plants_json:
        plants.append({"name": p["nickname"], "id": p["id"]})

    return render_template(
        "index.html",
        home=home_json,
        content=content_md,
        readme=readme_html,
        plants=plants
    )


# --- About ---

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

    plants = []
    plants_json = load_from_json("herbarium/herbarium.json")
    for p in plants_json:
        plants.append({"name": p["nickname"], "id": p["id"]})

    return render_template(
        "about.html",
        intro=intro_md,
        interests=interests_md,
        favourites=favourites_md,
        favs=favs,
        plants=plants
    )


# --- Blogs ---

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


# --- Writing ---

@app.route("/totv-pr.html")
def totv_pr():
    return render_template("totv_pr.html")


@app.route("/totv-gdg.html")
def totv_gdg():
    return render_template("totv_gdg.html")


# --- Music ---

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

    lyrics = []
    lyrics_entries = glob.glob(os.path.join("static/entries/music/lyrics", "*.json"))
    for entry in lyrics_entries:
        lyrics.append(load_from_json(entry.replace("static/entries", "")))

    return render_template(
        "music.html", intro=intro_md, playlists=playlists, lyrics=lyrics
    )


# --- Videogames ---

@app.route("/collection.html")
def collection():
    return render_template("collection.html")


@app.route("/gamelog.html")
def gamelog():
    data = load_from_json("gamelog/gamelog.json")

    completed = []
    planned = []
    not_completed = []

    for game in data:
        for p in game.get("versions", []):
            entry = {"name": game["name"], "plattform": p["plattform"]}
            if p["status"] == "f":
                completed.append(entry)
            elif p["status"] == "p":
                planned.append(entry)
            elif p["status"] == "n":
                not_completed.append(entry)

    completed.sort(key=lambda x: x["name"].lower())
    planned.sort(key=lambda x: x["name"].lower())
    not_completed.sort(key=lambda x: x["name"].lower())

    n = max(len(completed), len(planned), len(not_completed))

    return render_template(
        "gamelog.html",
        completed=completed,
        planned=planned,
        not_completed=not_completed,
        max=n,
    )


# --- Herbarium ---

@app.route("/herbarium/<id>.html")
def herbarium(id):
    plants_json = load_from_json("herbarium/herbarium.json")
    plant = next((p for p in plants_json if p["id"] == id), None)

    return render_template("herbarium.html", plant=plant, now=datetime.now(timezone.utc))


# --- Misc ---

@app.route("/license.html")
def license():
    entry = os.path.join("LICENSE")

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


# -----------------------------------------------------------------------------
# Login / Logout
# -----------------------------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        # expected = os.environ.get("ADMIN_PASSWORD")
        expected = "admin"
        if not expected:
            error = "ADMIN_PASSWORD ist serverseitig nicht gesetzt."
        elif password == expected:
            session["admin_logged_in"] = True
            next_url = request.args.get("next") or url_for("diary_index")
            return redirect(next_url)
        else:
            error = "Falsches Passwort."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# -----------------------------------------------------------------------------
# Private Pages
# -----------------------------------------------------------------------------

@app.route("/diary")
@require_login
def diary_index():
    entries = list_diary_entries()
    return render_template("diary_index.html", entries=entries)


@app.route("/diary/<entry_id>")
@require_login
def diary_view(entry_id):
    entry = load_diary_entry(entry_id)
    if not entry:
        return "Not found", 404
    return render_template("diary_view.html", entry=entry)


@app.route("/diary/new", methods=["GET", "POST"])
@require_login
def diary_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not content:
            return render_template("diary_new.html", error="Should not be empty")

        now = datetime.now(timezone.utc).isoformat()
        entry_id = datetime.now().strftime("%Y%m%d-%H%M%S")

        data = {
            "title": title,
            "content": content,
            "created_at": now,
        }

        save_diary_entry(entry_id, data)
        return redirect(url_for("diary_view", entry_id=entry_id))

    return render_template("diary_new.html")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc")
