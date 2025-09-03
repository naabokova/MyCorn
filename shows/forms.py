from django import forms
from .models import Show, Episode

class CommentForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=10, required=False)
    comment = forms.CharField(required=False, widget=forms.Textarea)