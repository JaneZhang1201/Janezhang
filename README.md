# Zhaohan Zhang — Personal Site

My personal website, built with **Django 5.2**: a home page, projects imported from GitHub, a blog, an online CV, and a contact form. All content is edited through the Django admin.

> Rebuilt in 2026 from my first Django project (2019–2020). The original code is still in this repo's git history.

## Features

- **Home**: intro plus the three most recent blog posts
- **Projects**: imports your public GitHub repos (language, stars, last update) with one click in the admin. You choose which to show and feature, and can add a screenshot and write-up
- **Blog**: list and detail pages with readable URLs (`/blog/<slug>/`), drafts, and scheduled publishing
- **CV**: profile, work history, education, skills and hobbies as web text, plus your full CV as a PDF (e.g. exported from Overleaf), embedded on the page with download and open-in-new-tab buttons
- **Contact**: message form that redirects after sending (no duplicate submissions), with a honeypot field against spam bots. Messages appear in the admin.
- Responsive layout with automatic light/dark mode, no frontend framework needed

## Tech stack

Python 3.12 · Django 5.2 · SQLite · WhiteNoise (static files) · python-dotenv

## Project structure

```
Janezhang/
├── config/            # Django settings, URLs, WSGI/ASGI
├── blog/              # Post model, list/detail views
├── cv/                # Profile, Experience, Education, Skill; home & CV views
├── contact/           # Message model and contact form
├── projects/          # Project model, GitHub import (github.py), import_github command
├── templates/         # base layout, partials and page templates
├── static/css/        # site stylesheet
├── fixtures/          # starter content (blog posts + CV)
├── requirements.txt
└── .env.example       # copy to .env for local settings
```

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # local dev settings (DEBUG on)
python manage.py migrate
python manage.py loaddata fixtures/initial_content.json   # optional starter content
python manage.py createsuperuser  # your admin login
python manage.py runserver
```

Then open http://127.0.0.1:8000. The admin is at http://127.0.0.1:8000/admin/.

Forgot the admin password? Reset it with `python manage.py changepassword <username>`.

## Updating the CV PDF

1. In Overleaf, click **Download PDF**.
2. In the admin, open **Profile**, choose the file under **CV (PDF)**, and save.

The CV page embeds the PDF on larger screens and shows download/open buttons on phones. Only `.pdf` files are accepted.

## Projects from GitHub

Your GitHub username is taken from the GitHub URL in your Profile (or the `GITHUB_USERNAME` setting).

- **Admin**: Projects → **Import from GitHub**, or from the terminal: `python manage.py import_github`
- New repos arrive **hidden**. Tick *show on site* to publish one, and *feature on home page* to show it on the home page and CV.
- Re-importing refreshes stars, language and dates. It never overwrites your own title, summary, write-up or visibility choices.
- Forks are skipped (`--include-forks` to include them). Optional `GITHUB_TOKEN` raises GitHub's rate limit.

## Tests

```bash
python manage.py test
```

## Deploying (e.g. PythonAnywhere)

Set these environment variables on the server:

| Variable | Example |
|---|---|
| `DJANGO_DEBUG` | `false` |
| `DJANGO_SECRET_KEY` | a long random string (see `.env.example` for how to generate one) |
| `DJANGO_ALLOWED_HOSTS` | `janezhang1201.pythonanywhere.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://janezhang1201.pythonanywhere.com` |
| `GITHUB_TOKEN` (optional) | a GitHub token with no scopes, only needed if imports hit the rate limit |

Then run `python manage.py migrate` and `python manage.py collectstatic`. Serve `media/` (uploaded photos and CV PDFs) through your host's static-files settings. Run `python manage.py check --deploy` to catch security misconfigurations.

The database (`db.sqlite3`), uploads (`media/`) and `.env` are git-ignored on purpose. Never commit them.
