from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from TaskManager.sleep import Sleep_Detector
from TaskManager.sleep import Blink_Detector
from TaskManager.sleep import sleep_Blink_Detector

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect , get_object_or_404

from django.utils import timezone
from .forms import UserForm
from .models import Question
from .forms import QuestionForm, AnswerForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('signup')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, '404.html', {})


# Create your views here.
def main(req):
    context = {

    }
    return render(req, "main.html", context=context)


def about(req):
    context = {

    }
    return render(req, "about.html", context=context)


def Task_Manager(req):
    context = {

    }
    return render(req, "TaskManager.html", context=context)


def Drowsiness(req):
    context = {

    }
    return render(req, "Drowsiness.html", context=context)


def Blinking(req):
    context = {

    }
    return render(req, "Blinking.html", context=context)

def question_list(req):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(req, "question_list.html", context=context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
# ---------------------------------- [edit] ---------------------------------- #
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'question_detail.html', context)




def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'question_form.html', context)




def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def task_manager(request):
    return StreamingHttpResponse(gen(sleep_Blink_Detector()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def sleep_detector(request):
    return StreamingHttpResponse(gen(Sleep_Detector()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def blink_detector(request):
    return StreamingHttpResponse(gen(Blink_Detector()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
