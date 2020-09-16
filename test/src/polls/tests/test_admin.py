import pytest
from mixer.backend.django import mixer
from django.contrib.admin.sites import AdminSite
pytestmark = pytest.mark.django_db

from .. import admin
from .. import models

class TestPollAdmin:
	def test_ptype__str__(self):
		site = AdminSite()
		polls_admin = admin.PtypeAdmin(models.Ptype, site)
		obj = mixer.blend('polls.Ptype', title='Hello World')
		result = polls_admin.__str__(obj)
		assert result == 'Hello World', 'Should return the first few characters'


	def test_pitem__str__(self):
		site = AdminSite()
		polls_admin = admin.PollAdmin(models.PollItem, site)
		obj = mixer.blend('polls.PollItem', title='Hello World')
		result = polls_admin.__str__(obj)
		assert result == 'Hello World', 'Should return the first few characters'


