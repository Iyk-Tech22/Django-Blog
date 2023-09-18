"""
    Defines forms used by the blog app
"""
from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """ Define the email form structure """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    
# COMMENT FORM
class CommentForm(forms.ModelForm):
    """ Build a form from an existing model """
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
