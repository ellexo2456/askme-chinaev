from django.db import models

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
