from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>/', DetailList.as_view(), name='detail'),
    path('create/', CreatePost.as_view(), name='create'),
    path('<int:pk>/edit/', EditPost.as_view(), name='edit'),
    path('<int:pk>/delete/', DeletePost.as_view(), name='delete'),

]
