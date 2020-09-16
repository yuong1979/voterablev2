import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from .. import forms
# from django.core.urlresolvers import reverse


class TestUserForm:
	def test_pusereditform(self):


		form = forms.PUserEditForm(data={'description':'123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong '})
		assert form.is_valid() is False, 'Should be invalid if too long'
		assert 'description' in form.errors, 'should have description field error'




