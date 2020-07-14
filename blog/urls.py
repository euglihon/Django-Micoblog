from django.urls import path
from . import views


# определяем пространство имен, для групировки
app_name = 'blog'


# маршруты и загрузка функций из  views
urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'), # реализация через обработчик класса
    # извлекаем значения из пути и передаем их функции views.post_detail
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail')
]