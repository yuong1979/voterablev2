from django import forms
from users.models import PUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios
import datetime

class PUserAddForm(forms.ModelForm):
	error_css_class = 'error'

	class Meta:
		model = PUser


		fields = [
			# "name",
			# "description",
			# "image",
			# "contact",
		]


	def __init__(self, *args, **kwargs):
		super(PUserAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Proceed', css_class='buttonspace btn-sm btn-success'))
		self.helper.layout = Layout(

		Fieldset(

			HTML("""<br><br>"""),

			HTML("""<div class="container">"""),	

			Div(Field('termsandconditions'), css_class='col-xs-12'),

			HTML("""</div>"""),

			## reimplement referralcode if needed
			# Div(Field('referralcode'), css_class='col-xs-12 col-sm-4 col-md-3'),

		)

		)


	termsandconditions = forms.BooleanField(
		required=True,
		label="""
		&nbsp;&nbsp;&nbsp;
		<b>
        I understand and agree to the voterable 
        <a href='/termsandconditions/' >Terms and conditions</a>, 
        <a href='/disclaimer/' >Disclaimer</a>,
        <a href='/privacypolicy/' >Privacy Policy.</a>
        </b>

        """
	)


	referralcode = forms.CharField(
		required=False,
		label="""
		<b>
        Referral code (if any)
        </b>

        """
	)


	def clean_referralcode(self):
		referralcode = self.cleaned_data.get("referralcode")

		if referralcode != "":
			try:
				referring_obj = PUser.objects.get(referralid=referralcode)
			except PUser.DoesNotExist:
				# check if the referral code belongs to a puser

				raise forms.ValidationError("Please use a valid referral code")
		return referralcode






class PUserEditForm(forms.ModelForm):

	# print (request.user)

	class Meta:
		model = PUser
		fields = [

			"name",
			"image",
			"description",
			"alt_email",

			# "subnewsletter",

			# "contact",
		]


		labels = {
			'name': 'Change your Name',
			'description': 'Describe Yourself',
			'alt_email': 'Your Alternate Email (For Notifications)',
			'image': 'Upload Your Picture',

			# 'subnewsletter': 'Subscribe notifications on your favorite tips and be updated on the latest and most powerful tips and tricks and exclusive deals and online events.',

		}


  #       help_texts = {
		# 	'name': 'Not required',
		# 	'description': 'Not required',
  #       }



	def __init__(self, *args, **kwargs):

		# print (kwargs.pop('instance',None))

		# test = kwargs.pop('instance',None)

		# print (test)

		# print (PUser.objects.filter(user=test))


		super(PUserEditForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Save', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))
		self.helper.layout = Layout(

		# HTML("""<br><br>"""),

		Fieldset(

			'',

			HTML("""<div class="row"><br></div>"""),

			Div(Field('name'), css_class='col-xs-12 col-sm-6 col-md-4'),
			HTML("""<div class="row"><br></div>"""),


			Div(Field('description'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"><br></div>"""),

			Div(Field('alt_email'), css_class='col-xs-10 col-sm-8 col-md-6'),
			HTML("""<div class="row"><br></div>"""),

			Div(Field('image'), css_class='col-xs-12 col-sm-6 col-md-4', style='background-color: lightgray; border-radius: 3px; margin: 0px 10px 5px 0px; padding: 18px;'),
			HTML("""<div class="row"><br></div>"""),

			# Div(Field('subnewsletter'), css_class='col-xs-10 col-sm-8 col-md-6', style='background-color: lightgray; border-radius: 3px; margin: 0px 10px 15px 15px; padding: 5px;'),
			# HTML("""<div class="row"><br><br><br><br></div>"""),

		),

		)

	def clean_description(self):
		description = self.cleaned_data['description']
		if len(str(description)) > 300:
			raise forms.ValidationError("Please use less then 300 characters")
		return description


	def clean_name(self):
		name = self.cleaned_data['name']
		if name:
			if PUser.objects.exclude(pk=self.instance.pk).filter(name=name).exists():
				raise forms.ValidationError(u'Name "%s" is already in use.' % name)
			return name

    # first_level = forms.ModelMultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Level_Expertise.objects.all(),
    #     label="Level",
    #     required=True
    # )


    # first_level = forms.ModelMultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Level_Expertise.objects.all(),
    #     label="Level",
    #     required=True
    # )

    # second_level = forms.ModelMultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Level_Expertise.objects.all(),
    #     label="Level",
    #     required=False
    # )

    # third_level = forms.ModelMultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Level_Expertise.objects.all(),
    #     label="Level",
    #     required=False
    # )


    # educational_level = forms.ModelMultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Educational_Level.objects.all(),
    #     label="Your Level of Education"
    # )

    # education_school = forms.ModelMultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Education_School.objects.all(),
    #     label="Your Education Institute"
    # )


    # years_of_experience = forms.ChoiceField(
    #     required=True,
    #     choices=exp_choices,
    #     label="Years of Experience"
    # )


    # salary_expectation = forms.ChoiceField(
    #     required=True,
    #     choices=pay_choices,
    #     label="Asking Rate/Hour"
    # )

    # region = forms.ModelMultipleChoiceField(
    #     required=True,
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Region.objects.all(),
    #     label="Your Preferred Locations"
    # )