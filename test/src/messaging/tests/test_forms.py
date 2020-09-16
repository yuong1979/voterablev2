import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from .. import forms
# from django.core.urlresolvers import reverse


class TestMsgForm:
	def test_pollitemmessageaddform(self):

		form = forms.PollItemMessageAddForm(data={})
		assert form.is_valid() is False, 'Should be invalid if not data provided'

		form = forms.PollItemMessageAddForm(data={'content':'123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong '})
		assert form.is_valid() is False, 'Should be invalid if too long'
		assert 'content' in form.errors, 'should have content field error'


	def test_pollitemmessageupdateform(self):

		form = forms.PollItemMessageUpdateForm(data={})
		assert form.is_valid() is False, 'Should be invalid if not data provided'

		form = forms.PollItemMessageUpdateForm(data={'content':'123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong 123456789toolong '})
		assert form.is_valid() is False, 'Should be invalid if too long'
		assert 'content' in form.errors, 'should have content field error'




