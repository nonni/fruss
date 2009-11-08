from django import forms
from models import Post, Category, Thread
from django.utils.translation import ugettext as _

class ThreadForm(forms.Form):
    '''
    New thread form
    '''
    title = forms.CharField(label=_('Title'))
    body = forms.CharField(widget=forms.Textarea(), label=_('Body'))
    category = forms.ModelChoiceField( Category.objects.all(), label=_('Category'))
    markdown = forms.BooleanField(initial=True, required=False, label=_('Markdown'))


class ReplyForm(forms.ModelForm):
    '''
    New reply form
    '''
    body = forms.CharField(widget=forms.Textarea(), label=_('Body'))
    markdown = forms.BooleanField(initial=True, required=False, label=_('Markdown'))

    class Meta:
        model = Post
        fields = ['body', 'markdown']
