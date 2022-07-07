from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet

from menu.models import FoodCategory, Food
from menu.serializers import FoodListSerializer


class FoodModelViewSet(ModelViewSet):
    """вьюха для отображения меню по категориям"""

    # используем prefetch_related чтобы исключить пункты меню is_published=False
    # похожее решение позаимствовал отсюда:
    # https://stackoverflow.com/questions/28163556/how-do-you-filter-a-nested-serializer-in-django-rest-framework
    menu = FoodCategory.objects.prefetch_related(
        Prefetch('food', queryset=Food.objects.filter(is_publish=True), to_attr='filtered_food')).order_by('order_id')

    # делаем список из id категорий, где все пункты меню is_published=False
    empty_categories = [category.id for category in menu if category.filtered_food == []]

    # удаляем пустые категории из меню
    queryset = menu.exclude(id__in=empty_categories)

    # если будут проблемы с миграцией, то надо закоментировать строчки 14-21 и разкоментировать 24 строку
    # queryset = FoodCategory.objects.all()

    serializer_class = FoodListSerializer

    def get_serializer_class(self):
        """метод контроля версий api"""
        if self.request.version == 'v1':
            return FoodListSerializer

