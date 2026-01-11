"""Модуль с контроллерами для квизов."""

from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from quiz.models import Quiz
from quiz.serializers import QuestionSerializer, QuizSerializer
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    quiz_service = QuizService()
    question_service = QuestionService()

    @action(detail=True, url_path='random_question', methods=['get'])
    def random_question(self, request: HttpRequest, pk: str):
        question = self.question_service.random_question_from_quiz(int(pk))
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    @action(detail=False, url_path='by_title/(?P<title>.+)', methods=['get'])
    def by_title(self, request: HttpRequest, title: str):
        quizzes = self.quiz_service.get_quizes_by_title(title)
        serializer = self.get_serializer(quizzes, many=True)
        return Response(serializer.data)
