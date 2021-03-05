from django.db import models

# Create your models here.



# ======== Викторина \ Тест ========
class Quiz(models.Model): 
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField()

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'




# ======== Вопрос ========
class Question(models.Model): 
    question = models.CharField(max_length=128)
    quiz = models.ForeignKey(Quiz, related_name='quiestions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'




# ======== Ответ ========
class Answer(models.Model): 
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    body = models.CharField(max_length=256)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'