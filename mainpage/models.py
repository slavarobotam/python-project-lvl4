from django.db import models  # noqa: F401
from django.contrib.auth.models import User


# class TaskStatus(models.Model):
#     NEW = 'new'
#     STARTED = 'started'
#     TESTING = 'testing'
#     FINISHED = 'finished'
#     STATUS_CHOICES = (
#         (NEW, 'New'),
#         (STARTED, 'Started'),
#         (TESTING, 'Testing')
#         (FINISHED, 'Finished')
#     )
#     name = models.CharField(max_length=15,
#                             choices=STATUS_CHOICES,
#                             default='new')

#     def __str__(self):
#         return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    NEW = 'new'
    STARTED = 'started'
    TESTING = 'testing'
    FINISHED = 'finished'
    STATUS_CHOICES = (
        (NEW, 'New'),
        (STARTED, 'Started'),
        (TESTING, 'Testing'),
        (FINISHED, 'Finished')
    )
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default=NEW)
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='tasks')
    assigned_to = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='assigned_to')
    tags = models.ManyToManyField(Tag,
                                  related_name='tags')
    objects = models.Manager()

    def get_absolute_url(self):
        return "/{}/".format(self.pk)

    def __str__(self):
        return self.name

