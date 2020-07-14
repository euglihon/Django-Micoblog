from django.core.mail import send_mail
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm
from .models import Post
from django.views.generic import ListView # базовый класс обработчик


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
class PostListView(ListView):
    # обработчик через базовый класс, а не функцию
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    # поиск поста в таблице Post, если ничего нет вернёт 404
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # функция получает post по его id
    post = get_object_or_404(Post, id=post_id, status='published')

    sent = False
    # ели форма была отправлена
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # если все поля прошли валидацию
            data = form.cleaned_data # записываем данные из формы

            # отправка электронной почты
            form_name = data['name']
            form_email = data['email']
            form_to = data['to']
            form_body = data['body']
            mail_title = f'{form_name}, {form_email} recommends you reding'
            post_url = request.build_absolute_uri(post.get_absolute_url())
            mail_body = f'Read {post.title}, at {post_url}\n{form_name} comments: {form_body}'

            send_mail(mail_title, mail_body, 'admin@gmail.com', [form_to, ])
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share_post.html',
                      {'post': post, 'form': form, 'sent': sent})