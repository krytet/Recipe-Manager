import csv
import os

import django
import sys

sys.path.append('../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_manager.settings')
django.setup()

def load_all_data(func):
    from api.models import Ingredient

    func('ingredients.csv', Ingredient)
    print('--------------------\nИнгридиенты загружены\n--------------')


@load_all_data
def load_table_from_csv(fname, model):
    from api.models import Ingredient
    file = open(fname, 'r', encoding='utf-8')
    reader = list(csv.reader(file, delimiter=','))

    for i in reader:
        Ingredient.objects.create(
            name=i[0],
            measurement_unit=i[1]
        )
        print(i[0], '  -  ', i[1])


