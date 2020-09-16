from django import forms
from users.models import PUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios, FieldWithButtons, StrictButton
import datetime
from polls.models import PollItem, Ptype
from variable.models import TypeTopic, TypeYear, TypeLocation
from captcha.fields import ReCaptchaField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from messaging.models import Message
from django.forms import ModelForm, Textarea





class PollItemMessageAddForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = [
			"content"
		]

		labels = {
			'content': 'Add your comment',
		}

		widgets = {
			# you can change 'maxlength' of textarea here:
			'content': Textarea(attrs={'cols': 10, 'rows': 5, 'maxlength': 200}),
		}


	def __init__(self, *args, **kwargs):

		# this line should be before a super call
		self.request = kwargs.pop('request', None)

		super(PollItemMessageAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Post', css_class='buttonspace btn-success'))


	def clean_content(self):
		content = self.cleaned_data.get("content")

		if len(str(content)) > 200:
			raise forms.ValidationError("Please limit your message to less the 200 characters")

		return content



# the comment module is dormant but lets the users leave messages on the poll detail - currently its done by facebook.
class PollItemMessageUpdateForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = [
			"content"
		]	

		labels = {
			'content': 'Update your comment',
		}

		help_texts = {
			'content': 'Note that updating comment will reset likes',
		}

		widgets = {
			# you can change 'maxlength' of textarea here:
			'content': Textarea(attrs={'cols': 10, 'rows': 5, 'maxlength': 200}),
		}


	def __init__(self, *args, **kwargs):

		# this line should be before a super call
		self.request = kwargs.pop('request', None)


		# """If no initial data, provide some defaults."""
		# initial = kwargs.get('initial', {})
		# initial['name'] = 'initial_name'
		# kwargs['initial'] = initial


		super(PollItemMessageUpdateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Post', css_class='btn buttonspace btn-sm btn-primary'))

		self.fields['content'].value = 'bar'

	def clean_content(self):
		content = self.cleaned_data.get("content")

		if len(str(content)) > 200:
			raise forms.ValidationError("Please limit your message to less the 200 characters")

		return content





