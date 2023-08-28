
from django.apps import apps
from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.utils import get_translation_fields
from cap.decorators import short_description, template_list_item

from categories.models import Category


class CategoryListFilter(admin.SimpleListFilter):
    title = _('Category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        for category in Category.objects.root_nodes():
            yield category.pk, "*" + category.name
            for child in category.get_children():
                yield child.pk, mark_safe("—") + child.name

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(category_id=self.value())


def get_formfield_overrides():

    if apps.is_installed('ckeditor'):
        from ckeditor.widgets import CKEditorWidget
        return {
            models.TextField: {'widget': CKEditorWidget}
        }

    return {}


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, MPTTModelAdmin):

    list_display = (
        ['id'] +
        get_translation_fields('name') +
        ['order', 'code', 'icon', 'product_count', 'get_preview']
    )

    list_editable = get_translation_fields('name') + ['order']

    fields = (
        ('parent', 'code', ),
        tuple(get_translation_fields('name')),
        tuple(get_translation_fields('title')),
        ('logo', 'icon', ),
        tuple(get_translation_fields('description')),
    )

    search_fields = get_translation_fields('name') + ['code']

    formfield_overrides = get_formfield_overrides()

    @template_list_item('admin/list_item_preview.html', _('Preview'))
    def get_preview(self, item):
        return {'file': item.logo}

    @short_description(_('Product count'))
    def product_count(self, item):
        return item.products.count()
