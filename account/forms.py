from django import forms

class BlogEditForm(forms.Form):
    class meta:
        fields = ['title', 'slug', 'category', '']