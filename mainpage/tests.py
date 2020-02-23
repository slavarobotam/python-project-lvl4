from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from mainpage import views
from mainpage.models import Status, Tag, Task


class TaskTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.c = Client()

    def create_task(self, name="test name"):
        some_status = Status.objects.create(name='New')
        some_tag = Tag.objects.create(name='Test')
        some_task = Task.objects.create(name=name,
                                        assigned_to=self.user,
                                        creator=self.user,
                                        status=some_status)
        some_task.tags.set([some_tag])
        return some_task

    def test_create_task(self):
        some_task = self.create_task()
        self.assertTrue(isinstance(some_task, Task))
        self.assertEqual(some_task.__str__(), some_task.name)
        self.assertEqual(Task.objects.count(), 1)

    def test_task_list(self):
        request = self.factory.get('/')
        request.user = self.user
        response = views.home(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_access(self):
        response = self.c.get(reverse('mainpage:home'))
        self.user = AnonymousUser()
        self.assertEqual(response.status_code, 302)

    def test_invalid_task(self):
        data = {'description': 'test description'}
        response = self.c.post(reverse('mainpage:new_task'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "name",
                             "This field is required.")

    def test_create_status(self):
        self.c.login(username='testuser', password='12345')
        response = self.c.get(reverse('mainpage:settings'))
        self.assertEqual(response.status_code, 200)
        data = {"name": "newstatus"}
        data['user'] = self.user.id
        response = self.c.post(reverse('mainpage:create_status'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 1)
