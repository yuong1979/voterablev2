import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class TestViewPollTypeUnique:
	def test_model_ptypeview_create(self):
		pobj = mixer.blend('polls.Ptype')

		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj = mixer.blend('analytics.ViewPollTypeUnique', p_type=pobj)
		obj.userview.add(uobj)

		assert obj.pk == 1, 'Should create a view instance'

		result = obj.get_user_count()
		assert result == 1, 'number of users viewed should be 1'

		result = obj.get_url()
		assert result == "/polls/?type=" + str(obj.p_type.slug), 'Should be absolute url to the ptype'


class TestViewPollItemUnique:
	def test_model_pitemview_create(self):
		pobj = mixer.blend('polls.PollItem')

		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj = mixer.blend('analytics.ViewPollItemsUnique', p_item=pobj)
		obj.userview.add(uobj)

		assert obj.pk == 1, 'Should create a view instance'

		result = obj.get_user_count()
		assert result == 1, 'number of users viewed should be 1'


class TestRanking:
	def test_model_ranking_create(self):
		obj = mixer.blend('analytics.Ranking', title="hello World!")
		assert obj.pk == 1, 'Should create a new rank instance'



class TestPostReport:
	def test_model_post_report_create(self):
		pobj = mixer.blend('polls.PollItem')
		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')		
		obj = mixer.blend('analytics.PostReport', Puser=uobj, p_item=pobj)

		assert obj.pk == 1, 'Should create a new report instance'


class TestPromoAnalytic:
	def test_model_promoanalytic_create(self):
		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj = mixer.blend('analytics.PromoAnalytic', promouser=uobj)
		assert obj.pk == 1, 'Should create a view instance'


class TestMarketingPromo:
	def test_model_marketingpromo_create(self):
		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj = mixer.blend('analytics.MarketingPromo', referrer=uobj)
		assert obj.pk == 1, 'Should create a view instance'


class TestControlTable:
	def test_model_controltable_create(self):
		obj = mixer.blend('analytics.ControlTable')
		assert obj.pk == 1, 'Should create a view instance'




