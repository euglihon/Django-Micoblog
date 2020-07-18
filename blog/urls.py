from django.urls import path
from . import views
from .feeds import LatestPostFeed


# определяем пространство имен, для групировки
app_name = 'blog'


# маршруты и загрузка функций из  views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    path('<int:post_id>/share', views.post_share, name='post_share'),
    # путь к rss фиду
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search')
]