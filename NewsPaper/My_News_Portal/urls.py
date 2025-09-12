from django.urls import path
from .views import PostsList, PostDetail, PostArticlesList, PostArticlesDetail, PostSearchList, NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete

urlpatterns = [
    path('news/', PostsList.as_view(), name='news_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/', PostArticlesList.as_view(), name='articles_list'),
    path('articles/<int:pk>', PostArticlesDetail.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('news/search/', PostSearchList.as_view(), name='post_search'),
]