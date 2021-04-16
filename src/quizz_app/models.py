from django.db import models

from authe.models import Author

# Create your models here.


# ======== Викторина \ Тест ========
class Quiz(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=False)
    user = models.ForeignKey(
        Author, related_name='quizes', on_delete=models.CASCADE)
    img_url = models.CharField(blank=True, max_length=1024)

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'

    def __str__(self):
        return self.title

    def possible(self):
        total = 0
        for question in self.question_set.all():
            question.save()
            total += question.value
        return total


# ======== Вопрос ========
class Question(models.Model):
    body = models.CharField(max_length=128)
    quiz = models.ForeignKey(
        Quiz, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.body


# ======== Ответ ========
class Answer(models.Model):
    question = models.ForeignKey(
        Question, related_name='answers', on_delete=models.CASCADE)
    body = models.CharField(max_length=256)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.body
