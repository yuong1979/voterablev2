import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.core.urlresolvers import reverse
# from django.test import Client
# from django.test import TestCase

class TestPUser:


	def test_model_puser_create(self):
		
		obj = mixer.blend('users.PUser')
		assert obj.pk == 1, 'Should create a user instance'


	def test_model_puser_get_update(self):
		obj = mixer.blend('users.PUser')
		result = obj.get_update()

		assert result == reverse('PUserUpdate', kwargs={'pk':1}), 'Should be absolute url to edit'


	def test_model_puser_get_absolute_url(self):
		obj = mixer.blend('users.PUser')
		result = obj.get_absolute_url()

		assert result == reverse('PUserDetail', kwargs={'pk':1}), 'Should be absolute url to the user'

