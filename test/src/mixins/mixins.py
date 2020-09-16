from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users.models import PUser
from django.contrib import messages
from polls.models import PollItem, PollFav, Ptype, SuggestedPoll
# from sellers.mixins import SellerAccountMixin

# class ProductManagerMixin(object):
#     def get_object(self, *args, **kwargs):
#         obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)
#         user = self.request.user
#         if obj.user == user:
#             return obj
#         else:
#             raise Http404

class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class UserChangeManagerMixin(object):
		def get_object(self, *args, **kwargs):
				obj = super(UserChangeManagerMixin, self).get_object(*args, **kwargs)
				user = self.request.user
				if obj.user == user:
						return obj
				else:
						raise Http404


class PollTypeMixin(object):
	def get_pobject(self, *args, **kwargs):

		#checking which type of list user is user
		try:
			type_slug = self.request.GET.get("type")
			poll_type = Ptype.objects.get(slug = type_slug)
		except:
			try:
				type_slug = self.request.GET.get("favorite")
				poll_type = Ptype.objects.get(slug = type_slug)			
			except:
				try:
					type_slug = self.request.GET.get("create")
					poll_type = Ptype.objects.get(slug = type_slug)
				except:
					try:
						type_slug = self.request.GET.get("createduser")
						poll_type = Ptype.objects.get(slug = type_slug)

					except:

						return redirect('Home')




		return poll_type




# class GetDetailsMixin(object):

# 		def get_msg(self, *args, **kwargs):
# 				msg_id = self.request.session.get("msg_id")
# 				msg = get_object_or_404(Message, pk=msg_id)
# 				# parent_msg_id = msg.parent_id
# 				# msg = get_object_or_404(Message, pk=parent_msg_id)
# 				return msg

# 		def get_opening(self, *args, **kwargs):
# 				msg = self.get_msg()
# 				opening = msg.re_opening
# 				return opening

# 		def get_student(self, *args, **kwargs):
# 				opening = self.get_opening()
# 				student = opening.hiring_student
# 				return student

# 		def get_teacher(self, *args, **kwargs):
# 				try:
# 						teacher = self.get_msg().senduser.teacher
# 				except:
# 						teacher = self.get_msg().touser.teacher
# 				return teacher

# 		def get_order(self, *args, **kwargs):
# 				order_id = self.request.session.get("order_id")
# 				order = Order.objects.get(pk=order_id)
# 				return order


# class GetCheckoutMixin(object):

# 		def get_user_cred(self, *args, **kwargs):
# 			user = self.request.user
# 			usercred_obj = get_object_or_404(UserCredit, user=user)
# 			usercred = usercred_obj.credit
# 			return usercred

# 		def get_credit_cost(self, *args, **kwargs):
# 			credit_id = self.request.session.get("credit_id")
# 			credit_pack = get_object_or_404(CreditToCash, id=credit_id)
# 			creditcost = credit_pack.cashprice
# 			return creditcost

# 		def get_credit(self, *args, **kwargs):
# 			credit_id = self.request.session.get("credit_id")
# 			credit_pack = get_object_or_404(CreditToCash, id=credit_id)
# 			credit = credit_pack.credits
# 			return credit

# 		def get_transaction(self, *args, **kwargs):
# 				transaction_id = self.request.session.get("transaction_id")
# 				transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
# 				return transaction


