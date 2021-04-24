from django.urls import path, include
from .views import (
    index,

    quiz_create, quiz_edit, quiz_run, quiz_remove,
    add_question, edit_question, remove_question
    
    # results_view
)

app_name = 'quizz_app'

urlpatterns = [
    # Quiz related urls
    path('', index, name='index'),
    path('quiz_create', quiz_create, name='quiz_create'),
    path('quiz_edit/<int:quiz_id>', quiz_edit, name='quiz_edit'),
    path('quiz_run/<int:quiz_id>', quiz_run, name='quiz_run'),
    path('quiz_remove/<int:quiz_id>', quiz_remove, name='quiz_remove'),

    # Questions related urls
    path('question_add/<int:quiz_id>', add_question, name='add_question'),
    path('question_edit/<int:question_id>', edit_question, name='edit_question'),
    path('question_remove/<int:question_id>/<int:quiz_id>', remove_question, name='remove_question'),

    # Results
    # path('results/<int:corrects>', results_view, name='results')
]
