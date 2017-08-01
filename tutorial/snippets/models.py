from django.db import models

# Create your models here.
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, UserManager)
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    class Meta:
        ordering = ('created',)

class User(AbstractBaseUser):
    """
    用户/学生模型
    """
    username = models.CharField(max_length=30, unique=True, primary_key=True)
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    grade = models.CharField(max_length=30, null=True)
    student_id = models.CharField(max_length=30, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'


class Teacher(AbstractBaseUser):
    """
    教师模型 
    """
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50)


    USERNAME_FIELD = 'username'


# token = Token.objects.create(user=...)
# print token.key

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    create a auth token for every User 
    """
    if created:
        Token.objects.create(user=instance)


# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)