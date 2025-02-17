from django import forms
from django.core.exceptions import ValidationError


from .models import Posts


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Posts
        fields = ['title', 'text', 'category', 'author']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("text")
        text = cleaned_data.get("user")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data