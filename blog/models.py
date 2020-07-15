from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # пользователи админки django
from django.urls import reverse


class PublishedManager(models.Manager):
    # Свой менеджер запроса к БД для поиска опубликованных постов
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOISES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # не даст создать одинаковый пост в один день
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default='draft')  # choices - возможные значения
    # внешний ключ.  models.CASCADE--- при удалении пользв. удаляться и его статьи
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    objects = models.Manager() # Менеджер по умолчанию
    published = PublishedManager() # Новый менеджер

    class Meta: # метаданные
        ordering = ('-publish',) # порядок сортировки Постов (по убыванию даты публикации)

    def __str__(self): # отображение объекта в понятном виде (например в админке)
        return self.title

    # создание канонического URL для каждого поста
    # будет вызвана в шаблоне в момент перехода на отдельный пост
    def get_absolute_url(self):
        return reverse('blog:post_detail', # название функции во views
                       args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Для того чтобы скрывать некоторые комментарии
    active = models.BooleanField(default=True)
    # внешний ключ
    # related_name --- обратная ссылка для обращения из другой таблицы
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'