"""Модуль с контроллерами для квизов"""

import random

from rest_framework import status
from rest_framework.views import APIView, Request, Response

from quiz.serializers import QuestionSerializer, QuizSerializer
from quiz.services.quiz import QuizService


class CreateAndListQuiz(APIView):
    quiz_service = QuizService()

    def get(self, request: Request):
        quizes = self.quiz_service.list_quizzes()
        serialized_quizes = QuizSerializer(quizes, many=True)

        return Response(serialized_quizes.data)

    def post(self, request: Request):
        serializer = QuizSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        question = self.quiz_service.create_quiz(serializer.validated_data)
        return Response(
            QuizSerializer(question).data,
            status=status.HTTP_201_CREATED
        )


class DetailGetUpdateDeleteQuiz(APIView):
    quiz_service = QuizService()

    def get(self, request: Request, id: int):
        quiz = self.quiz_service.get_quiz(id)
        return Response(QuizSerializer(quiz).data)

    def put(self, request: Request, id: int):
        serializer = QuizSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_quiz = self.quiz_service.update_quiz(
            id,
            serializer.validated_data
        )

        return Response(QuizSerializer(updated_quiz).data)

    def delete(self, request: Request, id: int):
        self.quiz_service.delete_quiz(id)
        return Response()


class QuizesByTitleView(APIView):
    quiz_service = QuizService()

    def get(self, request: Request, title: str):
        quiz = self.quiz_service.get_quizes_by_title(title)
        return Response(QuizSerializer(quiz, many=True).data)


class QuizRandomQuiestionView(APIView):
    quiz_service = QuizService()

    def get(self, request: Request, id: int):
        quiz = self.quiz_service.get_quiz(id)

        questions = quiz.questions.all()

        if not questions:
            return Response({
                'message': f'Quiz with id {quiz.pk} not have questions'
            })

        random_question = random.choice(questions)

        return Response(QuestionSerializer(random_question).data)
