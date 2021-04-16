from django.urls import path, include
from .views import (
    index,

    quiz_create, quiz_edit, quiz_run,
    add_question,
)

app_name = 'quizz_app'

urlpatterns = [
    # Quiz related urls
    path('', index, name='index'),
    path('quiz_create', quiz_create, name='quiz_create'),
    path('quiz_edit/<int:quiz_id>', quiz_edit, name='quiz_edit'),
    path('quiz_run/<int:quiz_id>', quiz_run, name='quiz_run'),

    # Questions related urls
    path('add_question/<int:quiz_id>', add_question, name='add_question'),
]
