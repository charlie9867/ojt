# -*- coding: utf-8 -*-
#!/usr/bin/python
import os, sys
import urllib.request

from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

# Create your views here.
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from .models import Boards
from .models import Comment
from .forms import ViewForm
from .forms import PostForm
from .forms import UserForm
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import login, views
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



# from HTMLParser import HTMLParser
def index(request):
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print('this is main')
    sort = request.GET.get('sort','')
    if sort == 'date_end':
        board = Boards.objects.order_by('update_date')
        return render(request, 'board/index.html', {'boards' : board})
    elif sort == 'mypost':
        user = request.user
        board = Boards.objects.filter(name_id = user).order_by('-update_date') #복수를 가져올수 있음
        return render(request, 'board/index.html', {'boards' : board})
    else:
        board = Boards.objects.order_by('-update_date')
        return render(request, 'board/index.html', {'boards' : board})

# 글 입력 및 저장
def post(request):
    if request.method == "POST":
        #저장
        form = PostForm(request.POST)
        if form.is_valid():
            board = form.save(commit = False)
            board.name_id = User.objects.get(username = request.user.get_username())
            board.generate()
            return redirect('index')
    else:
        #입력
        form = PostForm()
        return render(request, 'board/form.html',{'form': form})

# 글 상세보기
def viewBoard(request, user):
    if user != "":
        board = Boards.objects.get(pk = user)
        return render(request, 'board/view.html', {'board' : board})
    else:
        return redirect('index')

# 글 상세보기
def viewBoard2(request, user):
    board = Boards.objects.get(pk = user)
    comments = Comment.objects.filter(board = user)
    form = ViewForm()
    return render(request, 'board/view2.html', {'board' : board, 'form': form, 'comments': comments})

def postComment(request, user):
    if request.method == "POST":
        form = ViewForm(request.POST)
        board = Boards.objects.get(pk = user)
        comments = Comment.objects.filter(board = user)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.name_id = User.objects.get(username = request.user.get_username())
            comment.generate()
            form = ViewForm()
            return render(request, 'board/view2.html', {'board' : board, 'form': form, 'comments': comments})
    else:
        return redirect('index')


# 글 수정 및 저장
def modify(request, user):
    if request.method == "POST":
        #수정 저장
        board = Boards.objects.get(pk = user)
        form = PostForm(request.POST, instance=board)
        if form.is_valid():
             form.save()
             return redirect('index')
    else:
        #수정 입력
        board = Boards.objects.get(pk = user)
        if board.name_id == User.objects.get(username = request.user.get_username()):
            board = Boards.objects.get(pk = user)
            form = PostForm(instance = board)
            return render(request, 'board/modify.html', {'board' : board, 'form' : form})
        else:
            return render(request, 'board/warning.html')

# 글 삭제
def delete(request, user):
    board = Boards.objects.get(pk = user)
    if board.name_id == User.objects.get(username = request.user.get_username()):
        board.delete()
        return redirect('index')

    else:
        return render(request, 'board/warning.html')

# 회원가입
@csrf_exempt
def signup(request):

    if request.method == "POST":
        form = UserForm(request.POST)

        # 네이버 캡차 API 값 비교
        client_id = "sfa0nzbfho"
        client_secret = "B1fgAkU3c9FU7hq2ifpu7toRv9u04lc72ZpoSwlO"
        key = request.POST.get('checkCaptcha')
        value = request.POST.get('captchaVal')

        url = "https://naveropenapi.apigw.ntruss.com/captcha/v1/nkey?code=1&key=" + key + "&value=" + value
        requestUrl = urllib.request.Request(url)
        requestUrl.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        requestUrl.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(requestUrl)
        rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))

            if (result['result'] == False):
                return render(request, 'board/adduser.html', {'form': form})
        else:
            print("Error Code:" + rescode)
            return render(request, 'board/adduser.html', {'form': form})

        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_user)

            return redirect('index')
        else:
            return HttpResponse('사용자명이 이미 존재합니다.')
    else:
        form = UserForm()
        return render(request, 'board/adduser.html', {'form': form})


# 네이버 캡차 API 키발급
@csrf_exempt
def getCapchaKey(request):
    print("hello")
    client_id = "sfa0nzbfho"
    client_secret = "B1fgAkU3c9FU7hq2ifpu7toRv9u04lc72ZpoSwlO"
    code = "0"
    url = "https://naveropenapi.apigw.ntruss.com/captcha/v1/nkey?code=" + code
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
        getCaptchaImg(result)
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        print("Error Code:" + rescode)

# 네이버 캡차 API 이미지수신
@csrf_exempt
def getCaptchaImg(requestVal):
    client_id = "sfa0nzbfho"
    key = requestVal['key'] # 캡차 Key 값
    url = "https://naveropenapi.apigw.ntruss.com/captcha-bin/v1/ncaptcha?key=" + key + "&X-NCP-APIGW-API-KEY-ID=" + client_id;
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        with open('/opt/hco_test/static/image/captcha/'+key+'.jpg', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)

# 파파고 API
def transText(request):
    client_id = "sfa0nzbfho"
    client_secret = "B1fgAkU3c9FU7hq2ifpu7toRv9u04lc72ZpoSwlO"
    encText = urllib.parse.quote(request.POST.get('trans_text'))
    lang = urllib.parse.quote(request.POST.get('lang'))
    data = "source=ko&target=" + lang + "&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        print(result)
        return HttpResponse(result, content_type='application/json')
    else:
        print("Error Code:" + rescode)
        result = response_body.decode('utf-8')
        print(result)
        return HttpResponse(json.dumps(result), content_type='application/json')
