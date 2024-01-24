from django.urls import path
from .views import PostsList, PostDetail, PostSearch, NewsCreate, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, \
    ArticleDelete, CategoryListView, subscribe

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_urls'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('add/', NewsCreate.as_view(), name='news_add'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe,name='subscribe'),
]