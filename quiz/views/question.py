"""Модуль с контроллерами для вопросов."""

from django.http import HttpRequest
from django.http.response import json
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from quiz.models import Question
from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    service = QuestionService()

    @action(detail=False, url_path=r'by_text/(?P<query>.+)', methods=['get'])
    def by_text(self, request: HttpRequest, query: str):
        questions = self.service.get_questions_by_text(query)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path='check', methods=['post'])
    def check(self, request: HttpRequest, pk: str):
        answer = json.loads(request.body).get('user_answer', '')

        is_correct_answer = self.service.check_answer(int(pk), answer)
        return Response({'answer_correct': is_correct_answer})
