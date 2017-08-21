from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('owner','id', 'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')

owner = serializers.ReadOnlyField(source='owner.username')




class MyAuthTokenSerializer(AuthTokenSerializer):
    """
    custom Serializer that check request auth info
    """

    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    raise serializers.ValidationError(
                       detail={'username': {'message': u'用户未启用', 'code': '1'}},
                       code='authorization')
            else:
                raise serializers.ValidationError(
                    detail={'username': {'message': u'用户名或密码不正确', 'code': '2'}},
                    code='authorization')
        else:
            raise serializers.ValidationError(
                detail={'username': {'message': u'必须有用户名或密码', 'code': '3'}},
                code='authorization')

        attrs['user'] = user
        return attrs

