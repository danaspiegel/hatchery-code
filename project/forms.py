from django import forms
from django.core.validators import *


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    age = forms.IntegerField(validators=[MinValueValidator(20),
                                         MaxValueValidator(100)])
