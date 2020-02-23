from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Status(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
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

    def random_taskname():
        while 1:
            import random
            ROUTINE_TASKS = [
                'Go for a walk', 'Clean up something', 'Read 30 min',
                'Solve kata', 'Do small workout', 'Pat cat',
                'Straight your back', 'Make a stretch', 'Make coffee'
            ]
            return random.choice(ROUTINE_TASKS)
