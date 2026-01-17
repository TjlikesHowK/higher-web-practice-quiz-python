"""Модуль с контроллерами для вопросов"""

from django.http.response import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, Request

from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService


class CreateAndListQuestion(APIView):
    question_service = QuestionService()

    def get(self, request: Request):
        questions = self.question_service.list_questions()
        serialized_questions = QuestionSerializer(questions, many=True)

        return Response(serialized_questions.data)

    def post(self, request: Request):
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        question = self.question_service.create_question(
            serializer.validated_data['quiz'].pk,
            serializer.validated_data
        )
        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_201_CREATED
        )


class DetailGetUpdateDeleteQuestion(APIView):
    question_service = QuestionService()

    def get(self, request: Request, id: int):
        question = self.question_service.get_question(id)
        return Response(QuestionSerializer(question).data)

    def put(self, request: Request, id: int):
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_quiz = self.question_service.update_question(
            id,
            serializer.validated_data
        )

        return Response(QuestionSerializer(updated_quiz).data)

    def delete(self, request: Request, id: int):
        self.question_service.delete_question(id)
        return Response()


class QuestionsByTextView(APIView):
    question_service = QuestionService()

    def get(self, request: Request, text: str):
        questions = self.question_service.get_questions_by_text(text)
        return Response(QuestionSerializer(questions, many=True).data)


class CheckAnswerView(APIView):
    question_service = QuestionService()

    def post(self, request: Request, id: int):
        answer = json.loads(request.body).get('user_answer', '')
        is_correct_answer = self.question_service.check_answer(id, answer)

        return Response({
            'answer_correct': is_correct_answer
        })
