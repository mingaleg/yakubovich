import string

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from mapper.models import Problem

from django_object_actions import DjangoObjectActions


@admin.register(Problem)
class ProblemAdmin(DjangoObjectActions, admin.ModelAdmin):
    change_list_template = "mapper/admin/change_list.html"
    list_display = [
        'chars',
        'contest_id',
        'prob_id',
    ]
    list_display_links = [
        'chars',
    ]
    list_editable = list_display[1:]
    ordering = ['chars']

    CHARS = {
        'latin': string.ascii_uppercase,
        'cyrillic': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    }

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(r'generate/<typesetting>/', self.generate_typesetting)
        ] + urls

    def generate_typesetting(self, request, typesetting):
        for ch in self.CHARS[typesetting]:
            Problem.objects.create(
                chars=ch,
                contest_id=999999,
                prob_id=999999,
            )
        return HttpResponseRedirect("../../")
