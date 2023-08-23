from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Question

# Create your views here.


def index(request):
    # order_by('-pub_date')[:5] : 등록 날짜 기준 내림차순 정렬 후 5개까지만
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # html에 넘기는 dict를 context라고 함
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     q = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question {} does not exist'.format(question_id))

    # list(QuerySet)가 return될 시에는 get_object_or_404 대신 get_list_or_404를 활용
    q = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/detail.html', {'question': q})


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice_select'])
        # request.POST['choice_select'] :
        # detail.html의 <input type="radio" name="choice_select" value="{{ choice.id}}">에서 날라온 값
        # form으로 제출된 POST Request 전체에서 'choice_select'가 name인 HTML 태그의 value를 꺼내는 코드
        # request.POST는 {~~~, 'choice_select':7}와 같은 dictionary 형태
    except:
        # request.POST['choice_select']가 없을 경우, error_message를 가지고 detail.html로 되돌아감
        context = {'question': question,
                   'error_message': "You didn't select a choice."}
        return render(request, 'polls/detail.html', context)
    else:  # try 문에서 에러가 발생하지 않았을 경우 마지막에 실행됩니다.
        selected_choice.votes += 1
        selected_choice.save()  # 실제 DB에 저장
        return redirect('polls:results', question_id=question.id)


def results(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/results.html', {'question': question})
