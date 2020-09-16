# import pytest
# from mixer.backend.django import mixer
# pytestmark = pytest.mark.django_db
# # from django.core.urlresolvers import reverse


# class TestPtype:
# 	def test_model_ptype_create(self):
# 		obj = mixer.blend('polls.Ptype')
# 		assert obj.pk == 1, 'Should create a ptype instance'

# 	def test_model_ptype_get_update(self):
# 		obj = mixer.blend('polls.Ptype', title="hello world!")
# 		result = obj.get_update()
# 		assert result == "/poll_list/1/edit", 'Should be absolute url to edit'

# 	def test_model_ptype_get_url(self):
# 		obj = mixer.blend('polls.Ptype')
# 		result = obj.get_url()
# 		assert result == "/polls/?type=" + str(obj.slug), 'Should be absolute url to the ptype'




# class TestPollItem:
# 	def test_model_pollitem_create(self):
# 		obj = mixer.blend('polls.PollItem')
# 		assert obj.pk == 1, 'Should create a pitem instance'

# 	def test_model_pollitem_get_update(self):
# 		obj = mixer.blend('polls.PollItem', title="hello world!")
# 		result = obj.get_update()
# 		assert result == "/polls/1/edit", 'Should be absolute url to edit'

# 	def test_model_pollitem_get_absolute_url(self):
# 		obj = mixer.blend('polls.PollItem')
# 		result = obj.get_absolute_url()
# 		assert result == "/polls/1/", 'Should be absolute url to the pitem'

# 	def test_model_pollitem_calc_score(self):
# 		obj = mixer.blend('polls.PollItem')
# 		result = obj.calc_score()
# 		# insert the calculation when people start voting




# class TestPollVoting:
# 	def test_model_pollvoting_create(self):
# 		obj = mixer.blend('polls.PollVoting')
# 		assert obj.pk == 1, 'Should create a new vote instance'



# class TestPollFav:
# 	def test_model_pollfav_create(self):
# 		obj = mixer.blend('polls.PollFav')
# 		assert obj.pk == 1, 'Should create a new favorite instance'







# # reverse('poll_list_update', kwargs={'pk': self.pk})


