import pytest
from mixer.backend.django import mixer
from django.contrib.admin.sites import AdminSite
pytestmark = pytest.mark.django_db
from django.contrib.auth.models import User
from .. import admin
from .. import models

class TestBillingAdmin:

	def test_transaction__str__(self):
		site = AdminSite()
		billing_admin = admin.TransactionAdmin(models.Transaction, site)

		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj = mixer.blend('billing.Transaction', user=uobj, transaction_id="12345")

		result = billing_admin.__str__(obj)
		assert result == obj.transaction_id, 'Should return the title'


	def test_pricing__str__(self):
		site = AdminSite()
		billing_admin = admin.PriceToDaysAdmin(models.PriceToDays, site)
		obj = mixer.blend('billing.PriceToDays')

		result = billing_admin.__str__(obj)
		assert result == str(obj.label), 'Should return the pollitem'

