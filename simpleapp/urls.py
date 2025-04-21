from django.core.cache import cache
from django.urls import path
from django.views.decorators.cache import cache_page

from protect.views import IndexView
from .views import (
    PostDetail, ArticlesCreate, NewsUpdate, NewsDelete, subscribe,
    NewsSearch, NewsCreate, ArticlesDelete, ArticlesUpdate, CategoryListView, Index1,
)
from django.urls import path
from .views import upgrade_me

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from simpleapp import views


router = routers.DefaultRouter()
router.register(r'news', views.NewsViewSet, basename='news')
router.register(r'articles', views.ArticlesViewSet, basename='articles')
router.register(r'authors', views.AuthorViewest)
router.register(r'categories_n', views.CategoryViewset)
router.register(r'posts_n', views.PostViewset)
router.register(r'postcategories', views.PostCategoryViewset)
router.register(r'comments', views.CommentViewest)

urlpatterns = [

    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    # path('post/<int:pk>/', cache_page(60*5)(PostsDetail.as_view(), name='post_detail')),
    # path('posts/', cache_page(60)(NewsSearch.as_view(), name='news_search')),
    path('posts/', NewsSearch.as_view(), name='news_search'),
#
#
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    path('article/create/', ArticlesCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticlesUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticlesDelete.as_view(), name='article_delete'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('time_zone/', Index1.as_view(), name='time_zone'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', include(router.urls)),

    # path('swagger-ui/', TemplateView.as_view(
    #     template_name='swagger-ui.html',
    #     extra_context={'schema_url': 'openapi-schema'}
    # ), name='swagger-ui'),

    path('swagger-n/', TemplateView.as_view(
        template_name='swagger-n.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-n'),

    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),

]



