"""
Admin file of Django for which table in database to show in administration page
"""
from django.contrib import admin
from app.models import Article, User

admin.site.register(Article)
admin.site.register(User)
