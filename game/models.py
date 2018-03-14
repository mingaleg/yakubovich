import json
import uuid as uuid
from random import choice

from channels import Group
from django.conf import settings
from django.db import models
from django.db.models import Q

from .exceptions import GameException


class GameConfig(models.Model):
    words_fld = models.TextField()
    GUESS_MODE_CHOICES = (
        (0, "First"),
        (1, "Random"),
        (2, "All"),
    )
    guess_mode = models.PositiveIntegerField(choices=GUESS_MODE_CHOICES)
    correct_bonus = models.IntegerField(default=100)
    wrong_penalty = models.IntegerField(default=30)
    correct_shout_bonus = models.IntegerField(default=5)
    wrong_shout_bonus = models.IntegerField(default=5)

    @property
    def words(self):
        return list(map((lambda x: x.strip().split(maxsplit=1)), filter(None, self.words_fld.split('\n'))))

    def __str__(self):
        return "{} [{} words, {} mode]".format(
            self.id,
            len(self.words),
            self.guess_mode,
        )


class Game(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    STATE_CHOICES = (
        (0, "Registration"),
        (1, "Active"),
        (2, "End"),
    )
    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=0)
    config = models.ForeignKey(GameConfig, on_delete=models.PROTECT)
    round = models.PositiveIntegerField(default=0)
    wall = models.CharField(max_length=64, blank=True, null=True)
    score = models.IntegerField(default=0)
    title = models.CharField(max_length=128, blank=True, null=True)
    prevent_guesses = models.BooleanField(default=False)
    teamleader = models.ForeignKey(
        "Player",
        related_name="leaded_games",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    @classmethod
    def get(cls, uuid):
        if len(uuid) == 36:
            return cls.objects.get(uuid=uuid)
        elif len(uuid) == 8:
            return cls.objects.get(uuid__startswith=uuid)
        else:
            raise ValueError("uuid should be 8 or 36 chars long")

    class Meta:
        permissions = (
            ('start', "Start game"),
        )

    def guess(self, player, word):
        if self.state != 1:
            raise GameException("Game {} is not active".format(self.uuid))
        if self.prevent_guesses:
            raise GameException("Game {} preventing guessing")
        Event.guess(self, word)
        if self.config.words[self.round][0].upper() == word.upper():
            Event.correct_guess(self)
            self.new_round()
        else:
            self.prevent_guesses = True
            self.save()
            Event.wrong_guess(self)
            self.change_score(-self.config.wrong_penalty)

    def reload(self):
        Event.reload(self)

    @property
    def desc(self):
        return self.config.words[self.round][1] if self.state == 1 else ""

    def change_score(self, delta):
        self.score += delta
        self.save()
        Event.score(self)

    def join(self, player):
        if self.state != 0:
            raise GameException("Registration is closed for game {}".format(self.uuid))
        player.game = self
        player.save()
        Event.join(self, player)

    def lead(self, player):
        if self.teamleader:
            raise GameException("Game {} already has a leader".format(self.uuid))
        self.teamleader = player
        self.save()
        Event.lead(self, player)

    def shout(self, chars, player):
        chars = chars.upper()
        if self.state != 1:
            raise GameException("Game {} is not active".format(self.uuid))
        Event.shout(self, player, chars)
        correct_positions = []
        hidden = self.config.words[self.round][0]
        for i, ch in enumerate(hidden):
            if self.wall[i] == '.' and ch in chars:
                correct_positions.append(i)
        if self.config.guess_mode == 0:
            correct_positions = correct_positions[:1]
        elif self.config.guess_mode == 1:
            correct_positions = correct_positions and [choice(correct_positions)]
        for i in correct_positions:
            self.wall = self.wall[:i] + hidden[i] + self.wall[i+1:]
        self.save()
        Event.shout_result(self, chars, len(correct_positions))
        if len(correct_positions):
            self.prevent_guesses = False
            self.save()
            Event.wall(self)
            self.change_score(self.config.correct_shout_bonus)
        else:
            self.change_score(self.config.wrong_shout_bonus)
        if self.wall == hidden:
            self.new_round()
        return len(correct_positions)

    def start(self):
        self.state = 1
        self.wall = '.' * len(self.config.words[self.round][0])
        self.save()
        Event.start(self)
        Event.wall(self)
        Event.desc(self)

    def new_round(self):
        self.round += 1
        self.prevent_guesses = False
        self.change_score(self.config.correct_bonus)
        if self.round >= len(self.config.words):
            self.save()
            self.end()
            return
        self.state = 1
        self.wall = '.' * len(self.config.words[self.round][0])
        self.save()
        Event.new_round(self)
        Event.wall(self)
        Event.desc(self)

    def end(self):
        self.state = 2
        self.save()
        Event.end(self)

    def events(self):
        return Event.objects.filter(
            Q(game=self) | Q(glob=True)
        ).order_by("timestamp")

    def __str__(self):
        return self.title or self.uuid.__str__()


class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, blank=True, null=True, on_delete=models.SET_NULL)
    ejudge_id = models.PositiveIntegerField(primary_key=True)

    def shout(self, chars):
        hit = self.game.shout(chars, self)
        return hit

    def __str__(self):
        return "{} ({})".format(
            self.user,
            self.user.get_full_name(),
        )

    def guess(self, guess):
        return self.game.guess(self, guess)


class Event(models.Model):
    game = models.ForeignKey(Game, blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    style = models.CharField(max_length=64)
    glob = models.BooleanField(default=False)

    def save(self, **kwargs):
        super().save(**kwargs)
        grname = 'global' if self.glob else self.game.uuid.__str__()
        Group(grname).send({
            'text': json.dumps({
                'text': self.text,
                'timestamp': self.timestamp.timestamp(),
                'style': self.style,
            })
        })

    @classmethod
    def join(cls, game, player):
        cls.objects.create(
            game=game,
            text="К игре присоединился {}".format(player.user.get_full_name()),
            style="join",
        )

    @classmethod
    def shout(cls, game, player, chars):
        cls.objects.create(
            game=game,
            text="{}: {}".format(player.user.get_full_name(), chars),
            style="shout",
        )

    @classmethod
    def shout_result(cls, game, char, hit):
        if hit:
            cls.objects.create(
                game=game,
                text="Откройте букву {}! +{} баллов".format(char, game.config.correct_shout_bonus),
                style="shout_result hit",
            )
        else:
            cls.objects.create(
                game=game,
                text="Такой буквы здесь нет! +{} баллов".format(game.config.wrong_shout_bonus),
                style="shout_result miss",
            )

    @classmethod
    def new_round(cls, game):
        cls.objects.create(
            game=game,
            text="Новый раунд",
            style="new_round",
        )

    @classmethod
    def score(cls, game):
        cls.objects.create(
            game=game,
            text="{}".format(game.score),
            style="score",
        )

    @classmethod
    def wall(cls, game):
        cls.objects.create(
            game=game,
            text="{}".format(game.wall),
            style="wall",
        )

    @classmethod
    def desc(cls, game):
        cls.objects.create(
            game=game,
            text="{}".format(game.desc),
            style="desc",
        )

    @classmethod
    def start(cls, game):
        cls.objects.create(
            game=game,
            text="Игра началась!",
            style="start",
        )

    @classmethod
    def end(cls, game):
        cls.objects.create(
            game=game,
            text="Игра завершена! Баллов: {}".format(game.score),
            style="end",
        )

    @classmethod
    def lead(cls, game, player):
        cls.objects.create(
            game=game,
            text="Капитан: {}".format(game.teamleader.user.get_full_name()),
            style="lead",
        )

    @classmethod
    def guess(cls, game, word):
        cls.objects.create(
            game=game,
            text="{}?".format(word),
            style="guess",
        )

    @classmethod
    def correct_guess(cls, game):
        cls.objects.create(
            game=game,
            text="Ну разумеется! +{} баллов!".format(game.config.correct_bonus),
            style="guess correct",
        )

    @classmethod
    def wrong_guess(cls, game):
        cls.objects.create(
            game=game,
            text="Ну что вы такое говорите... -{} баллов!".format(game.config.wrong_penalty),
            style="guess wrong",
        )

    @classmethod
    def reload(cls, game):
        cls.objects.create(
            game=game,
            text="## перезагрузка страницы ##",
            style="reload",
        )