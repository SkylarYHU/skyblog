from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    # 如果不是为了自定义placeholder，这三行可以不用写
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your comment here...'}), max_length=500)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))

    # 定义表单包含的字段，分别是 name、email 和 body
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
