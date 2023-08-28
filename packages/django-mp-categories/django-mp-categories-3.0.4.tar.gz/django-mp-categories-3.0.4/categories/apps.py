
from django.apps import AppConfig, apps
from django.utils.translation import gettext_lazy as _


class CategoriesAppConfig(AppConfig):

    name = 'categories'
    verbose_name = _('Categories')

    def ready(self):
        if not apps.is_installed('mptt'):
            raise Exception("`mp-categories` app depends on `django-mptt`")

        try:
            from slugify import slugify_url
        except ImportError:
            raise Exception("`mp-categories` app depends on `awesome-slugify`")
