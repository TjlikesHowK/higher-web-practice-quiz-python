"""Модуль c роутингом"""

from django.urls import path

from quiz.views.category import (CreateAndListCategory,
                                 DetailGetUpdateDeleteCategory)
from quiz.views.question import (CheckAnswerView, CreateAndListQuestion,
                                 DetailGetUpdateDeleteQuestion,
                                 QuestionsByTextView)
from quiz.views.quiz import (CreateAndListQuiz, DetailGetUpdateDeleteQuiz,
                             QuizesByTitleView, QuizRandomQuiestionView)

urlpatterns = [
    path(
        'category/',
        CreateAndListCategory.as_view(),
        name='create-and-list-category'
    ),
    path(
        'category/<int:id>/',
        DetailGetUpdateDeleteCategory.as_view(),
        name='detail-get-update-delete-category'
    ),
    path(
        'quiz/',
        CreateAndListQuiz.as_view(),
        name='create-and-list-quiz'
    ),
    path(
        'quiz/<int:id>/',
        DetailGetUpdateDeleteQuiz.as_view(),
        name='detail-get-update-delete-quiz'
    ),
    path(
        'quiz/by_title/<str:title>/',
        QuizesByTitleView.as_view(),
        name='get-by-title-quiz'
    ),
    path(
        'quiz/<int:id>/random_question/',
        QuizRandomQuiestionView.as_view(),
        name='quiz-random-question'
    ),
    path(
        'question/',
        CreateAndListQuestion.as_view(),
        name='create-and-list-question'
    ),
    path(
        'question/<int:id>/',
        DetailGetUpdateDeleteQuestion.as_view(),
        name='detail-get-update-delete-question'
    ),
    path(
        'question/by_text/<str:text>/',
        QuestionsByTextView.as_view(),
        name='get-by-text-question'
    ),
    path(
        'question/<int:id>/check/',
        CheckAnswerView.as_view(),
        name='check-answer'
    ),
]
