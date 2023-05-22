from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars',
                               null=True,
                               blank=True)
    # user = models.OneToOneField(to=User, on_delete=models.CASCADE)


class TagManager(models.Manager):
    def order_by_popular(self):
        return self.order_by('-count')


class Tag(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    objects = TagManager()


class QuestionManager(models.Manager):
    def order_by_date(self):
        return self.order_by('-ask_date')

    def order_by_rating(self):
        return self.order_by('-rating', '-answers_count')

    def get_by_tag(self, tag):
        return self.filter(tags__name__icontains=tag)

    def get_by_id(self, id):
        return self.get(pk=id)


class Question(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField()
    ask_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to=Tag)
    answers_count = models.IntegerField(default=0) #
    rating = models.IntegerField(default=0) #

    objects = QuestionManager()


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question).order_by('-rating')


class Answer(models.Model):
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    ask_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name='answers')
    rating = models.IntegerField(default=0)  #

    objects = AnswerManager()


class AnswerLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_like = models.BooleanField()


class QuestionLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_like = models.BooleanField()

# class Like(models.Model):
#     LIKE = 'L'
#     DISLIKE = 'D'
#     ESTIMATION_CHOICES = [
#         (LIKE, 'L'),
#         (DISLIKE, 'D'),
#     ]
#     estimation = models.CharField(max_length=1, choices=ESTIMATION_CHOICES)
#     question = models.ForeignKey(to=Question,
#                                  on_delete=models.CASCADE,
#                                  null=True,
#                                  blank=True)
#     answer = models.ForeignKey(to=Answer,
#                                on_delete=models.CASCADE,
#                                null=True,
#                                blank=True)
#     profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
#
#     objects = LikeManager()


# def new_questions():
#     return Question.objects.order_by('ask_date')
#
#
# def tag_questions(tag_id):
#     return Question.objects.filter(tags__id=tag_id)
#
#
# def get_questions(get, tag_id=None):
#     try:
#         questions = get() if tag_id is None else get(tag_id)
#     except TypeError as e:
#         print('Error with getting question: ', e)
#         return
#
#     return [[q, Answer.objects.answers_count(q.id), Like.objects.question_likes_count(q.id), q.tags.all()] for q in
#             questions]
#
#
# def get_hot_questions():
#     return sorted(get_questions(new_questions), key=lambda question: question[2], reverse=True)
#
#
# def get_question_with_counts(question_id):
#     question = Question.objects.get(id=question_id)
#     return [question, Like.objects.question_likes_count(question_id), question.tags.all()]
#
#
# def get_answers(question_id):
#     try:
#         answers = Answer.objects.filter(question_id=question_id)
#     except TypeError as e:
#         print('Error with getting answers: ', e)
#         return
#     return sorted([[answer, Like.objects.answer_likes_count(answer.id)] for answer in answers],
#                   key=lambda answer: answer[1], reverse=True)
