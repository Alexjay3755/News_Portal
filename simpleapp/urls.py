from django.urls import path
from .views import (
    PostsDetail, ArticlesCreate, NewsUpdate, NewsDelete, subscribe,
    NewsSearch, NewsCreate, ArticlesDelete, ArticlesUpdate, CategoryListView
)
from django.urls import path
from .views import upgrade_me

urlpatterns = [

    path('post/<int:pk>/', PostsDetail.as_view(), name='post_detail'),
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

]



