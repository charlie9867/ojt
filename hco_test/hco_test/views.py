from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

class MainView(TemplateView):
    template_name = 'main.html'
