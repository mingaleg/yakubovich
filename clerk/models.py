from django.db import models

from .signals import new_judged_submission

from ejudge_plug.models import Runs


class Contest(models.Model):
    contest_id = models.PositiveIntegerField(primary_key=True)
    wait_next_run = models.PositiveIntegerField(default=0)

    def pull_new_submissions(self):
        for obj in Runs.objects.filter(
            contest_id=self.contest_id,
            run_id__gte=self.wait_next_run,
        ):
            Submission.update(self, obj)
            self.wait_next_run = max(self.wait_next_run, obj.run_id+1)
            self.save()

        for obj in Submission.objects.filter(
            need_update=True
        ):
            obj.pull()

    def __str__(self):
        return "Contest {} [{} runs]".format(self.contest_id, self.wait_next_run)


class Submission(models.Model):
    run_id = models.PositiveIntegerField()
    contest = models.ForeignKey(Contest, on_delete=models.PROTECT)
    create_time = models.DateTimeField()

    user_id = models.PositiveIntegerField()
    prob_id = models.PositiveIntegerField()
    lang_id = models.PositiveIntegerField()

    need_update = models.BooleanField()

    STATUS_CHOICES = (
        ( 0, "OK"),
        ( 1, "Compilation Error"),
        ( 2, "Run-Time Error"),
        ( 3, "Time-Limit Exceeded"),
        ( 4, "Presentation Error"),
        ( 5, "Wrong Answer"),
        ( 6, "Check Failed"),
        ( 7, "Partial Solution"),
        ( 8, "Accepted for Testing"),
        ( 9, "Ignored"),
        (10, "Disqualified"),
        (11, "Pending"),
        (12, "Memory Limit Exceeded"),
        (13, "Security Violation"),
        (14, "Style Violation"),
        (15, "Wall Time Limit Exceeded"),
        (16, "Pending Review"),
        (17, "Rejected"),
        (18, "Skipped"),
        (19, "Synchronization Error"),
        (23, "Summoned for Defence"),
        (95, "Full Rejudge"),
        (96, "Running"),
        (97, "Compiled"),
        (98, "Compiling"),
        (99, "Rejudge"),
        (22, "Empty Record"),
        (20, "Virtual Start"),
        (21, "VIrtual Stop"),
    )

    STATUSES_IGNORE_SUBMISSION = (20, 21, 22)
    STATUSES_NOT_JUDGED = (11, 95, 96, 97, 98, 99)

    status = models.IntegerField(choices=STATUS_CHOICES)
    score = models.IntegerField()

    class Meta:
        unique_together = ('run_id', 'contest')

    def is_judged(self):
        return not self.need_update and self.status not in self.STATUSES_NOT_JUDGED

    def save(self, **kwargs):
        if self.status in self.STATUSES_IGNORE_SUBMISSION:
            return
        if not kwargs.pop("force_need_update", False):
            self.need_update = self.status in self.STATUSES_NOT_JUDGED
        super().save(**kwargs)

    def __str__(self):
        return "Run {}#{} [{}]".format(
            self.contest_id,
            self.run_id,
            self.status,
        )

    def pull(self):
        obj = self.get_run()
        was_judged = self.is_judged()
        self.create_time=obj.create_time
        self.user_id=obj.user_id
        self.prob_id=obj.prob_id
        self.lang_id=obj.lang_id
        self.status=obj.status
        self.score=obj.score
        self.save()
        if not was_judged and self.is_judged():
            new_judged_submission.send_robust(
                sender=Submission,
                contest_pk=self.contest.contest_id,
                run_id=self.run_id,
            )

    @classmethod
    def update(cls, contest, obj):
        obj, created = Submission.objects.update_or_create(
            run_id=obj.run_id,
            contest=contest,
            create_time=obj.create_time,
            user_id=obj.user_id,
            prob_id=obj.prob_id,
            lang_id=obj.lang_id,
            status=obj.status,
            score=obj.score,
        )
        if created and obj.is_judged():
            new_judged_submission.send_robust(
                sender=Submission,
                contest_pk=obj.contest.pk,
                run_id=obj.run_id,
            )

    def force_update(self):
        self.need_update = True
        self.save(force_need_update=True)

    def get_run(self):
        return Runs.objects.get(
            contest_id=self.contest.contest_id,
            run_id=self.run_id,
        )
