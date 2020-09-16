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




class TestPuserViews(TestCase):

	def setUp(self):
		self.client = Client()

		self.normaluser = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')

		self.otheruser = User.objects.create_user(
			username='otheruser', email='s@gmail.com', password='secret123')

		self.nopuser = User.objects.create_user(
			username='nopuser', email='s@gmail.com', password='secret123')

		self.adminuser = User.objects.create_user(
			username='adminuser', email='s@gmail.com', password='secret123', is_staff=True)

		obj_puser = mixer.blend('users.PUser', user=self.normaluser)
		obj_puser_otheruser = mixer.blend('users.PUser', user=self.otheruser)
		obj_puser_staff = mixer.blend('users.PUser', user=self.adminuser)

		ranking1 = mixer.blend('analytics.Ranking', title="test1", low_score=0, high_score=9, add_days=5)
		ranking2 = mixer.blend('analytics.Ranking', title="test2", low_score=10, high_score=19, add_days=5)


	def test_puser_detail_view(self):
		path = reverse('PUserDetail', kwargs={'pk':1})
		res = self.client.get(path)
		assert res.status_code == 200, 'Can be viewed by all users'





	def test_puser_create_view(self):
		path = reverse('PUserCreate')
		res = self.client.get(path)
		assert res.status_code == 302, 'Cannot be accessed by users who are not signed in'

		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 302, 'Cannot be accessed by users with a puser profile'

		#this is not working - can only be accessed by users withour puser profle
		self.client.login(username="nopuser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'Can only be accessed by users without puser profile'





	def test_puser_update_view(self):
		path = reverse('PUserUpdate', kwargs={'pk':1})


		res = self.client.get(path)
		assert res.status_code == 404, 'Cannot be viewed by none signed in user'

		self.client.login(username="otheruser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 404, 'Cannot be updated by user who does not own'

		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'Can be updated by user who created'



