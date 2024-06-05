from django.contrib import admin
from news.models import *
from news.forms import *

# from datetime import datetime

# from django.contrib import messages
# from django.contrib.postgres import fields
# from django.http import HttpResponse
# from django.shortcuts import redirect
# from django.urls import path
# from django_json_widget.widgets import JSONEditorWidget
from django.contrib import admin



class SearchAdmin(admin.ModelAdmin):
    pass

class ArticleAdmin(admin.ModelAdmin):
    pass

    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Search, SearchAdmin)
# Register your models here.
