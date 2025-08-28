from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    #model = Post
    #ordering = "categoryType"
    queryset = Post.objects.filter(
        categoryType = 'NW'
    )
    template_name = "news.html"
    context_object_name = "news"


class PostDetail(DetailView):
    queryset = Post.objects.filter(
        categoryType='NW'
    )
    template_name = "idnews.html"
    context_object_name = "idnews"
