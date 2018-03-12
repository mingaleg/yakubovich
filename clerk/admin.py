from django.contrib import admin
from .models import Contest, Submission


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    actions = [
        'pull_new_submissions',
    ]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'run_id',
        'contest',
        'prob_id',
        'user_id',
        'status',
        'score',
        'create_time',
        'need_update',
    ]

    actions=[
        "update",
    ]

    def update(self, request, queryset):
        queryset.update(need_update=True)
