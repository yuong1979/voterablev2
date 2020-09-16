from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios, FieldWithButtons, StrictButton
from billing.models import PriceToDays, Transaction
from django.core.exceptions import NON_FIELD_ERRORS

# from polls.models import PollItem, Ptype
from variable.models import TypeTopic, TypeYear, TypeLocation

from users.models import PUser




# class DaysAddForm(forms.Form):

# 	class Meta:
# 		# model = Transaction
# 		fields = [
# 			# "Credits",
# 			# "label",
# 			# "cashprice",
# 			# "daystoadd"
# 		]


# 	def __init__(self, *args, **kwargs):
# 		super(DaysAddForm, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_method = 'post'
# 		self.helper.add_input(Submit('submit', value='Confirm Selection', css_class='btn-success btn-sm buttonspace', style='font-weight: bold;'))

# 		self.helper.layout = Layout(

# 			HTML("""<br>"""),

# 			Fieldset(
# 				'',

# 				Div(Field('subtype'), css_class='col-xs-12 col-md-12 col-lg-12', style='font-size: 12px; font-weight: bold;'),
# 				HTML("""<div class="row"></div><br>"""),

# 			),
# 		)	

# 	subtype = forms.ModelChoiceField(
# 		widget=forms.RadioSelect,
# 		empty_label=None,
# 		queryset=PriceToDays.objects.filter(active=True),
# 		label='Days to Subscribe / USD',
# 		required=True
# 		)





# class CustomUserForm(forms.ModelForm):
# 	class Meta:
# 		model = PUser
# 		fields = [	
# 			'stripe_id'
# 			]













