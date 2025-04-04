from gc import get_objects
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from pyexpat.errors import messages
from unicodedata import category
from django_filters.rest_framework import FilterSet, filters
from django.shortcuts import render, reverse, redirect
from django.views import View
from .filters import PostFilter
from .forms import PostForm
from .models import Posts, Category
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .tasks import create_news_task

class NewsSearch(LoginRequiredMixin, ListView):
    model = Posts
    ordering = '-time_in'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostsDetail(DetailView):
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Posts.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'posts-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'posts-{self.kwargs["pk"]}', obj)

        return obj


class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Posts
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'A'
        # create_news_task.delay(post.pk)
        return super().form_valid(form)


class NewsCreate(CreateView):
    form_class = PostForm
    model = Posts
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'N'
        # create_news_task.delay(post.pk)
        return super().form_valid(form)



class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_posts', 'simpleapp.change_posts')
    form_class = PostForm
    model = Posts
    template_name = 'articles_edit.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context



class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_posts', 'simpleapp.change_posts')
    form_class = PostForm
    model = Posts
    template_name = 'news_edit.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


# Представление удаляющее товар.
class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.add_posts', 'simpleapp.change_posts')
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_search')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.add_posts', 'simpleapp.change_posts')
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_search')



class PostsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        post = Posts(
            author=request.POST['author'],
            title=request.POST['title'],
        )
        post.save()
        return redirect('appointments:make_appointment')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

class CategoryListView(NewsSearch):
    model = Posts
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Posts.objects.filter(category=self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории..Ура!!..'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})



# from django.http import HttpResponse
# from django.views import View
# from .tasks import hello
#
# class dexView(View):
#     def get(self, request):
#         hello.delay()
#         return HttpResponse('Hello!')