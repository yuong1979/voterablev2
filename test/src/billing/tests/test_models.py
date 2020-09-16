import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.contrib.auth.models import User





class TestTransaction:
	def test_model_transaction_create(self):
		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj = mixer.blend('billing.Transaction', user=uobj)

		assert obj.pk == 1, 'Should create a transaction instance'



class TestPriceToDays:
	def test_model_pricetodays_create(self):
		obj = mixer.blend('billing.PriceToDays')

		assert obj.pk == 1, 'Should create a pricing type instance'

