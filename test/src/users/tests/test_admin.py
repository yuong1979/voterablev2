import pytest
from mixer.backend.django import mixer
from django.contrib.admin.sites import AdminSite
pytestmark = pytest.mark.django_db

from .. import admin
from .. import models

class TestUserAdmin:
	def test_user__str__(self):
		site = AdminSite()
		puser_admin = admin.PUserAdmin(models.PUser, site)
		obj = mixer.blend('users.PUser')
		result = puser_admin.__str__(obj)
		assert result == (str(obj.user)), 'Should return name of user'


