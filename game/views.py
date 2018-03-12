from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .models import Game, Event
from .forms import GuessForm


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class GameView(LoginRequiredView):
    template_name = "game/game.html"

    def get(self, request, uuid):
        game = Game.get(uuid)
        if not request.user.player.game:
            return redirect("join", uuid=uuid)
        is_teamleader = game.teamleader == request.user.player
        return render(request, self.template_name, {
            'game': game,
            'is_teamleader': is_teamleader,
        })


class ShoutView(LoginRequiredView):
    def get(self, request, uuid, chars):
        game = Game.get(uuid)
        player = request.user.player
        if player.game != game:
            raise PermissionDenied
        player.shout(chars)
        return redirect("game", uuid=uuid)


class JoinView(LoginRequiredView):
    def get(self, request, uuid):
        game = Game.get(uuid)
        player = request.user.player
        game.join(player)
        return redirect("game", uuid=uuid)


class LeadView(LoginRequiredView):
    def get(self, request, uuid):
        game = Game.get(uuid)
        player = request.user.player
        game.lead(player)
        return redirect("game", uuid=uuid)


class StartView(LoginRequiredView):
    def get(self, request, uuid):
        if not request.user.has_perm("game.start"):
            raise PermissionDenied
        game = Game.get(uuid)
        game.start()
        return redirect("game", uuid=uuid)


class GuessView(LoginRequiredView):
    def get(self, request, uuid):
        game = Game.get(uuid)
        player = request.user.player
        if game.teamleader != player:
            raise PermissionDenied
        form = GuessForm()
        return render(request, 'game/guess.html', {
            'game': game,
            'form': form,
        })

    def post(self, request, uuid):
        game = Game.get(uuid)
        player = request.user.player
        form = GuessForm(request.POST)
        if form.is_valid():
            guess = form.cleaned_data['guess']
            player.guess(guess)
            return HttpResponseRedirect('../')
        return render(request, 'game/guess.html', {
            'game': game,
            'form': form,
        })