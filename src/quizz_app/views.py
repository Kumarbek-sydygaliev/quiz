from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from authe.models import Author
from .models import Quiz, Question, Answer
from .forms import (
    QuizCreateForm, QuestionCreateForm, AnswerCreateForm,
    QuizForm
)

# Create your views here.


def index(request):
    quizes = list(Quiz.objects.all())
    result = []
    for i in quizes[::2]:
        try:
            j = quizes[quizes.index(i) + 1]
            result.append([i, j])
        except:
            result.append([i])
    return render(request, 'index.html', {'quizes': result})


@login_required(login_url='/auth/login/')
def quiz_create(request):
    form = QuizCreateForm
    if request.GET:
        new_quiz = Quiz.objects.create(
            title=request.GET['title'],
            description=request.GET['description'],
            user=Author.objects.filter(id=request.user.id).last(),
            img_url=request.GET['url']
        )
        new_quiz.save()

        return redirect('quizz_app:index')
    return render(request, 'quiz_create.html', {'form': form})


def quiz_edit(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).last()

    # Changing values in quiz objects
    if request.GET:
        quiz_change = Quiz.objects.filter(id=quiz_id).last()
        # print(request.GET['title'])
        quiz_change.title = request.GET['title']
        quiz_change.description = request.GET['text']
        quiz_change.save()
    return render(request, 'quiz_edit.html', {'quiz': quiz})


def quiz_run(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).last()
    questions = quiz.questions.all()

    return render(request, 'quiz_run.html', {
        'quiz': quiz,
        'questions': questions
    })


def add_question(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).last()

    if request.GET:
        new_question = Question.objects.create(
            body=request.GET['body'],
            quiz=quiz,
        )
        new_question.save()

    return render(request, 'add_question.html', {
        'quiz': quiz,
    })
