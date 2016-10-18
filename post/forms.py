from django import forms
from .models import Post, Comment
from django.forms.extras.widgets import SelectDateWidget
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=SelectDateWidget)
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "tags",
            "draft",
            "publish"
        ]


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("name", "text",)
