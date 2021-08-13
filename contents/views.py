import datetime
import os
from calendar import monthrange
from random import randint
from time import timezone

from django.http import JsonResponse, FileResponse, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from itertools import chain
from django.core.mail import send_mail

# from users.filters import BorrowFilter
# from .forms import *
from .models import *
from django.db.models import Count
from django.db.models import Q

# Create your views here.


class Home(View):

    def get(self, *args, **kwargs):
        posts = Post.objects.all()[:3]
        slides = Slide.objects.all()

        context = {
            'posts': posts,
            'slides': slides,
        }

        return render(self.request, 'home.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post-detail.html'
    slug_field = 'post_id'
    slug_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().exclude(post_id=self.object.post_id)
        context["posts"] = posts
        return context
