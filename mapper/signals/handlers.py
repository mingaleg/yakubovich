import django.dispatch
from clerk.signals import new_judged_submission
from clerk.models import Submission
from game.models import Player
from ..models import Problem, History


@django.dispatch.receiver(new_judged_submission, sender=Submission)
def shout(sender, **kwargs):
    contest_pk = kwargs['contest_pk']
    run_id = kwargs['run_id']

    subm = Submission.objects.get(
        contest=contest_pk,
        run_id=run_id,
    )
    if subm.status != 0:
        return False

    try:
        prob = Problem.objects.get(
            contest_id=subm.contest_id,
            prob_id=subm.prob_id,
        )
    except Problem.DoesNotExist:
        return

    if not History.new(
            contest_id=subm.contest_id,
            prob_id=subm.prob_id,
            ejudge_id=subm.user_id,
    ):
        return

    try:
        player = Player.objects.get(
            ejudge_id=subm.user_id,
        )
    except Player.DoesNotExist:
        return

    player.shout(prob.chars)
