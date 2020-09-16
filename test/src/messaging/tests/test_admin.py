import pytest
from mixer.backend.django import mixer
from django.contrib.admin.sites import AdminSite
pytestmark = pytest.mark.django_db

from .. import admin
from .. import models

class TestMessageAdmin:
	def test_message__str__(self):
		site = AdminSite()
		polls_admin = admin.MessageAdmin(models.Message, site)
		obj = mixer.blend('messaging.Message', content='Hello World')
		result = polls_admin.__str__(obj)
		assert result == 'Hello World', 'Should return the first few characters'
