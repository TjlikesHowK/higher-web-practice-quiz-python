"""Модуль с реализацией сервиса квизов"""

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuizService
from quiz.models import Quiz
from quiz.services.utils import update_object


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза"""

    def list_quizzes(self):
        return Quiz.objects.all()

    def get_quiz(self, quiz_id: int):
        return get_object_or_404(Quiz, id=quiz_id)

    def get_quizes_by_title(self, title: str):
        return Quiz.objects.filter(title__icontains=title).all()

    def create_quiz(self, data: dict):
        return Quiz.objects.create(**data)

    def update_quiz(self, quiz_id: int, data: dict):
        return update_object(Quiz, quiz_id, data)

    def delete_quiz(self, quiz_id: int):
        quiz = self.get_quiz(quiz_id)
        quiz.delete()
