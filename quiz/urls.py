"""Модуль c роутингом."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from quiz.views.category import CategoryViewSet
from quiz.views.question import QuestionViewSet
from quiz.views.quiz import QuizViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('question', QuestionViewSet, basename='question')
router.register('quiz', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
]
