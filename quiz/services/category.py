"""Модуль с реализацией сервиса категорий"""

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractCategoryService
from quiz.models import Category
from quiz.services.utils import update_object


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий"""

    def list_categories(self):
        return Category.objects.all()

    def get_category(self, category_id: int):
        return get_object_or_404(Category, id=category_id)

    def create_category(self, title: str):
        return Category.objects.create(title=title)

    def update_category(self, category_id: int, data: dict):
        return update_object(Category, category_id, data)

    def delete_category(self, category_id: int):
        category = self.get_category(category_id)
        category.delete()
