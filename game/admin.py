from django.contrib import admin

from game.models import Game, GameConfig, Player, Event


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'title',
        'state',
        'score',
        'players',
        'teamleader',
    ]

    actions = [
        'start',
        'reload',
        'stop',
    ]

    def players(self, obj):
        return obj.player_set.count()

    def start(self, request, queryset):
        for x in queryset:
            x.start()

    def reload(self, request, queryset):
        for x in queryset:
            x.reload()

    def stop(self, request, queryset):
        for x in queryset:
            x.end()


@admin.register(GameConfig)
class GameConfigAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'wordscnt',
        'guess_mode'
    ]

    def wordscnt(self, obj):
        return len(obj.words)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'game',
        'ejudge_id',
    ]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'style',
        'text',
        'game',
    ]