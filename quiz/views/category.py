"""Модуль с контроллерами для категорий"""

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status

from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService


class CreateAndListCategory(APIView):
    category_service = CategoryService()

    def get(self, request: Request):
        categories = self.category_service.list_categories()
        serialized_categories = CategorySerializer(categories, many=True)

        return Response(serialized_categories.data)

    def post(self, request: Request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        category = self.category_service.create_category(
            serializer.validated_data['title']
        )
        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )


class DetailGetUpdateDeleteCategory(APIView):
    category_service = CategoryService()

    def get(self, request: Request, id: int):
        category = self.category_service.get_category(id)
        return Response(CategorySerializer(category).data)

    def put(self, request: Request, id: int):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_category = self.category_service.update_category(
            id,
            serializer.validated_data
        )

        return Response(CategorySerializer(updated_category).data)

    def delete(self, request: Request, id: int):
        self.category_service.delete_category(id)
        return Response()
