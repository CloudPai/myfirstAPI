from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# from snippets import views
from rest_framework.authtoken import views
from .views import SnippetList,SnippetDetail,UserList,UserDetail
from django.conf.urls import include
urlpatterns = [
    url(r'^snippets/$', SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', SnippetDetail.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    # url(r'^register/$',),
    url(r'^api-token-auth/', views.obtain_auth_token), # 获取token
]

urlpatterns = format_suffix_patterns(urlpatterns)
