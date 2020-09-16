# import pytest
# from django.test import RequestFactory
# from django.urls import reverse
# from mixer.backend.django import mixer
# from django.contrib.auth.models import User
# from .. import views
# pytestmark = pytest.mark.django_db
# from polls.views import PollDetailView
# from django.test import Client
# from django.test import TestCase
# from polls.models import PollItem, Ptype
# from users.models import PUser
# from polls.views import PollsListView




# class TestViews(TestCase):

# 	def setUp(self):
# 		self.client = Client()

# 		self.user = User.objects.create_user(
# 			username='normaluser', email='s@gmail.com', password='secret123')

# 		self.notcreateuser = User.objects.create_user(
# 			username='notcreateuser', email='s@gmail.com', password='secret123')

# 		self.adminuser = User.objects.create_user(
# 			username='adminuser', email='s@gmail.com', password='secret123', is_staff=True)

# 		obj_puser = mixer.blend('users.PUser', user=self.user)
# 		obj_puser_oth = mixer.blend('users.PUser', user=self.notcreateuser)
# 		obj_puser_staff = mixer.blend('users.PUser', user=self.adminuser)

# 		obj_ptype = mixer.blend('polls.Ptype', active=True)
# 		obj_pitem0 = mixer.blend('polls.PollItem', polltype=obj_ptype, user_submit=self.user, allowed=True)
# 		obj_pitem1 = mixer.blend('polls.PollItem', polltype=obj_ptype, user_submit=self.user, allowed=True)




# 	# def test_poll_list_view_query(self):
# 	# 	self.client.login(username="normaluser", password="secret123")
# 	# 	ptype_obj = Ptype.objects.get(pk__in=[1])
# 	# 	path = "/polls/"
# 	# 	data = {'type': ptype_obj.slug }
# 	# 	res = self.client.get(path, data)


# 	# 	pitemlist = PollItem.objects.filter(pk__in=[1,2])

# 	# 	#list of assertqueriesequal I am testing
# 	# 	# self.assertQuerysetEqual(res.context['object_list'], [repr(r) for r in pitemlist])
# 	# 	# self.assertQuerysetEqual(res.context['object_list'], pitemlist, transform=lambda x:x)
# 	# 	# self.assertQuerysetEqual(res.context['object_list'], map(repr, pitemlist))

# 	# 	self.assertQuerysetEqual(res.context['object_list'], pitemlist)






# 	def test_poll_detail_view(self):
# 		self.client.login(username="normaluser", password="secret123")
# 		path = reverse('polls_detail', kwargs={'pk':1})

# 		res = self.client.get(path)
# 		assert res.status_code == 200, 'Can be viewed by users logged in'

# 		pitem_obj = PollItem.objects.get(pk=1)
# 		pitem_obj.allowed = False
# 		pitem_obj.save()

# 		res = self.client.get(path)
# 		assert res.status_code == 302, 'disallowed pollitem cannot be viewed'


# 	def test_poll_detail_create_view(self):
# 		self.client.login(username="normaluser", password="secret123")
# 		path = reverse('polls_detail_create')
# 		ptype_obj = Ptype.objects.get(pk=1)

# 		data = {'type_slug': ptype_obj.slug }
# 		res = self.client.get(path, data)
# 		assert res.status_code == 302, 'Redirect if no type_slug in session'

# 		session = self.client.session
# 		session['type_slug'] = ptype_obj.slug
# 		session.save()

# 		data = {'type_slug': ptype_obj.slug }
# 		res = self.client.get(path, data)
# 		assert res.status_code == 200, 'User can add new poll'

# 		obj_puser = PUser.objects.get(pk=1)
# 		obj_puser.banned = True
# 		obj_puser.save()

# 		data = {'type_slug': ptype_obj.slug }
# 		res = self.client.get(path, data)
# 		assert res.status_code == 302, 'User cannot access if user is banned'


# 	def test_poll_detail_update_view(self):
# 		path = reverse('polls_detail_update', kwargs={'pk':1})

# 		self.client.login(username="notcreateuser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 302, 'User who did not create cannot view update page'

# 		self.client.login(username="normaluser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 200, 'User who create can view update page'

# 		self.client.login(username="adminuser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 200, 'staff/admin can view update page'


# 	def test_poll_detail_update_preview_view(self):
# 		path = reverse('polls_detail_preview', kwargs={'pk':1})

# 		self.client.login(username="notcreateuser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 302, 'User who create can view preview page'

# 		self.client.login(username="normaluser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 200, 'User who create can view update page'

# 		self.client.login(username="adminuser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 200, 'staff/admin can view update page'









# 	def test_poll_list_view(self):
# 		self.client.login(username="normaluser", password="secret123")
# 		ptype_obj = Ptype.objects.get(pk=1)

# 		path = "/polls/"
# 		data = {'type': ptype_obj.slug }

# 		res = self.client.get(path, data)
# 		assert res.status_code == 200, 'Can be called by anyone'

# 		ptype_obj.active = False
# 		ptype_obj.save()

# 		res = self.client.get(path, data)
# 		assert res.status_code == 302, 'Inactive ptype cannot be viewed'




# 	def test_poll_list_view(self):
# 		self.client.login(username="normaluser", password="secret123")
# 		ptype_obj = Ptype.objects.get(pk=1)

# 		path = "/polls/"
# 		data = {'type': ptype_obj.slug }

# 		res = self.client.get(path, data)
# 		assert res.status_code == 200, 'Can be called by anyone'

# 		ptype_obj.active = False
# 		ptype_obj.save()

# 		res = self.client.get(path, data)
# 		assert res.status_code == 302, 'Inactive ptype cannot be viewed'








# 	def test_poll_list_create(self):
# 		path = reverse('poll_list_create')

# 		self.client.login(username="adminuser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 200, 'staff can create new poll'

# 		self.client.login(username="normaluser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 302, 'normal users cannot create new poll'



# 	def test_poll_list_update(self):
# 		path = reverse('poll_list_update', kwargs={'pk':1})
# 		ptype_obj = Ptype.objects.get(pk=1)

# 		session = self.client.session
# 		session['type_slug'] = ptype_obj.slug
# 		session.save()

# 		self.client.login(username="adminuser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 200, 'staff can update poll list'

# 		self.client.login(username="normaluser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 302, 'who create poll list cannot update poll list'

# 		self.client.login(username="notcreateuser", password="secret123")
# 		res = self.client.get(path)
# 		assert res.status_code == 302, 'normal users cannot update poll list'








# 	def test_poll_list_favorite_fav(self):
# 		path = reverse('polls_favorite_list')
# 		ptype_obj = Ptype.objects.get(pk=1)
# 		data = {'favorite': ptype_obj.slug }

# 		self.client.login(username="notcreateuser", password="secret123")
# 		res = self.client.get(path, data)
# 		assert res.status_code == 200, 'users can view their favorite list'







# 	def test_poll_list_favorite_created(self):
# 		path = reverse('polls_favorite_list')
# 		ptype_obj = Ptype.objects.get(pk=1)
# 		data = {'create': ptype_obj.slug }

# 		self.client.login(username="notcreateuser", password="secret123")
# 		res = self.client.get(path, data)
# 		assert res.status_code == 200, 'users can view their create list'









































































# 	# def test_poll_list_update(self):
# 	# 	self.client.login(username="normaluser", password="secret123")
# 	# 	ptype_obj = Ptype.objects.get(pk=1)

# 	# 	path = "/polls/"
# 	# 	data = {'type': ptype_obj.slug }

# 	# 	res = self.client.get(path, data)
# 	# 	assert res.status_code == 200, 'Can be called by anyone'

# 	# 	ptype_obj.active = False
# 	# 	ptype_obj.save()

# 	# 	res = self.client.get(path, data)
# 	# 	assert res.status_code == 302, 'Inactive ptype cannot be viewed'








# # class TestPollsListView:
# # 	def test_anonymous(self):
# # 		req = RequestFactory().get('/')
# # 		print (req)
# # 		resp = views.PollsListView.as_view()(req)
# # 		assert resp.status_code == 200, 'Can be called by anyone'


# # class TestViews:

# # 	def test_product_detail(self):
# # 		path = reverse('detail', kwargs={'pk':1})
# # 		request = RequestFactory().get(path)
# # 		request.user = mixer.blend(User)

# # 		response = product_detail(request, pk=1)

# # 		assert response.status_code == 200, 'Can be called by anyone'


# # class MyViewTest(TestCase):
# #     def setUp(self):
# #         self.client = Client()
# #         self.user = User.objects.create_user(
# #             username='jacob', email='soos@i.com', password='vvggtt')

# #     def view_test(self):
# #         # Create an instance of a POST request.
# #         self.client.login(username="jacob", password="vvggtt")

# #         print ("1")
# #         data = {'name': 'test name'}
# #         res = self.client.post('/my-url/', data)
# #         print(res)
# #         self.assertEqual(res.status_code, 200)

# 		# session = self.client.session
# 		# session['type_slug'] = ptype_obj.slug
# 		# session.save()
# 		# print (self.client.session['type_slug'])