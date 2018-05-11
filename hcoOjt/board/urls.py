from django.conf.urls import url
from board.views import *

urlpatterns = [
    # Class-based views
    url(r'^$', PostLV.as_view(), name='index'),
    url(r'^posts/$', PostLV.as_view(), name='post_list'),
    url(r'^posts/(?P<slug>[-\w]+)/$', PostDV.as_view(), name='post_detail'),
]
