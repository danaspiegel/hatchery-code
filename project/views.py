from django.template.response import TemplateResponse
from django.shortcuts import redirect

import forms


def index2(request):
    return TemplateResponse(request, 'index2.html', {
        'var1': 'This is var1',
        'var2': 'This is var2',
        'list_var': ['a', 'b', 'c'],
    })


def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            return redirect('contact_complete')
    else:
        form = forms.ContactForm()

    return TemplateResponse(request, 'contact.html', {
        'form': form,
    })


def contact_complete(request):
    return TemplateResponse(request, 'contact_complete.html')
