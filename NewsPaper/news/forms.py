from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'title',
            'text',
            'post_type'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 3:
            raise ValidationError({
                "post_title": "Заголовок статьи не может быть менее трех символов или пустым."
            })
        return cleaned_data