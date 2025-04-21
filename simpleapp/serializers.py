from .models import *
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Author
       fields = ['id', 'rating', 'user_id', 'url']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['id', 'name', 'name_en_us', 'name_ru', 'url',]


class PostSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['id', 'author_id', 'type_post', 'title', 'text', 'rating', 'url']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Comment
       fields = ['id', 'text', 'rating', 'user_id', 'post_id']


class PostCategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = PostCategory
       fields = ['id', 'category_id', 'post_id']



from rest_framework import serializers
from .models import Post

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'