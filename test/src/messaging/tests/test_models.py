import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User



class TestMessage:


	def test_model_message_create(self):
		obj = mixer.blend('messaging.Message')
		assert obj.pk == 1, 'Should create a message instance'

	def test_model_message_get_absolute_url(self):

		ptype_obj = mixer.blend('polls.Ptype')
		pitem_obj = mixer.blend('polls.PollItem',polltype=ptype_obj)		
		msg_obj = mixer.blend('messaging.Message',pollitem=pitem_obj)

		result = msg_obj.get_absolute_url()

		assert result == reverse("polls_detail", kwargs={"pk":1}), 'absolute url link to pollsdetail'


	def test_model_message_count_likes(self):

		self.normaluser = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj_puser = mixer.blend('users.PUser', user=self.normaluser)
		ptype_obj = mixer.blend('polls.Ptype')
		pitem_obj = mixer.blend('polls.PollItem',polltype=ptype_obj)		
		msg_obj = mixer.blend('messaging.Message',pollitem=pitem_obj)
		msg_obj.userlikes.add(self.normaluser)

		result = msg_obj.calc_likes()

		assert result == 1, 'counting message/review likes'





