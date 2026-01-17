from django.contrib import admin

from quiz.models import Category, Question, Quiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'category', 'quiz', 'difficulty',
        'text', 'correct_answer'
    )
    search_fields = (
        'text', 'category__title',
        'quiz__title', 'description'
    )
    list_filter = (
        'category',
        'difficulty'
    )
