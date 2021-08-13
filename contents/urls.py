from django.urls import path

from .views import *
app_name = 'content'

urlpatterns = [

    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('', Home.as_view(), name='home'),
    path('posts/', Posts.as_view(), name='posts'),
    path('post-detail/<post_id>/', PostDetailView.as_view(), name='post'),

    path('admin-home/', AdminHome.as_view(), name='s_home'),
    path('staff/', AdminStaff.as_view(), name='s_staff'),
    path('admin-posts/', AdminPosts.as_view(), name='s_posts'),
    path('post-images/', PostImages.as_view(), name='post_images'),
    path('staff-detail/<uid>/', StaffDetailView.as_view(), name='staff_detail'),
    path('staff-activities/<uid>/', StaffActivities.as_view(), name='staff_activities'),
    path('delete-staff/<uid>/', DeleteStaff.as_view(), name='delete_staff'),

    path('a-post-detail/<post_id>/', AdminPostDetailView.as_view(), name='a_post'),
    path('a-slide-detail/<pk>/', AdminSlideDetailView.as_view(), name='a_slide'),
    path('add-user/', AuthorRegistration.as_view(), name='add_staff'),

    path('add-post', AddPost.as_view(), name='add_post'),
    path('update-post/<post_id>/', UpdatePost.as_view(), name='update_post'),
    path('delete-post/<post_id>/', DeletePost.as_view(), name='delete_post'),

    path('add-post-image', AddPostImage.as_view(), name='add_post_img'),
    path('update-post-image/<pk>/', UpdatePostImage.as_view(), name='update_post_img'),
    path('delete-post-image/<pk>/', DeletePostImage.as_view(), name='delete_post_img'),

    path('add-post-category', AddPostCat.as_view(), name='add_post_cat'),
    path('update-post-category/<pk>/', UpdatePostCat.as_view(), name='update_post_cat'),
    path('delete-post-cat/<pk>/', DeletePostCat.as_view(), name='delete_post_cat'),

    path('add-slide/', AddSlide.as_view(), name='add_slide'),
    path('update-slide/<pk>/', UpdateSlide.as_view(), name='update_slide'),
    path('delete-slide/<pk>/', DeleteSlide.as_view(), name='delete_slide'),

    path('update-first-name/<pk>/', FirstnameUpdate.as_view(), name='update_first_name'),
    path('update-surname/<pk>/', SurnameUpdate.as_view(), name='update_surname'),
    path('update-staff-title/<uid>/', TitleUpdate.as_view(), name='update_staff_title'),
]

