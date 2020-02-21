from django.contrib.auth.models import User
from django.db import models  # noqa: F401
from django.urls import reverse


class Status(models.Model):
    status_value = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return self.status_value


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='To do:')
    status = models.ForeignKey(Status,
                               default=1,
                               on_delete=models.CASCADE,
                               related_name='statuses')
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='creator')
    assigned_to = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='assigned_to')
    tags = models.ManyToManyField(Tag,
                                  default=1,
                                  related_name='tags')
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('mainpage:view_task', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    def description_lines(self):
        return filter(
            None,
            (line.strip() for line in self.description.splitlines()))

    def random_taskname():
        while 1:
            import random
            ROUTINE_TASKS = [
                'Go for a walk', 'Clean up a room', 'Read 30 min',
                'Solve kata', 'Workout', 'Pat cat', 'Meditate',
                'Stretching', 'Job searching'
            ]
            return random.choice(ROUTINE_TASKS)
