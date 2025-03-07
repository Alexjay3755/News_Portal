from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import BaseRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'



