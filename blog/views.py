from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView # базовый класс обработчик


class PostListView(ListView):
    # обработчик через базовый класс, а не функцию
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# def post_list(request):
#     # запрос через собственный менеджер
#     posts = Post.published.all()
#     # Создаём объект пагинации
#     paginator = Paginator(posts, 3)  # по три поста на странице
#     # из GET запроса получаем текущую страницу
#     page = request.GET.get('page')
#
#     try:
#         # если все ок
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # если страница не является целым числом
#         posts = paginator.page(1)
#     except EmptyPage:
#         # если номер страницы больше чем число страниц, вернем последнею
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'blog/post/list.html', {'page': page,
#                                                    'posts': posts})


def post_detail(request, year, month, day, post):
    # поиск поста в таблице Post, если ничего нет вернёт 404
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
