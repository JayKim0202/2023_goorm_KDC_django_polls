from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


class Question(models.Model):  # DB Table for 설문조사 주제
    question_text = models.CharField(max_length=200)  # 설문조사 주제 텍스트
    # 'date published': 관리자 페이지에서 보여질 항목명
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    # 관리자 페이지 Question 리스트에서 Tru/False 문구를 아이콘으로 변경
    was_published_recently.boolean = True
    # 'WAS PUBLISHED RECENTLY' 열의 정렬 기준을 pub_date(설문조사 주제 생성 시간)로 세팅
    was_published_recently.admin_order_field = 'pub_date'
    # 'WAS PUBLISHED RECENTLY' 열의 이름 변경
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):  # DB Table for 설문조사 주제에 대한 선택지 (+ 선택지마다의 득표 수)
    # 자동으로 Question table의 Primary key를 Foreign Key로 세팅
    # on_delete=models.CASCADE: Question(질문) 항목 삭제 시 관계된 선택지들도 모두 자동 삭제
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)  # 설문조사 제주의 id 값
    choice_text = models.CharField(max_length=200)  # 설문조사 주제에 대한 선택지 텍스트
    votes = models.IntegerField(default=0)  # 선택지에 대한 득표 수

    def __str__(self):
        return self.choice_text
