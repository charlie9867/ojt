from django.conf.urls import include, url
from django.contrib import admin
from board import views
from django.contrib.auth import views as auth_views



urlpatterns = [

    # 관리자 페이지
    url(r'^admin/', admin.site.urls),
    # 메인 페이지
    url(r'^$', views.index, name='index'),
    # 게시판 추가
    url(r'^new/$', views.post, name='new_board'),
    # 개사판 상세
    url(r'^(?P<user>[0-9]+)/view/$', views.viewBoard, name='view_board'),
    # 게시판 수정
    url(r'^(?P<user>[0-9]+)/modify/$', views.modify, name='modify_board'),
    # 개사펀 삭제
    url(r'^(?P<user>[0-9]+)/delete/$', views.delete, name='delete_board'),
    # 로그인을 위한 관리자 auth_url을 추가
    url('^', include('django.contrib.auth.urls')),
    # 회원가입
    url(r'^join/$', views.signup, name='join'),
    # CAPCHA API
    url(r'^join/captcha/$', views.getCapchaKey, name="getCapchaKey"),
    # 로그아웃
    url(r'^logout/$', auth_views.logout, {'next_page' : '/board/logout.html'}),
    # 로그인
    url(r'^login/$', auth_views.login,  {'template_name':'board/login.html'}),
    # Papago NMT API
    url(r'^new/trans/$', views.transText, name="transText"),

    url(r'^(?P<user>[0-9]+)/view2/$', views.viewBoard2, name='view_board2'),
    url(r'^(?P<user>[0-9]+)/comment/$', views.postComment, name='post_comment'),
]
