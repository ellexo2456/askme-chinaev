from django.db import models

QUESTIONS = [
    {
        'id': question_id,
        'title': f'Question {question_id}',
        'text': f'Text of question {question_id}',
        'answers_number': question_id * question_id,

    } for question_id in range(1, 10)
]
