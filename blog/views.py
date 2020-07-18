from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm, CommentFrom, SearchForm
from .models import Post
from taggit.models import Tag
from django.db.models import Count # функция БД для подсчёта количества

# страница всех постов
def post_list(request, tag_slug=None):
    posts = Post.published.all()

    # Фильтрация постов по тегам
    tag = None
    if tag_slug:
        # если передастся слаг тега
        # формируем начальный массив
        tag = get_object_or_404(Tag, slug=tag_slug)
        # формируем посты по полученным тегам
        posts = posts.filter(tags__in=[tag])

    # Создаём объект пагинации
    paginator = Paginator(posts, 4)  # по три поста на странице
    # из GET запроса получаем текущую страницу
    page = request.GET.get('page')

    try:
        # если все ок
        posts = paginator.page(page)
    except PageNotAnInteger:
        # если страница не является целым числом
        posts = paginator.page(1)
    except EmptyPage:
        # если номер страницы больше чем число страниц, вернем последнею
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


# страница каждого поста
def post_detail(request, year, month, day, post):
    # поиск поста в таблице Post, если ничего нет вернёт 404
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # реализация системы комментариев
    # получение активных комментариев из таблицы Comment через обратную ссылку
    comments = post.comments.filter(active=True)
    new_comment = None # заглушка
    if request.method == 'POST':
        # если форма отправлена
        comment_form = CommentFrom(request.POST)
        if comment_form.is_valid():
            # создаём комментарий
            new_comment = comment_form.save(commit=False) # объект создастся из данных формы но не пойдет в БД
            # привязка комментария к текущему посту
            new_comment.post = post
            # сохранение в БД
            new_comment.save()
    else:
        comment_form = CommentFrom()

    # Реализация блока рекомендованных постов
    # запись в массив всех ID тегов,   flat=True --- плоский массив
    post_tags_id = post.tags.values_list('id', flat=True)
    # получаем все статьи у которых есть хоть один тег полученный раньше из массива
    similar_posts = Post.published.filter(tags__in=post_tags_id)
    # исключаем текущую статью из списка
    similar_posts = similar_posts.exclude(id=post.id)
    # формируем поле, которое содержит количество совпадений.
    # сортируем список по количеству совпадение и оставляем только 4 результата
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


# поделиться постом через email
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


# полнотекстовый поиск
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        # проверка отправлена ли форма чрез GET
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']

        # title будет важнее в ранжировании чем body
        serch_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        serch_query = SearchQuery(query)

        results = Post.objects.annotate(
            serch=serch_vector,
            rank=SearchRank(serch_vector, serch_query)
        ).filter(serch=serch_query).order_by('-rank')

    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})
