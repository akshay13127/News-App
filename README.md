# Midnight Times

A news search app. Sign up, search any keyword with optional filters, and every search is saved to your account so you can come back to it. A background job refreshes saved searches every hour with new articles.

Django 4.2, Celery 5.4 with Redis, NewsAPI, SQLite.

## Features

- **Account-based search history.** Each user has their own saved searches and the articles that came back for them.
- **Filters.** Narrow by date range, source, category or language (passed straight through to NewsAPI).
- **No duplicate searches.** Searching a keyword you've already saved reuses it, and an AJAX check warns you before you submit.
- **Manual refresh with a cooldown.** You can pull fresh results for a saved search, but not more often than every 15 minutes, which keeps the free NewsAPI quota alive.
- **Hourly background refresh.** Celery beat walks every saved search on the hour and adds articles it hasn't seen, deduplicated by URL.
- **Full auth flow.** Sign up, log in, log out and password reset.

## Data model

```
User 1--* Search (keyword, created_at)
             1--* Article (title, description, url, published_at)
```

## Run it locally

You'll need Python 3.9+, Redis, and a free API key from https://newsapi.org.

```bash
cd news_project
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export NEWS_API_KEY=your_key_here
python manage.py migrate
python manage.py runserver
```

For the hourly refresh, run Celery in two more terminals:

```bash
celery -A news_project worker -l info
celery -A news_project beat -l info
```

Open http://localhost:8000/search/.

## Routes

| Path | Does |
| --- | --- |
| `/signup/`, `/login/`, `/logout/` | Account management |
| `/search/` | Search form and your saved searches |
| `/results/` | Articles for the current search |
| `/refresh/<id>/` | Re-fetch a saved search (15 minute cooldown) |
| `/check_keyword/` | AJAX check for an existing saved keyword |
