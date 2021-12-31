from django.shortcuts import render
from django.views.generic import TemplateView


class Register(TemplateView):
    template_name = 'register.html'
