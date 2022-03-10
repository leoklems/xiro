import datetime
import os
from calendar import monthrange
from random import randint
from time import timezone

from django.core.paginator import Paginator
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
from .forms import *
from .models import *
from django.db.models import Count
from django.db.models import Q

# Create your views here.


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,
                            password=password)

        if user is not None:
            login(request, user)
            staff = Author.objects.get(user=request.user)
            act = Activity(actor=staff, action='Login')
            act.save()
            return redirect('content:s_home')

        else:
            messages.info(request, 'username or password is incorrect')

    return render(request, 'forms/login.html')


def logoutUser(request):
    staff = Author.objects.get(user=request.user)
    act = Activity(actor=staff, action='Logout')
    act.save()
    logout(request)
    return redirect('content:login')


class Home(View):

    def get(self, *args, **kwargs):
        posts = Post.objects.all()[:3]
        slides = Slide.objects.all()

        context = {
            'posts': posts,
            'slides': slides,
        }

        return render(self.request, 'home.html', context)


class Posts(View):

    def get(self, *args, **kwargs):
        posts = Post.objects.all().exclude(lead=True)
        post = Post.objects.get(lead=True)

        context = {
            'posts': posts,
            'post': post,
        }

        return render(self.request, 'posts.html', context)


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

# --------------------------------------Admin section-----------------------


class AdminHome(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        posts = Post.objects.all()[:10]
        post_cats = PostCategory.objects.all()
        slides = Slide.objects.all()
        staff = Author.objects.all()

        context = {
            'posts': posts,
            'post_cats': post_cats,
            'slides': slides,
            'staff': staff,
        }

        return render(self.request, 'staff/home.html', context)


class AdminStaff(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        staff = Author.objects.all()

        context = {
            'staff': staff,
        }

        return render(self.request, 'staff/staff.html', context)


class AdminPostCats(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        post_cats = PostCategory.objects.all()
        context = {
            'post_cats': post_cats,
        }

        return render(self.request, 'staff/post_cathegories.html', context)


class AdminPosts(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        posts = Post.objects.all()
        context = {
            'posts': posts,
        }

        return render(self.request, 'staff/posts.html', context)



class PostImages(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        images = PostImage.objects.all()
        context = {
            'images': images,
        }

        return render(self.request, 'staff/post-images.html', context)


class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'staff/staff-profile.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor = Author.objects.get(user=self.object.user)
        acts = Activity.objects.filter(actor=self.object).order_by('-action_date')[:10]
        context["acts"] = acts
        return context


class StaffActivities(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'staff/staff-activities.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    # paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        acts = Activity.objects.filter(actor=self.object).order_by('-action_date')
        paginator = Paginator(acts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["acts"] = page_obj
        return context


class AdminSlides(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        slides = Slide.objects.all()
        context = {
            'slides': slides,
        }

        return render(self.request, 'staff/slides.html', context)


class AdminPostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'staff/post-detail.html'
    slug_field = 'post_id'
    slug_url_kwarg = 'post_id'


class AdminSlideDetailView(LoginRequiredMixin, DetailView):
    model = Slide
    template_name = 'staff/slide-detail.html'


def random_int():
    random_ref = randint(0, 9999999999)
    uid = random_ref
    return uid


class AuthorRegistration(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('users.add_user', 'users.add_student')

    def get(self, request):
        form = CreateUserForm()
        profile_form = AuthorProfileForm()

        context = {
            'form': form,
            'profile_form': profile_form,
        }
        return render(request, 'forms/registration.html', context)

    def post(self, request, *args, **kwargs):
        u_name = request.POST.get('username')
        # print(request.POST ,'', request.FILES)
        profile_form = AuthorProfileForm(request.POST, request.FILES)
        form = CreateUserForm(request.POST)

        if profile_form.is_valid() and form.is_valid():
            user = form.save()
            username = user.username

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.uid = random_int()
            profile.save()
            staff = Author.objects.get(user=request.user)
            act = Activity(actor=staff, type='Add', action=f'Account created for {username}')
            act.save()

            messages.success(request, 'Account was created for ' + username)

            return redirect('user:register_student')

        else:
            # when the form has an error
            print(profile_form.errors)
            profile_form = AuthorProfileForm()
            messages.success(request, 'Fill out all the necessary details ')
            context = {
                'form': form,
                'profile_form': profile_form,
            }
            return render(request, 'forms/registration.html', context)


class DeleteStaff(LoginRequiredMixin, DeleteView):

    model = Author
    template_name = 'forms/delete_staff.html'
    success_url = reverse_lazy('content:s_home')


class AddPost(LoginRequiredMixin, CreateView):

    model = Post
    form_class = PostForm
    template_name = 'forms/post.html'
    success_url = reverse_lazy('content:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        categories = self.request.POST.getlist('categories')
        # print(categories)
        author = Author.objects.get(user=self.request.user)
        form = form.save(commit=False)
        form.post_id = random_int()
        form.author = author
        if form.lead:
            try:
                leads = Post.objects.filter(lead=True)
                for lid in leads:
                    lid.lead = False
                    lid.save()
            except ObjectDoesNotExist:
                pass

        form.save()
        for i in categories:
            category = PostCategory.objects.get(id=i)
            c_in = Post.objects.get(post_id=self.object.post_id)
            form.categories.add(category)

        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Add', action=f'Post added: {form.title}')
        act.save()
        # messages.success(self.request, 'Post was successfully added')
        return redirect('content:s_home')

    def form_invalid(self, form, *args, **kwargs):
        # print(self.request.POST)
        # print(form.errors)
        # messages.success(self.request, 'Post was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/post.html', {'form': form})


class UpdatePost(LoginRequiredMixin, UpdateView):

    model = Post
    form_class = PostForm
    template_name = 'forms/update_post.html'
    slug_field = 'post_id'
    slug_url_kwarg = 'post_id'
    success_url = reverse_lazy('content:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        categories = self.request.POST.getlist('categories')
        # print(categories)
        form = form.save(commit=False)
        # categories = form.categories

        if form.lead:
            try:
                leads = Post.objects.filter(lead=True)
                for lid in leads:
                    lid.lead = False
                    lid.save()
            except ObjectDoesNotExist:
                pass
        form.save()
        all_cat = PostCategory.objects.all()
        c_in_rem = Post.objects.get(post_id=self.object.post_id)
        for c in c_in_rem.categories.all():
            c_in_rem.categories.remove(c)

        for i in categories:
            try:
                category = PostCategory.objects.get(id=i)
                c_in = Post.objects.get(post_id=self.object.post_id)
                # print(c_in)
                if category in c_in.categories.all():
                    pass
                else:
                    form.categories.add(category)
            except ObjectDoesNotExist:
                pass

        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Post updated: {form.title}')
        act.save()
        # messages.success(self.request, 'Post was successfully updated')
        return redirect('content:s_home')

    def form_invalid(self, form, *args, **kwargs):
        # print(form.errors)

        return render(self.request, 'forms/update_post.html', {'form':form})


class DeletePost(LoginRequiredMixin, DeleteView):

    model = Post
    template_name = 'forms/delete_post.html'
    slug_field = 'post_id'
    slug_url_kwarg = 'post_id'
    success_url = reverse_lazy('content:s_home')


class AddPostImage(LoginRequiredMixin, CreateView):

    model = PostImage
    form_class = PostImageForm
    template_name = 'forms/post-img.html'

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save()
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Add', action=f'Post Image category added: {form.title}')
        act.save()
        # messages.success(self.request, 'Post category was successfully added')
        return redirect('content:s_home')

    def form_invalid(self, form, *args, **kwargs):
        # messages.success(self.request, 'Post category was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/post-category.html', {'form': form})


class UpdatePostImage(LoginRequiredMixin, UpdateView):

    model = PostImage
    form_class = PostImageForm
    template_name = 'forms/update_post_img.html'
    success_url = reverse_lazy('content:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save()
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Post image category updated: {form.title}')
        act.save()
        # messages.success(self.request, 'Post category was successfully updated')
        return redirect('content:s_home')


class DeletePostImage(LoginRequiredMixin, DeleteView):

    model = Post
    template_name = 'forms/delete_post_img.html'
    success_url = reverse_lazy('content:s_home')


class AddPostCat(LoginRequiredMixin, CreateView):

    model = PostCategory
    form_class = PostCatForm
    template_name = 'forms/post-cat.html'

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save()
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Add', action=f'Post category added: {form.name}')
        act.save()
        # messages.success(self.request, 'Post category was successfully added')
        return redirect('content:s_home')

    def form_invalid(self, form, *args, **kwargs):
        # messages.success(self.request, 'Post category was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/post-category.html', {'form': form})


class UpdatePostCat(LoginRequiredMixin, UpdateView):

    model = PostCategory
    form_class = PostCatForm
    template_name = 'forms/update_post_cat.html'
    success_url = reverse_lazy('content:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save()
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Post category updated: {form.name}')
        act.save()
        # messages.success(self.request, 'Post category was successfully updated')
        return redirect('content:s_home')


class DeletePostCat(LoginRequiredMixin, DeleteView):

    model = Post
    template_name = 'forms/delete_post_cat.html'
    success_url = reverse_lazy('content:s_home')


class AddSlide(LoginRequiredMixin, CreateView):

    model = Slide
    form_class = Slide
    template_name = 'forms/slide.html'
    success_url = reverse_lazy('content:s-home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save(commit=False)
        try:
            lead = Slide.objects.filter(index=form.index)
            leads = Slide.objects.filter(index__gte=form.index)
            for lid in leads:
                lid.index += 1
        except ObjectDoesNotExist:
            pass

        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Add', action=f'Slide added: {form.title}')
        act.save()
        # messages.success(self.request, 'Slide was successfully added')
        return redirect('content:s-home')

    def form_invalid(self, form, *args, **kwargs):
        # print(self.request.POST)
        # print(form.errors)
        # messages.success(self.request, 'Slide was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/post.html', {'form': form})


class UpdateSlide(LoginRequiredMixin, UpdateView):

    model = Slide
    form_class = SlideForm
    template_name = 'forms/update_slide.html'
    success_url = reverse_lazy('content:s-home')


class DeleteSlide(LoginRequiredMixin, DeleteView):

    model = Slide
    template_name = 'forms/delete_slide.html'
    success_url = reverse_lazy('content:s-home')


class FirstnameUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = FirstnameChangeForm
    template_name = 'forms/firstname-update.html'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'first name updated for {self.object}')
        act.save()
        return reverse('content:staff_detail', kwargs={'uid': self.object.id})


class SurnameUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = SurnameChangeForm
    template_name = 'forms/surname-update.html'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Surname updated for {self.object}')
        act.save()
        return reverse('content:staff_detail', kwargs={'uid': self.object.id})

# ------------------------ Update Student -----------------------


class TitleUpdate(LoginRequiredMixin, UpdateView):

    model = Author
    form_class = TitleChangeForm
    template_name = 'forms/title-update.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Title updated for {self.object}')
        act.save()
        return reverse('content:staff_detail', kwargs={'uid': self.object.uid})
