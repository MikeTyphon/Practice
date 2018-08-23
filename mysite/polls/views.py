from django.shortcuts import render

from django.http import HttpResponse

from .models import Question

from django.http import Http404

# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index! Awww yeah bay beeeee!!")

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     HttpResponse(output)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # try:
    # 	question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    # 	raise Http404("Question does not exist")#this raises the Http404 exception if a question with the requested ID doesn't exist. 

    # the previous code was replaced in order to make use of the more efficient get_object_or_404() method. See the following

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/index.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s.")