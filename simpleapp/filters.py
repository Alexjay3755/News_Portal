
from django_filters.widgets import RangeWidget

from .models import Post
import django_filters

class PostFilter(django_filters.FilterSet):

    time_in = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:

       model = Post
       fields = {
           'title': ['exact'] ,
           'author': ['exact'],

       }