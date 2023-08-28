
from os.path import join
from sxl import Workbook

from django.conf import settings
from django.core.management.base import BaseCommand

from categories.models import Category


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):

        wb = Workbook(join(settings.BASE_DIR, 'tmp', options['filename']))

        ws = wb.sheets['Export Groups Sheet']

        Category.objects.all().delete()

        categories = {}

        for row in ws.rows[2:]:
            code = str(int(row[0]))
            name_uk = row[2]
            name_ru = row[1]

            categories[code] = Category.objects.create(
                name=name_uk,
                name_uk=name_uk,
                name_ru=name_ru,
                title=name_uk,
                title_uk=name_uk,
                title_ru=name_ru,
                code=code
            )

        for row in ws.rows[2:]:
            code = str(int(row[0]))
            parent_code = row[4]

            if parent_code is None:
                continue

            parent_code = str(int(parent_code))

            category = categories[code]

            category.parent_id = categories[parent_code].pk
            category.save(update_fields=['parent_id'])

        Category.objects.rebuild()

        self.stdout.write(self.style.SUCCESS('Success'))
