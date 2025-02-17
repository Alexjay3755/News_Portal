from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import PostFilter
from .forms import PostForm
from .models import Posts



class NewsSearch(ListView):
    model = Posts
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
        context['filterset'] = self.filterset
        return context


class PostsDetail(DetailView):
    model = Posts
    template_name = 'post.html'
    context_object_name = 'post'


class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'A'
        return super().form_valid(form)


class NewsCreate(CreateView):
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'N'
        return super().form_valid(form)


class ArticlesUpdate(UpdateView):
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'


# Представление удаляющее товар.
class ArticlesDelete(DeleteView):
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_search')


class NewsDelete(DeleteView):
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_search')

