from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import random

from authe.models import Author
from .models import Quiz, Question, Answer
from .forms import (
    QuizCreateForm, QuestionCreateForm, AnswerCreateForm,
    QuizForm
)

# Main view


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

# Quiz views


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
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.all()

    # Changing values in quiz objects
    if request.GET:
        quiz.title = request.GET['title']
        quiz.description = request.GET['text']
        quiz.save()

    return render(request, 'quiz_edit.html', {
        'quiz': quiz, 'questions': questions
    })


def quiz_run(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).last()
    questions = quiz.questions.all()

    if request.GET:
        vals = dict(request.GET)

        result = 0
        for answer_item in vals.items():
            answer = Answer.objects.get(id=answer_item[1][0])
            if answer.correct == True:
                result += 1

        result = "%s / %d" % (result,
                            len(Question.objects.filter(quiz_id=quiz_id)))
        
        return render(request, 'results.html', {'result': result, 'quiz': quiz,})

    return render(request, 'quiz_run.html', {
        'quiz': quiz,
        'questions': questions
    })


def quiz_remove(request, quiz_id):
    quiz_remove = Quiz.objects.filter(id=quiz_id).last().delete()
    return redirect('quizz_app:index')

# Question views


def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    answers = ['gridRadios1', 'gridRadios2', 'gridRadios3', 'gridRadios4']

    if request.POST:

        question = Question.objects.create(
            body=request.POST['question_body'],
            quiz=Quiz.objects.filter(id=quiz_id).last()
        )

        for i in range(1, 5):
            choice = 'gridRadios'+str(i)
            correct = 'on' == request.POST.get(choice)
            answer = 'answer'+str(i)

            Answer.objects.create(
                question_id=question.id,
                body=request.POST[answer],
                correct=correct
            )
        return redirect('quizz_app:quiz_edit', quiz_id=quiz_id)

    return render(request, 'add_question.html', {
        'quiz': quiz,
    })


def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)

    if request.POST:
        vals = dict(request.POST)
        print(vals)

        question.body = vals['question_body'][0]
        # question.save()

        answers_list = Answer.objects.filter(question_id=question_id)
        for answer_body, answer in zip(vals['answers'], answers_list):
            answer.body = answer_body
            answer.correct = False
            answer.save()
            print(answer)

        try:
            for answer_id in vals['corrects']:
                answer = Answer.objects.get(id=answer_id)
                answer.correct = True
                answer.save()
        except:
            None

    return render(request, 'edit_question.html', {'question': question})


def remove_question(request, question_id, quiz_id):
    Question.objects.get(id=question_id).delete()

    return redirect('quizz_app:quiz_edit', quiz_id=quiz_id)