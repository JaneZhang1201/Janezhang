# Jane Zhang — Personal Site

My personal website, built with **Django 5.2**: a home page, a blog, an online CV, and a contact form. All content is edited through the Django admin.

> Rebuilt in 2026 from my first Django project (2019–2020). The original code is still in this repo's git history.

## Features

- **Home**: intro plus the three most recent blog posts
- **Blog**: list and detail pages with readable URLs (`/blog/<slug>/`), drafts, and scheduled publishing
- **CV**: profile, work history, education, skills and hobbies, rendered as real HTML (with an optional PDF download)
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

Then run `python manage.py migrate` and `python manage.py collectstatic`. Serve `media/` (uploaded photos and CV PDFs) through your host's static-files settings. Run `python manage.py check --deploy` to catch security misconfigurations.

The database (`db.sqlite3`), uploads (`media/`) and `.env` are git-ignored on purpose. Never commit them.
