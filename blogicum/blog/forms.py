from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'is_published',
            'title',
            'text',
            'pub_date',
            'location',
            'category',
            'image',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M:%S'
            )
        }
