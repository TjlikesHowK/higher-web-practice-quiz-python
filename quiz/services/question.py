"""Модуль с реализацией сервиса вопросов"""

import random

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuestionService
from quiz.models import Question
from quiz.services.quiz import QuizService
from quiz.services.utils import update_object


class QuestionService(AbstractQuestionService):
    """Реализация сервиса доступа к БД вопросов"""

    def __init__(self) -> None:
        self.quiz_service = QuizService()

    def list_questions(self):
        return Question.objects.all()

    def get_questions_for_quiz(self, quiz_id: int):
        return Question.objects.filter(quiz_id=quiz_id).all()

    def get_question(self, question_id: int):
        return get_object_or_404(Question, id=question_id)

    def get_questions_by_text(self, text: str):
        return Question.objects.filter(text__icontains=text).all()

    def create_question(self, quiz_id: int, data: dict):
        return Question.objects.create(quiz_id=quiz_id, **data)

    def update_question(self, question_id: int, data: dict):
        return update_object(Question, question_id, data)

    def delete_question(self, question_id: int):
        question = self.get_question(question_id)
        question.delete()

    def check_answer(self, question_id: int, answer: str):
        question = self.get_question(question_id)

        try:
            correct_option = question.options[question.correct_answer]
        except (IndexError, TypeError):
            return False

        return correct_option == answer

    def random_question_from_quiz(self, quiz_id: int):
        questions = Question.objects.filter(quiz_id=quiz_id).all()
        return random.choice(questions)
