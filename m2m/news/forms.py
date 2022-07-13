from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'types_of_topic',
            'text'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 10:
            raise ValidationError({
                "title": "Описание не может быть менее 10 символов."
            })
        text = cleaned_data.get("text")
        if text is not None and len(text) < 10:
            raise ValidationError({
                "text": "Описание не может быть менее 10 символов."
            })
        if text == title:
            raise ValidationError({
                "text": "описание не должно повторять название"
            })
        return cleaned_data
