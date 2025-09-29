from django import forms

from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'is_published',
            'title',
            'text',
            'pub_date',
            'location',
            'category',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M:%S'
            )
        }
