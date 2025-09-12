from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy


class PostsList(ListView):
    queryset = Post.objects.filter(
        categoryType = 'NW'
    )
    template_name = "news.html"
    context_object_name = "news"
    paginate_by = 10


class PostDetail(DetailView):
    queryset = Post.objects.filter(
        categoryType='NW'
    )
    template_name = "idnews.html"
    context_object_name = "idnews"


class PostArticlesList(ListView):
    queryset = Post.objects.filter(
        categoryType='AR'
    )
    template_name = "articles.html"
    context_object_name = "articles"
    paginate_by = 10


class PostArticlesDetail(DetailView):
    queryset = Post.objects.filter(
        categoryType='AR'
    )
    template_name = "article.html"
    context_object_name = "article"


class PostSearchList(ListView):
    template_name = "search.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.categoryType = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.categoryType = 'AR'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('product_list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('product_list')