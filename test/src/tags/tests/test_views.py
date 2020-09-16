import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from .. import views
pytestmark = pytest.mark.django_db
from polls.views import PollDetailView
from django.test import Client
from django.test import TestCase
from polls.models import PollItem, Ptype
from users.models import PUser
from polls.views import PollsListView
from tags.models import TagPoll



class TestTagViews(TestCase):

	def setUp(self):
		self.client = Client()

		self.user = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')

		self.notcreateuser = User.objects.create_user(
			username='notcreateuser', email='s@gmail.com', password='secret123')

		self.nopuser = User.objects.create_user(
			username='nopuser', email='s@gmail.com', password='secret123')

		self.adminuser = User.objects.create_user(
			username='adminuser', email='s@gmail.com', password='secret123', is_staff=True)

		obj_puser = mixer.blend('users.PUser', user=self.user)
		obj_puser_oth = mixer.blend('users.PUser', user=self.notcreateuser)
		obj_puser_staff = mixer.blend('users.PUser', user=self.adminuser)


		obj_ptype = mixer.blend('polls.Ptype', active=True)
		obj_tag = mixer.blend('tags.TagPoll', tagfav=self.user)
		obj_tag.polltype.add(obj_ptype)





	def test_tagall_view(self):
		path = reverse('TagAllView')

		self.client.login(username="nopuser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 302, 'Can be viewed by users logged in'

		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'Can be viewed by users logged in'



	def test_tag_view(self):
		path = reverse('TagView', kwargs={'pk':1})

		self.client.login(username="nopuser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 302, 'Can be viewed by users logged in'

		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'Can be viewed by users logged in'



