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




class TestHomeViews(TestCase):

	def setUp(self):
		self.client = Client()

		self.user = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')

		self.notcreateuser = User.objects.create_user(
			username='notcreateuser', email='s@gmail.com', password='secret123')

		self.adminuser = User.objects.create_user(
			username='adminuser', email='s@gmail.com', password='secret123', is_staff=True)

		obj_puser = mixer.blend('users.PUser', user=self.user)
		obj_puser_oth = mixer.blend('users.PUser', user=self.notcreateuser)
		obj_puser_staff = mixer.blend('users.PUser', user=self.adminuser)

		ranking1 = mixer.blend('analytics.Ranking', title="test1", low_score=0, high_score=9, add_days=5)
		ranking2 = mixer.blend('analytics.Ranking', title="test2", low_score=10, high_score=19, add_days=5)



	def test_home_view(self):

		path = reverse('Home')

		res = self.client.get(path)
		assert res.status_code == 200, 'All users can view'

		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'All viewers logged in can view'



	def test_contact_view(self):

		path = reverse('Contact')

		res = self.client.get(path)
		assert res.status_code == 200, 'All users can view'

		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'All viewers logged in can view'




	def test_termsandconditions_view(self):
		path = reverse('TermsAndCondition')
		res = self.client.get(path)
		assert res.status_code == 200, 'All users can view'
		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'All viewers logged in can view'


	def test_disclaimer_view(self):
		path = reverse('Disclaimer')
		res = self.client.get(path)
		assert res.status_code == 200, 'All users can view'
		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'All viewers logged in can view'


	def test_privacypolicy_view(self):
		path = reverse('PrivacyPolicy')
		res = self.client.get(path)
		assert res.status_code == 200, 'All users can view'
		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'All viewers logged in can view'


	def test_ourmission_view(self):
		path = reverse('AboutUs')
		res = self.client.get(path)
		assert res.status_code == 200, 'All users can view'
		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'All viewers logged in can view'


	def test_pressrelease_view(self):
		path = reverse('Press')
		res = self.client.get(path)
		assert res.status_code == 200, 'All users can view'
		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'All viewers logged in can view'


	def test_faq_view(self):
		path = reverse('FAQ')
		res = self.client.get(path)
		assert res.status_code == 200, 'All users can view'
		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'All viewers logged in can view'

