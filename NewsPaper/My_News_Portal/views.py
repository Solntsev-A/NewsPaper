import pytz
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Subscription, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from django.views import View
from django.utils import timezone


class PostsList(ListView):
    queryset = Post.objects.filter(
        categoryType='NW'
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

    def get_object(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        cache_key = f'post-{pk}'

        obj = cache.get(cache_key)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(cache_key, obj)
        return obj


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

    def get_object(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        cache_key = f'post-{pk}'

        obj = cache.get(cache_key)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(cache_key, obj)
        return obj


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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('My_News_Portal.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.categoryType = 'NW'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('My_News_Portal.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.categoryType = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('My_News_Portal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('My_News_Portal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('My_News_Portal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('My_News_Portal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('articles_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class SetTimezoneView(View):
    def post(self, request):
        timezone = request.POST.get('timezone')
        if timezone:
            request.session['django_timezone'] = timezone
        return redirect(request.META.get('HTTP_REFERER', '/'))
