from django import forms
from models import Post, Category, Thread

class ThreadForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())
    category = forms.ModelChoiceField( Category.objects.all())
    markdown = forms.BooleanField(initial=True, required=False)


class ReplyForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea())
    markdown = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Post
        fields = ['body']
