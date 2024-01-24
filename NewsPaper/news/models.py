from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(Post_Rating=models.Sum('rating')).get('Post_Rating') or 0
        comment_rating = Comment.objects.filter(post__author=self).aggregate(Comment_Rating=models.Sum('rating')).get(
            'Comment_Rating') or 0
        self.rating = posts_rating * 3 + comment_rating
        self.save()

class Category(models.Model):
    # имя категории - текстовое поле длинной не более 64 сим-ов и уникальное(unique)
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    # Внутренний класс (Мета класс), который используется для определения модели.
    class Meta:
        # Настройка отображения имени модели в админ панели (ед число)
        verbose_name = 'Категория'
        # Настройка отображения имени модели в админ панели (множ число)
        verbose_name_plural = 'Категории'

    # Данный метод переопределен, чтобы корректно отображать нужную нам
    # информацию (имя пользователя - автора) в админке
    def __str__(self):
        # вывод имени категории в админке в формате "f-строки"
        return f'{self.name}'


class CategorySubscribers(models.Model):
    sub_categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_users = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sub_categories}, {self.sub_users}'

class Post(models.Model):
    ARTICLE = 'ART'
    NEWS = 'NEW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=3, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + '...'
        return self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title} : {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
