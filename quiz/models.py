"""Модуль c моделями приложения quiz"""

from django.db import models

from .consts import (CATEGORY_MAX_LENGTH, DESCRIPTION_AND_TEXT_MAX_LENGTH,
                     DIFFICULTY_MAX_LNEGTH, EXPLANATION_MAX_LENGTH,
                     QUIZ_MAX_LENGTH)


class Category(models.Model):
    """Модель категории вопросов"""

    title = models.CharField(
        max_length=CATEGORY_MAX_LENGTH,
        verbose_name='Название категории'
    )


class Quiz(models.Model):
    """Модель квиза"""

    title = models.CharField(
        max_length=QUIZ_MAX_LENGTH,
        verbose_name='Название квиза'
    )
    description = models.CharField(
        max_length=DESCRIPTION_AND_TEXT_MAX_LENGTH,
        blank=True,
        verbose_name='Описание квиза'
    )


class Difficulty(models.TextChoices):
    """Варианты сложностей для вопросов"""

    EASY = 'easy', 'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'


class Question(models.Model):
    """Модель вопроса"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='questions'
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='Квиз',
        related_name='questions'
    )
    text = models.CharField(
        max_length=DESCRIPTION_AND_TEXT_MAX_LENGTH,
        verbose_name='Текст вопроса'
    )
    description = models.CharField(
        max_length=DESCRIPTION_AND_TEXT_MAX_LENGTH,
        blank=True,
        verbose_name='Описание вопроса'
    )
    options = models.JSONField(
        verbose_name='Варианты ответа'
    )
    correct_answer = models.IntegerField(
        verbose_name='Правильный ответ'
    )
    explanation = models.CharField(
        max_length=EXPLANATION_MAX_LENGTH,
        blank=True,
        verbose_name='Объяснение правильного ответа'
    )
    difficulty = models.CharField(
        max_length=DIFFICULTY_MAX_LNEGTH,
        choices=Difficulty.choices,
        verbose_name='Сложность вопроса'
    )
