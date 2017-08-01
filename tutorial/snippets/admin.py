from django.contrib import admin
from .models import User,Teacher
# Register your models here.
from .models import Snippet

admin.site.register(Snippet)
admin.site.register(User)
admin.site.register(Teacher)