import json

from django.core.management import BaseCommand

from menu.models import FoodCategory, Food


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.json_path = 'restaurant/menu/fixtures/'

    def fill_table(self, model, json_file, category=None):
        """метод для добавления позиций меню из категории"""

        # считываем данные из json
        with open(self.json_path + json_file, mode='r', encoding='utf-8') as infile:
            items = json.load(infile)

            # записываем в бд
        for item in items:
            new_item = model(**item)
            # если указана категория, то прописываем ее
            if category is not None:
                new_item.category = category
            new_item.save()
            print(f'{new_item.name_ru} теперь в бд')

    def handle(self, *args, **options):
        # обнуляем таблицу с категориями
        FoodCategory.objects.all().delete()
        # записываем категории
        self.fill_table(FoodCategory, 'categories.json')
        # обнуляем таблицу с едой
        Food.objects.all().delete()
        # записываем еду
        self.fill_table(Food, 'snacks.json', FoodCategory.objects.get(pk=1))
        self.fill_table(Food, 'soup.json', FoodCategory.objects.get(pk=2))
        self.fill_table(Food, 'main_dishes.json', FoodCategory.objects.get(pk=3))
        self.fill_table(Food, 'desserts.json', FoodCategory.objects.get(pk=4))
        self.fill_table(Food, 'drinks.json', FoodCategory.objects.get(pk=5))
