import django.dispatch
from . import new_judged_submission
from ..models import Submission


@django.dispatch.receiver(new_judged_submission, sender=Submission)
def print_ok(sender, **kwargs):
    contest_pk = kwargs['contest_pk']
    run_id = kwargs['run_id']
    subm = Submission.objects.get(
        contest=contest_pk,
        run_id=run_id,
    )
    print(subm)

