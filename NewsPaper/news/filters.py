from django_filters import FilterSet, DateFilter
from .models import Post, Author


class PostFilter(FilterSet):
    created_at = DateFilter
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'created_at': ['gt'],
            'categories': ['exact']
        }