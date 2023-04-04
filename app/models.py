from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars',
                               null=True,
                               blank=True)
    # user = models.OneToOneField(to=User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class QuestionManager(models.Manager):
    def butch_by_data(self, begin, end):
        return self.order_by('ask_date').filter(id__range=(begin, end))


class Question(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField()
    aks_date = models.DateField(auto_now_add=True)
    # correct_answer = models.OneToOneField(to='Answer',
    #                                       on_delete=models.SET_NULL,
    #                                       null=True,
    #                                       blank=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to=Tag)


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField(default=False)
    aks_date = models.DateField(auto_now_add=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)


class Like(models.Model):
    LIKE = 'L'
    DISLIKE = 'D'
    ESTIMATION_CHOICES = [
        (LIKE, 'L'),
        (DISLIKE, 'D'),
    ]
    estimation = models.CharField(max_length=1, choices=ESTIMATION_CHOICES)
    question = models.ForeignKey(to=Question,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    answer = models.ForeignKey(to=Answer,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)


QUESTIONS = [
    {
        'id': question_id,
        'title': f'Question {question_id}',
        'text': f'Text of question {question_id}',
        'answers_number': question_id * question_id,
        'likes_count': question_id,
    } for question_id in range(1, 100)
]

ANSWERS = [
    {
        'id': answer_id,
        'text': f'Text of answer {answer_id}',
        'answers_number': answer_id * answer_id,
        'likes_count': answer_id,
        'avatar_path': f'img/avatar-{answer_id}.jpg',
    } for answer_id in range(2, 4)
]
