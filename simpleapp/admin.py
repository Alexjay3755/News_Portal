from django.contrib import admin
from .models import Posts, Author, Category, Comment, PostCategory

admin.site.register(Posts)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)



