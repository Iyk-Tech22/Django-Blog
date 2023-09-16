"""
    Defines forms used by the blog app
"""
from django import forms

class EmailPostForm(forms.Form):
    """ Define the email form structure """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

