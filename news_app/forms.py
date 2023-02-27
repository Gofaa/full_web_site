from django import forms
from .models import ContactUs, Comment


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = "__all__"

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

