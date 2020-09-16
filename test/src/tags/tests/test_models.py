import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.core.urlresolvers import reverse



class TestTag:

	def test_model_tagpoll_create(self):
		obj = mixer.blend('tags.TagPoll')
		assert obj.pk == 1, 'Should create a ptype instance'

	def test_model_ptype_get_update(self):
		obj = mixer.blend('tags.TagPoll')
		result = obj.get_absolute_url()
		assert result == reverse("TagView", kwargs={"pk":1}), 'Should be absolute url to edit'



class TestTopic:

	def test_model_topicpoll(self):
		obj = mixer.blend('tags.TagPoll')
		assert obj.pk == 1, 'Should create a pitem instance'




