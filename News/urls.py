from django.urls import path, include
from django.contrib import admin
from .views import *

urlpatterns = [
    path('news/', NewsList.as_view(), name='post_list'),
    path('author_now/', author_now, name='author_now'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='one_post'),
]