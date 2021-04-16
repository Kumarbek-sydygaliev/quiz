from django import forms
from .models import Quiz, Question, Answer


# -------- Quiz --------
class QuizCreateForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    image = forms.ImageField(required=True)

    class Meta:
        model = Quiz
        fields = ('title', 'description', 'image')


# -------- Question --------
class QuestionCreateForm(forms.Form):
    body = forms.CharField(required=True)
    quiz = forms.ChoiceField(required=True)

    class Meta:
        model = Question
        fields = ('body', 'quiz')



# -------- Answer --------
class AnswerCreateForm(forms.Form):
    body = forms.CharField(required=True)
    question = forms.ChoiceField(required=True)
    correct = forms.BooleanField(required=True)

    class Meta:
        model = Answer
        fields = ('body', 'question', 'correct')


# -------- Quiz questions form ----------
class QuizForm(forms.Form):
    def __init__(self, data, questions, *args, **kwargs):
        self.questions = questions
        for question in questions:
            field_name = "question_%d" % question.pk
            choices = []
            for answer in question.answer_set().all():
                choices.append((answer.pk, answer.answer,))
            ## May need to pass some initial data, etc:
            field = forms.ChoiceField(label=question.question, required=True, 
                                      choices=choices, widget=forms.RadioSelect)
        return super(QuizForm, self).__init__(data, *args, **kwargs)
        