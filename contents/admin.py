from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Author)
admin.site.register(Activity)
admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Slide)
