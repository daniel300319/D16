from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect, get_object_or_404
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category, CategorySubscriber
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .tasks import *
from django.template.loader import render_to_string

class PostsList(ListView):
    model = Post
    ordering = "-created_at"
    template_name = "news.html"
    context_object_name = "posts"
    paginate_by = 10



class PostDetail(DetailView):
    model = Post
    template_name = "new.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_now"] = datetime.utcnow()

        return context


class PostSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'post_search.html'
    context_object_name = 'posts_search'
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context



class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать новость'
        return context


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать статью'
        return context


# Представление для изменения новости одинаково с созданием, используем только другой дженерик
class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать новость'
        return context


class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать статью'
        return context


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Удалить новость'
        context['previous_page_url'] = reverse_lazy('post_list')
        return context


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Удалить статью'
        context['previous_page_url'] = reverse_lazy('post_list')
        return context

class CategoryList(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'

class CategoryDetail(DetailView):
    # указываем имя шаблона
    template_name = 'news/category_subscription.html'
    # указываем модель(таблицу базы данных)
    model = Category

    # для отображения кнопок подписки (если не подписан: кнопка подписки - видима, и наоборот)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # общаемся к содержимому контекста нашего представления
        category_id = self.kwargs.get('pk')  # получаем ИД поста (выдергиваем из нашего объекта из модели Категория)
        # формируем запрос, на выходе получим список имен пользователей subscribers__username, которые находятся
        # в подписчиках данной группы, либо не находятся
        category_subscribers = Category.objects.filter(pk=category_id).values("subscribers__username")
        # Добавляем новую контекстную переменную на нашу страницу, выдает либо правду, либо ложь, в зависимости от
        # нахождения нашего пользователя в группе подписчиков subscribers
        context['is_not_subscribe'] = not category_subscribers.filter(
            subscribers__username=self.request.user).exists()
        context['is_subscribe'] = category_subscribers.filter(subscribers__username=self.request.user).exists()
        return context

@login_required
def add_subscribe(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.subscribers.add(request.user)
    print('Пользователь', request.user, 'добавлен в подписчики категории:', category)
    return redirect('news:category_list')


# def sending_emails_to_subscribers(instance):
#     sub_text = instance.text
#     sub_title = instance.title
#     # получаем нужный объект модели Категория через рк Пост
#     category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).categories.pk)
#     # получаем список подписчиков категории
#     subscribers = category.subscribers.all()
#
#     # проходимся по всем подписчикам в списке
#     for subscriber in subscribers:
#         # создание переменных, которые необходимы для таски
#         subscriber_username = subscriber.username
#         subscriber_useremail = subscriber.email
#         html_content = render_to_string('news/mail.html',
#                                         {'user': subscriber,
#                                          'title': sub_title,
#                                          'text': sub_text[:50],
#                                          'post': instance})
#         # функция для таски, передаем в нее все что нужно для отправки подписчикам письма
#         email_task(subscriber_username, subscriber_useremail, html_content)
#     return redirect('/news/')