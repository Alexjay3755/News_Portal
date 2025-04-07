from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = 0
        comments_rating = 0
        post_comments_rating = 0
        posts =  Post.objects.filter(author=self)
        for p in posts:
            post_rating += p.rating
        comments = Comment.objects.filter(user=self.user)
        for c in comments:
            comments_rating += c.rating
        post_comments = Comment.objects.filter(post__author=self)
        for pc in post_comments:
            post_comments_rating += pc.rating

        self.rating = post_rating * 3 + comments_rating + post_comments_rating
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique = True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name

class Post(models.Model):

    news = 'N'
    article = 'A'

    options = [
        (news, 'Новости'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=1, choices=options, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    # @property
    # def on_stock(self):
    #     return self.rating > 0

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/post/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()




