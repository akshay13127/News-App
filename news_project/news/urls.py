from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('results/', views.results, name='results'),
    path('refresh/<int:search_id>/', views.refresh_search, name='refresh_search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('check_keyword/', views.check_keyword, name='check_keyword'),
]