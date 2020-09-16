from django import template

register = template.Library()


from messaging.models import Message



# simple tags are for simple functions
@register.simple_tag
def total_posts():
	# test = Message.senduser.count()
	test = "dude"
	return test


# previously assignment_tags - now changed to simple_tag - for queries
@register.simple_tag
def get_most_commented_posts(count=5):
	test1 = Message.objects.filter()
	return test1