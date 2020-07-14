from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Post


@admin.register(Post)  # Регаем модель в админке
class PostAdmin(admin.ModelAdmin):
    # отобрж. столбцов в админке
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # отобрж. боковой панели фильтрции
    list_filter = ('status', 'created', 'publish', 'author')
    # отобрж. инпута поиска по указаным полям
    search_fields = ('title', 'body')
    # автозаполняемое поле на основе title
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('author', )
    # ссылки по навигации по датам
    date_hierarchy = 'publish'
    # сортировк по полям
    ordering = ('status', 'publish')