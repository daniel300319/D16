from django.urls import path
from .views import PostsList, PostDetail, PostSearch, NewsCreate, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, \
    ArticleDelete, CategoryList, add_subscribe, CategoryDetail

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_urls'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('add/', NewsCreate.as_view(), name='create_post'),
    path('categories/', (CategoryList.as_view()), name='categories'),
    # Страница выбранной категории для подписки/отписки
    path('categories/<int:pk>/', (CategoryDetail.as_view()), name='category_subscription'),
    # Функция-представление для подписки на выбранную категорию
    path('categories/<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
]