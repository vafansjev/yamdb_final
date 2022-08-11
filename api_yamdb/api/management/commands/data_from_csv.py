from django.apps import apps
from django.core.management import BaseCommand
import csv

# Структура данных - приложение, модель, файл для импорта
DATA = [
    ("users", "USER", "./static/data/users.csv"),
    ("", "", "./static/data/category.csv"),
    ("", "", "./static/data/comments.csv"),
    ("", "", "./static/data/genre_title.csv"),
    ("", "", "./static/data/genre.csv"),
    ("", "", "./static/data/review.csv"),
    ("", "", "./static/data/titles.csv"),
]


class Command(BaseCommand):
    help = "Модуль загрузки тестовых данных из CSV"

    def handle(self, *args, **options):
        for current in DATA:
            try:
                file = current[2]
                print(f"\n\nИдет загрузка данных из файла {file}")
                _model = apps.get_model(current[0], current[1])
                csv_file = open(file, "r")
                reader = csv.reader(csv_file, delimiter=",")
                header = next(reader)
                before = _model.objects.count()
                rec_count = 0
                for row in reader:
                    _object_dict = {
                        key: value for key, value in zip(header, row)
                    }
                    _model.objects.get_or_create(**_object_dict)
                    rec_count += 1
                print(
                    f"Файл: {file}\nОбработано: {rec_count} записей\n"
                    + f"Добавлено: {_model.objects.count()-before}\n"
                    + "-------------------------------------------"
                )
            except Exception as e:
                print(f"{file}: Ошибка {e}")
