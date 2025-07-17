from django import forms

class BlogForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=2, required=True)
    content = forms.CharField(min_length=2, required=True)
    category_id = forms.IntegerField(required=True)
