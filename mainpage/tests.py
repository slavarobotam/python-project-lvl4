from django.test import RequestFactory, TestCase, Client
from mainpage.models import Task, Status, Tag
from django.contrib.auth.models import User
from mainpage.forms import TaskForm


# models test
class TaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')

    def create_task(self, name="test title"):
        some_status = Status.objects.create(status_value='New')
        some_tag = Tag.objects.create(name='Test')
        some_task = Task.objects.create(name=name,
                                        assigned_to=self.user,
                                        creator=self.user,
                                        status=some_status)
        some_task.tags.set([some_tag])
        return some_task

    def test_task_creation(self):
        some_task = self.create_task()
        self.assertTrue(isinstance(some_task, Task))
        self.assertEqual(some_task.__str__(), some_task.name)
