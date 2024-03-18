from django import forms
from .models import Contact, Comment

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = "__all__"


class SubscriptionForm(forms.ModelForm):
    subject = forms.CharField(max_length=150)
    message = forms.CharField()
    email = forms.EmailField()


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']
