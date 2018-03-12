from django.db import models
from clerk.models import Contest


class Problem(models.Model):
    contest_id = models.PositiveIntegerField()
    prob_id = models.PositiveIntegerField()
    chars = models.CharField(max_length=32)

    def save(self, **kwargs):
        Contest.objects.get_or_create(
            contest_id=self.contest_id,
        )
        super().save(**kwargs)

    def __str__(self):
        return "{}#{}: <{}>".format(
            self.contest_id,
            self.prob_id,
            self.chars,
        )