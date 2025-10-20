from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
    
    def clean_title(self):
        t = self.cleaned_data['title']
        if "test" in t.lower():
            raise forms.ValidationError("Title cannot contain the word 'test'.")
        if len(t) < 3:
            raise forms.ValidationError('Title too short.')
        return t
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'text': forms.TextInput(attrs={'placeholder': 'Your comment', 'rows': 3}),
        }

def clean_text(self):
    t = self.cleaned_data.get('text', '').strip()
    if len(t) < 2:
        raise forms.ValidationError('Comment is too short.')
    return t