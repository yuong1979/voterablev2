from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
# from blog.models import BlogPost
from polls.models import PollItem, Ptype

class StaticViewSitemap(sitemaps.Sitemap):
	priority = 0.5
	changefreq = 'daily'

	def items(self):
		# return ['Home', 'Contact', 'TermsAndCondition', 'Disclaimer', 'PrivacyPolicy',
		# 'FAQ', 'Customer_Support', 'AboutUs','Press', 'Partnership', 'TeacherList', 
		# 'StudentList', 'OpeningList', 'blog_list', 'poll_topics', 'polls_list', 
		# 'polls_detail','PollSearchView','TagView']

		return ['Home', 'Contact', 'TermsAndCondition', 'Disclaimer', 'PrivacyPolicy', 'FAQ', 'Customer_Support',
			'AboutUs','Press', 'Partnership', 'poll_topics', 'polls_list', 'PollSearchView']



	def location(self, item):
		return reverse(item)


class PollsSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.5

	def items(self):
		return PollItem.objects.filter(allowed=True)

	def lastmod(self, obj):
		return obj.date

	def location(self, obj):
		return "/polls/" + str(obj.pk) + "/"



class PollsTypeSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.5

	def items(self):
		return Ptype.objects.filter(active=True)

	def lastmod(self, obj):
		return obj.date

	def location(self, obj):
		return "/polls/?type=" + str(obj.slug) + "/"




# class BlogSitemap(Sitemap):
# 	changefreq = "daily"
# 	priority = 0.5

# 	def items(self):
# 		return BlogPost.objects.filter(draft=False)

# 	def lastmod(self, obj):
# 		return obj.updated_at

# 	def location(self, obj):
# 		return "/" + obj.slug + "/"