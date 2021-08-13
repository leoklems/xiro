from django.urls import path

from .views import *
app_name = 'content'

urlpatterns = [

    path('', Home.as_view(), name='home'),
    path('post-detail/<post_id>/', PostDetailView.as_view(), name='post'),
]

