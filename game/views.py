from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from mapper.models import Problem, History
from .models import Game, Event, Player
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

class StaffRequiredView(View):
    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StandingsView(StaffRequiredView):
    def get(self, request):
        probs = Problem.objects.order_by('chars')
        rows = []
        for game in Game.objects.order_by('-score'):
            eids = Player.objects.filter(game=game).values_list('ejudge_id', flat=True)
            rows.append({
                'name': game.title,
                'score': game.score,
                'wall': game.wall,
                'round': game.round,
                'players': Player.objects.filter(game=game).count(),
                'probs': [],
            })
            for p in probs:
                cnt = History.objects.filter(
                        prob_id=p.prob_id,
                        contest_id=p.contest_id,
                        ejudge_id__in=eids,
                    ).count()
                rows[-1]['probs'].append({
                    'cnt': cnt or ''
                })
        players = []
        for player in Player.objects.filter(user__is_staff=False):
            if not player.game:
                continue
            oks_hst = History.objects.filter(
                ejudge_id=player.ejudge_id,
            )
            oks = []
            for ok in oks_hst:
                oks.append(Problem.objects.get(
                    contest_id=ok.contest_id,
                    prob_id=ok.prob_id,
                ))
            players.append({
                'name': player.user.get_full_name(),
                'game': player.game.title,
                'oks': len(oks),
                'probs': []
            })
            for prob in probs:
                players[-1]['probs'].append({
                    'cnt': '+' if prob in oks else ' '
                })

        return render(request, 'game/standings.html', {
            'problems': probs.values_list('chars', flat=True),
            'rows': rows,
            'players': players,
        })