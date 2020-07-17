from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog'

    def items(self):
        # объекты включенные в рассылку
        return Post.published.all()[:5]

    def item_title(self, item):
        # вернёт заголовок статьи
        return item.title

    def item_description(self, item):
        # вернёт описание статьи, truncatewords -- ограничит 30 символами
        return truncatewords(item.body, 30)