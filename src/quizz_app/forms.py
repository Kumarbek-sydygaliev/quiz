from django import forms
from .models import Quiz, Question, Answer


# -------- Quiz --------
class QuizCreateForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    class Meta:
        model = Quiz
        fields = ('title', 'despription', 'image')

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