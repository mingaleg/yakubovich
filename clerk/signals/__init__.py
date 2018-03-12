import django.dispatch

new_judged_submission = django.dispatch.Signal(['contest_pk', 'run_id'])
