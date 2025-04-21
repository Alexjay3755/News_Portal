from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, Author, PostCategory, Comment
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from .models import Category, Post
from django.shortcuts import redirect

from .serializers import AuthorSerializer, CategorySerializer, PostSerializer, PostCategorySerializer, \
    CommentSerializer, NewsSerializer, ArticlesSerializer
from .templatetags.custom_tags import current_time



class IsAuthenticatedOrReadOnly1(permissions.BasePermission):
    """Разрешает GET, HEAD, OPTIONS всем, а POST, PUT, DELETE — только авторизованным пользователям."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_authenticated


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type_post='N').order_by('-time_in')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly1]


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type_post='A').order_by('-time_in')
    serializer_class = ArticlesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly1]


class NewsSearch(LoginRequiredMixin, ListView, View):
    model = Post
    ordering = '-time_in'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10



    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context




class PostDetail(DetailView):
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'A'
        # create_news_task.delay(post.pk)
        return super().form_valid(form)


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'N'
        # create_news_task.delay(post.pk)
        return super().form_valid(form)



class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_post', 'simpleapp.change_post')
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context



class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_post', 'simpleapp.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


# Представление удаляющее товар.
class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.add_post', 'simpleapp.change_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_search')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.add_post', 'simpleapp.change_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_search')



@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/posts/')


class CategoryListView(NewsSearch):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_in')
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


from django.views.decorators.cache import cache_page  # импортируем декоратор для кэширования отдельного представления


@cache_page(
    60 * 15)  # в аргументы к декоратору передаём количество секунд, которые хотим, чтобы страница держалась в кэше. Внимание! Пока страница находится в кэше, изменения, происходящие на ней, учитываться не будут!
def my_view(request):
    ...



class Index1(View):
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.META['HTTP_REFERER'])


from django.shortcuts import render
from rest_framework import viewsets, permissions
from education.serializers import *
from education.models import *


class AuthorViewest(viewsets.ModelViewSet):
   queryset = Author.objects.all()
   serializer_class = AuthorSerializer


class CategoryViewset(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer


class PostViewset(viewsets.ModelViewSet):
   queryset = Post.objects.all()
   serializer_class = PostSerializer


class PostCategoryViewset(viewsets.ModelViewSet):
   queryset = PostCategory.objects.all()
   serializer_class = PostCategorySerializer


class CommentViewest(viewsets.ModelViewSet):
   queryset = Comment.objects.all()
   serializer_class = CommentSerializer