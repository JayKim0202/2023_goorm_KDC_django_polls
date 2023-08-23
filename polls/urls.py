from django.urls import path
from . import views  # 같은 폴더 내의 views.py를 import

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),  # 127.0.0.1:8000/polls/
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/results/', views.results, name='results'),
]
