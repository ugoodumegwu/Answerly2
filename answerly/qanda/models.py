from django.db import models
from django.conf import settings
from django.urls import reverse


class Question(models.Model):

    title = models.CharField(max_length=150)
    question = models.TextField()
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('qanda:question_detail', kwargs={'pk': self.id})


    def can_accept_answers(self, user):
        return self.user == user

    def can_delete(self, user):
        return self.user==user


class Answer(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )

