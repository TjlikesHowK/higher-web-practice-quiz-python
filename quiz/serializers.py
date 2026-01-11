"""Модуль c сериализаторами"""

from rest_framework import serializers

from quiz.models import Category, Question, Quiz


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов"""

    class Meta:
        model = Question
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для квизов"""

    class Meta:
        model = Quiz
        fields = '__all__'
