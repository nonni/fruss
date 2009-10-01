from django import forms
from models import Thread, Category

class ThreadForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())
    category = forms.ModelChoiceField( Category.objects.all())

    class Meta:
        model = Thread
        fields = ['title', 'body', 'category']
