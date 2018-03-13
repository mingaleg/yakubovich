from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from ejudge_plug.models import Runs


class StaffRequiredView(View):
    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class EjContestView(StaffRequiredView):
    def get(self, request, runid):
        cid, rid = map(int, runid.split('-'))
        run = Runs.objects.get(
            contest_id=cid,
            run_id=rid
        )
        return HttpResponse(str(run.prob_id))