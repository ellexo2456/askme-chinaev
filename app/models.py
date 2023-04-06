from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars',
                               null=True,
                               blank=True)
    # user = models.OneToOneField(to=User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=100)


# class QuestionManager(models.Manager):
#     def new_with_counts(self):
#
#
#         return questions_with_counts
#
#
class Question(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField()
    ask_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to=Tag)

    # objects = QuestionManager


class AnswerManager(models.Manager):
    def answers_count(self, question_id):
        return self.filter(question_id=question_id).count()


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField(default=False)
    ask_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    objects = AnswerManager()


class LikeManager(models.Manager):
    def likes_count(self, question_id):
        return self.filter(question_id=question_id).count()


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

    objects = LikeManager()


def new_questions():
    return Question.objects.order_by('ask_date')


def tag_questions(tag_id):
    return Question.objects.filter(tags__id=tag_id)


def get_questions(get, tag_id=None):
    try:
        questions = get() if tag_id is None else get(tag_id)
    except TypeError as e:
        print('Error with getting question: ', e)
        return

    questions_with_counts = []

    for q in questions:
        questions_with_counts.append(
            [q,
             Answer.objects.answers_count(q.id),
             Like.objects.likes_count(q.id),
             q.tags.all()])

    return questions_with_counts


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
