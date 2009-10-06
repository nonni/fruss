from django import forms
from models import Post, Category, Thread

class ThreadForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())
    category = forms.ModelChoiceField( Category.objects.all())

    class Meta:
        model = Thread
        fields = ['title', 'body', 'category']


class ReplyForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())
    
    class Meta:
        model = Post
        fields = ['body']
