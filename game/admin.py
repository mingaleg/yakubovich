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

    def players(self, obj):
        return obj.player_set.count()



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