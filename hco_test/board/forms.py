# -*- coding: utf-8 -*-
from django import forms
from .models import Boards
from .models import Comment
# 모델 클래스 Board로 부터 데이터를 입력 받을 폼을 작성한다.
from django.contrib.auth.models import User


class ViewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'board', 'text']
        widgets = {
            'board': forms.TextInput(attrs={'class': 'form-control', 'type':'hidden'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'50자 이내로 입력 가능합니다.'}),
        }
        labels = {
            'board': 'board',
            'text': '댓글',
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Boards
        choice = (
            ("en", "영어"),
            ("zh-CN", "중국어 간체"),
            ("zh-TW", "중국어 번체"),
            ("es", "스페인어"),
            ("fr", "프랑스어"),
            ("vi", "베트남어"),
            ("th", "태국어"),
            ("id", "인도네시아어"),
        )
        fields = ['title', 'text', 'lang', 'trans_text',  'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'230자 이내로 입력 가능합니다.'}),
            'lang': forms.Select(choices=choice, attrs={'type' : 'selectbox', 'id' : 'sort-select'}),
            'trans_text': forms.Textarea(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'priority': forms.CheckboxInput(attrs={'type' : 'checkbox'}),
        }
        labels = {
            'title': '제목',
            'text': '내용',
            'lang': '언어',
            'trans_text': '번역',
            'priority': '중요',
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'hco@naver.com'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'username': '아이디',
            'email': '이메일',
            'password': '패스워드',
        }
    # 글자수 제한
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__( *args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15
