import pytest
from mixer.backend.django import mixer
from django.contrib.admin.sites import AdminSite
pytestmark = pytest.mark.django_db

from .. import admin
from .. import models

class TestTagAdmin:
	def test_tagpoll__str__(self):
		site = AdminSite()
		tags_admin = admin.TagPollAdmin(models.TagPoll, site)
		obj = mixer.blend('tags.TagPoll', title='Hello World')
		result = tags_admin.__str__(obj)
		assert result == 'Hello World', 'Should return the first few characters'


	def test_topicpoll__str__(self):
		site = AdminSite()
		tags_admin = admin.TopicPollAdmin(models.TopicPoll, site)
		obj = mixer.blend('tags.TopicPoll', title='Hello World')
		result = tags_admin.__str__(obj)
		assert result == 'Hello World', 'Should return the first few characters'



