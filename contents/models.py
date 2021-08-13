from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Author(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    TITLE = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Ms', 'Ms'),
    )
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                related_name="student", blank=True)
    uid = models.SlugField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=GENDER, null=True, blank=True)
    title = models.CharField(max_length=7, default='', choices=TITLE, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default="media/profile_pix.png", null=True, blank=True)
    reg_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user}"


class Slide(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=300)
    index = models.IntegerField(unique=True, null=True, blank=True)
    link = models.CharField(max_length=50, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='slides/', default="media/lib_slider.jpg", blank=True, null=True)

    class Meta:
        ordering = ("index",)

    def __str__(self):
        return f"{self.title}"


class Post(models.Model):

    title = models.CharField(max_length=50)
    sub_heading = models.CharField(max_length=100)
    body = RichTextField()
    index = models.IntegerField(unique=True, null=True, blank=True)
    author = models.ForeignKey(Author, related_name='post_author', on_delete=models.CASCADE, null=True, blank=True)
    post_id = models.SlugField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='post/', default="media/blog.jpeg", blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def time_published(self):
        current = timezone.now()
        diff = current - self.date_added

        if diff.days == 0 and diff.seconds > 0and diff.seconds < 1:
            now = " just now "
            return now

        elif diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + " second ago "
            else:
                return str(seconds) + " seconds ago "

        elif diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            if diff.seconds < 120:
                return str(diff.seconds // 60) + " minute ago "
            else:
                return str(diff.seconds // 60) + " minutes ago "

        elif diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            if diff.seconds < 7200:
                return str(diff.seconds // 3600) + " hour ago "
            else:
                return str(diff.seconds // 3600) + " hours ago "

        elif diff.days >= 1 and diff.days < 30:
            if diff.days < 2:
                return str(1) + " day ago "
            else:
                return str(diff.days) + " days ago "

        elif diff.days >= 30 and diff.days < 365:
            if diff.days < 60:
                return str(diff.days // 30) + " month ago "
            else:
                return str(diff.days // 30) + " months ago "

        elif diff.days >= 365:
            if diff.days < 730:
                return str(diff.days // 365) + " year ago "
            else:
                return str(diff.days // 365) + " years ago "

    def __str__(self):
        return f"{self.title}"

