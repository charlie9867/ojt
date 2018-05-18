from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Boards(models.Model):
    name_id = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 50, db_column='제목')
    text = models.TextField(max_length = 230, db_column='내용', help_text='메모 내용은 230자 이내로 입력 가능합니다.')
    trans_text = models.TextField(max_length = 230, db_column='번역 결과')
    lang = models.CharField(max_length = 10, db_column='언어')
    update_date = models.DateTimeField()
    priority = models.BooleanField(db_column='중요')

    def generate(self):
        self.update_date = timezone.now()
        self.save()


    def __str__(self):
        return '%s by %s' % (self.title, self.name_id)


class Comment(models.Model):
    board = models.ForeignKey('board.Boards', related_name='comments')
    name_id = models.CharField(max_length = 50, db_column='아이디')
    text = models.TextField(max_length = 50, db_column='내용')
    created_date = models.DateTimeField()

    def generate(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text
