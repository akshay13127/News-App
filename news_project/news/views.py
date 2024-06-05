import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Search, Article
from .forms import SearchForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from news_project.settings import *


def login_view(request):
    """
    The login_view function is a view that handles the login process.
    It takes in a request object and returns an HttpResponseRedirect to the search page if successful, or renders the login template with an AuthenticationForm if unsuccessful.
    
    :param request: Get the request object
    :return: A rendered template of the login page
    :doc-author: Trelent
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('search')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    """
    The logout_view function logs the user out of the system.
        It takes a request as an argument and returns a redirect to login.
    
    :param request: Get the current user
    :return: The redirect function, which is a shortcut for returning an httpresponseredirect
    :doc-author: Trelent
    """
    logout(request)
    return redirect('login')

@login_required
def search(request):
    """
    Handle search requests. Create or fetch a Search object based on the keyword.
    Fetch articles if the search is new or if no articles exist for it.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object rendering the search form or redirecting to results.
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            search, created = Search.objects.get_or_create(
                user=request.user,
                keyword=keyword
            )
            if created or not search.article_set.exists():
                fetch_articles(search)
            return redirect('results')
    else:
        form = SearchForm()
    return render(request, 'news/search.html', {'form': form})


@login_required
def results(request):
    searches = Search.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'news/results.html', {'searches': searches})

@login_required
def refresh_search(request, search_id):
    """
    Refresh the articles for a given search. Only fetch new articles published after
    the latest article in the database.

    Args:
        request (HttpRequest): The request object.
        search_id (int): The ID of the Search object to refresh.

    Returns:
        HttpResponse: The response object redirecting to the results page.
    """
    search = get_object_or_404(Search, id=search_id, user=request.user)
    
    # Prevent frequent refreshes
    last_refreshed = search.article_set.order_by('-published_at').first()
    if last_refreshed and timezone.now() - last_refreshed.published_at < timedelta(minutes=SEARCH_THRESHOLD):
        return redirect('results')
    
    latest_article_date = search.article_set.order_by('-published_at').first().published_at if search.article_set.exists() else None
    fetch_articles(search, latest_article_date)
    return redirect('results')


def fetch_articles(search, from_date=None, to_date=None, source_name=None, category=None, language=None):
    """
    Fetch articles from the News API and save them to the database.

    Args:
        search (Search): The Search object for which to fetch articles.
        from_date (datetime, optional): The date from which to start fetching new articles.
        to_date (datetime, optional): The date till which to fetch new articles.
        source_name (str, optional): The name of the news source.
        category (str, optional): The category of the news.
        language (str, optional): The language of the articles.
    """
    params = {
        'q': search.keyword,
        'apiKey': NEWS_API_KEY,
        'sortBy': 'publishedAt',
    }
    if from_date:
        params['from'] = from_date.isoformat()
    if to_date:
        params['to'] = to_date.isoformat()
    if source_name:
        params['sources'] = source_name
    if category:
        params['category'] = category
    if language:
        params['language'] = language
    
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()

    for article_data in data.get('articles', []):
        Article.objects.create(
            search=search,
            title=article_data['title'],
            description=article_data.get('description', ''),
            url=article_data['url'],
            published_at=article_data['publishedAt'],
        )


def signup(request):
    """
    The signup function is a view that allows users to sign up for an account.
        It takes in the request and returns a rendered template of the signup form.
        If the user submits valid information, it creates an account for them and logs them in.
    
    :param request: Get the request object
    :return: A rendered template if the request is a get request
    :doc-author: Trelent
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return render(request, 'news/search.html', {'form': form})  # Redirect to the home page
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def check_keyword(request):
    keyword = request.GET.get('keyword', None)
    if keyword:
        exists = Search.objects.filter(user=request.user, keyword=keyword).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})
