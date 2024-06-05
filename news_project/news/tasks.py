# news/tasks.py
from celery import shared_task
from .models import Search
from django.utils import timezone
import requests

NEWS_API_KEY = '3b90dd5d454240748486312eeada983a'

@shared_task
def refresh_search_results():
    searches = Search.objects.all()
    for search in searches:
        # Fetch new articles for the search keyword from the API
        # (Implement the logic to fetch and update articles here)
        keyword = search.keyword
        # Fetch articles from the API (replace with actual API call)
        response = requests.get(f'https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}')
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            for article in articles:
                # Check if the article already exists to avoid duplicates
                if not search.article_set.filter(url=article['url']).exists():
                    search.article_set.create(
                        title=article['title'],
                        description=article['description'],
                        url=article['url'],
                        published_at=timezone.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                    )
