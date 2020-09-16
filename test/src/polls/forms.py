from django import forms
from users.models import PUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios, FieldWithButtons, StrictButton
import datetime
from polls.models import PollItem, Ptype, SuggestedPoll
from variable.models import TypeTopic, TypeYear, TypeLocation
from captcha.fields import ReCaptchaField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from messaging.models import Message
from django.forms import ModelForm, Textarea
from django.urls import reverse



class PollRecoAddForm(forms.ModelForm):

	class Meta:
		model = SuggestedPoll
		fields = [
			"title",
		]
		labels = {
			'title': 'Make your recommendation',
		}
		widgets = {
			# you can change 'maxlength' of textarea here:
			'title': Textarea(attrs={'cols': 10, 'rows': 5, 'maxlength': 200}),
		}


	def __init__(self, *args, **kwargs):

		super(PollRecoAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_id = 'poll_recc_form'
		self.helper.form_action = reverse('PollRecoView')
		self.helper.add_input(Submit('submit', value='Post', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))
		self.helper.layout = Layout(

			# HTML("""<br>"""),

			Fieldset(
				'',

				Div(Field('title'), css_class='col-xs-12 col-sm-12 col-md-12'),
				HTML("""<div class="row"></div>"""),

			),

		)

	#issue display the validation error on the 
	def clean_title(self):

		title = self.cleaned_data.get("title")
		posted_titles = [str(obj.title) for obj in SuggestedPoll.objects.filter(allowed=True)]
		if not title or len(title) < 20:
			raise forms.ValidationError("Please do your title with more than the 20 characters")
		elif len(title) > 80:
			raise forms.ValidationError("Please limit your title to less than 80 characters")
		elif title in posted_titles:
			raise forms.ValidationError("This recommendation has already been submitted.")

		return title




class PollSuggAddForm(forms.ModelForm):

	class Meta:
		model = SuggestedPoll
		fields = [
			"title",
		]
		labels = {
			'title': 'Add your suggestion',
		}
		widgets = {
			# you can change 'maxlength' of textarea here:
			'title': Textarea(attrs={'cols': 10, 'rows': 5, 'maxlength': 200}),
		}


	def __init__(self, *args, **kwargs):

		super(PollSuggAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_id = 'poll_sugg_form'
		self.helper.form_action = reverse('PollSuggView')
		self.helper.add_input(Submit('submit', value='Post', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))
		self.helper.layout = Layout(

			# HTML("""<br>"""),

			Fieldset(
				'',

				Div(Field('title'), css_class='col-xs-12 col-sm-12 col-md-12'),
				HTML("""<div class="row"></div>"""),

			),

		)


	def clean_title(self):

		title = self.cleaned_data.get("title")
		posted_titles = [str(obj.title) for obj in SuggestedPoll.objects.filter(allowed=True)]
		if not title or len(title) < 20:
			raise forms.ValidationError("Please do your title with more than the 20 characters")
		elif len(title) > 80:
			raise forms.ValidationError("Please limit your title to less than 80 characters")
		elif title in posted_titles:
			raise forms.ValidationError("This suggestion has already been submitted.")

		return title
	# def clean_title(self):

	# 	title = self.cleaned_data.get("title")
	# 	if len(str(title)) > 80:
	# 		raise forms.ValidationError("Please limit your title to less than 80 characters")
	# 	if len(str(title)) < 40:
	# 		raise forms.ValidationError("Please do your title with more than the 20 characters")

	# 	return title



















## I have removed captcha because it is not working on production
class PollTopicAddForm(forms.ModelForm):

	# captcha = ReCaptchaField()

	class Meta:
		model = Ptype
		fields = [

			"title",
			# "year",
			# "location",
			"topic",
			# "subtopic",
			"description",
			"image",
			# "captcha",
		]

		labels = {
			'title': 'Title of your tip list',
			# 'image': 'Load relevant image',
			'description': 'Description of your tip list',
		}

		widgets = {
			'title': Textarea(attrs={'cols': 10, 'rows': 2, 'maxlength': 200}),
		}

	def __init__(self, *args, **kwargs):

		# this line should be before a super call
		self.request = kwargs.pop('request', None)

		super(PollTopicAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Post', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))

		self.helper.layout = Layout(

			HTML("""<br><br>"""),

			Fieldset(
				'',

				Div(Field('title'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				Div(Field('tags'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div><br>"""),

				# Div(InlineRadios('year'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div><br>"""),

				# Div(InlineRadios('location'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div><br>"""),

				Div(InlineRadios('topic'), css_class='col-xs-12 col-md-12 col-lg-12'),
				HTML("""<div class="row"></div><br>"""),

				# Div(Field('subtopic'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				Div(Field('description'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				Div(Field('image'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				# Div(Field('captcha'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# Div(InlineRadios('level'), css_class='col-xs-12 col-md-12 col-lg-12'),

				# Div(InlineRadios('gender'), css_class='col-xs-12 col-sm-10 col-md-8'),

			),

		)

	#topic
	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(str(title)) > 80:
			raise forms.ValidationError("Please limit your title to less than 80 characters")
		if len(str(title)) < 10:
			raise forms.ValidationError("Please do your title with more than the 10 characters")

		return title

	#topic
	def clean_description(self):
		description = self.cleaned_data['description']
		if len(str(description)) > 150:
			raise forms.ValidationError("Please limit your description to less than 150 characters")
		if len(str(description)) < 20:
			raise forms.ValidationError("Please do your description with more than the 20 characters")
		return description



	tags = forms.CharField(
		widget=Textarea(attrs={'cols': 10, 'rows': 2, 'maxlength': 200}),
		# empty_label=None,
		label='Relevant Tags',
		help_text="Example: Marketing, Social Media Marketing, Startup",
		required=False
		# required=True
	)

	topic = forms.ModelChoiceField(
		widget=forms.RadioSelect,
		empty_label=None,
		queryset=TypeTopic.objects.filter(active=True),
		label="Topics",
		required=True
	)










class PollTopicEditForm(forms.ModelForm):

	# captcha = ReCaptchaField()

	class Meta:
		model = Ptype
		fields = [

			"title",
			# "year",
			# "location",
			"topic",
			# "subtopic",
			"description",
			"image",
			# "captcha",
		]

		labels = {
			'title': 'Title of your tip list',
			# 'image': 'Load relevant image',
			'description': 'Description of your tip list',
		}

		widgets = {
			'title': Textarea(attrs={'cols': 10, 'rows': 2, 'maxlength': 200}),
		}


	def __init__(self, *args, **kwargs):

		# this line should be before a super call
		self.request = kwargs.pop('request', None)

		super(PollTopicEditForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Post', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))


		self.helper.layout = Layout(

			HTML("""<br><br>"""),

			Fieldset(
				'',

				Div(Field('title'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				Div(Field('tags'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div><br>"""),

				# Div(InlineRadios('year'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div><br>"""),

				# Div(InlineRadios('location'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div><br>"""),

				Div(InlineRadios('topic'), css_class='col-xs-12 col-md-12 col-lg-12'),
				HTML("""<div class="row"></div><br>"""),

				# Div(Field('subtopic'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				Div(Field('description'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				Div(Field('image'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				# Div(Field('captcha'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# Div(InlineRadios('level'), css_class='col-xs-12 col-md-12 col-lg-12'),

				# Div(InlineRadios('gender'), css_class='col-xs-12 col-sm-10 col-md-8'),

			),

		)

	#topic
	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(str(title)) > 80:
			raise forms.ValidationError("Please limit your title to less than 80 characters")
		if len(str(title)) < 10:
			raise forms.ValidationError("Please do your title with more than the 10 characters")

		return title

	#topic
	def clean_description(self):
		description = self.cleaned_data['description']
		if len(str(description)) > 150:
			raise forms.ValidationError("Please limit your description to less than 150 characters")
		if len(str(description)) < 20:
			raise forms.ValidationError("Please do your description with more than the 20 characters")
		return description

	# def common_clean_images(self, name):

	# 	image = self.cleaned_data.get(name, False)
	# 	if image and getattr(self.instance, name) != image:
	# 		if image.size > 2.0*1024*1024:
	# 			raise forms.ValidationError("Image file too large ( > 2.0 mb )")
	# 	return image


	# def clean_image(self):
	# 	return self.common_clean_images('image')





	tags = forms.CharField(
		widget=Textarea(attrs={'cols': 10, 'rows': 2, 'maxlength': 200}),
		# empty_label=None,
		label='Relevant Tags',
		help_text="Example: Marketing, Social Media Marketing, Startup",
		required=False
		# required=True
	)

	topic = forms.ModelChoiceField(
		widget=forms.RadioSelect,
		empty_label=None,
		queryset=TypeTopic.objects.filter(active=True),
		label="Topics",
		required=True
	)









class PollItemAddForm(forms.ModelForm):

	# captcha = ReCaptchaField()

	class Meta:
		model = PollItem
		fields = [

			"title",
			# "image",
			# "imageurl",
			# "imgatt",
			"description",
			"textatt",
			# "url",
			# "ytubeurl",
			# "fburl",
			# "googurl",
			# "yelpurl",
		]

		labels = {
			'title': 'Title of your Tip',
			'image': 'Upload your image',
			'imageurl': 'Link to image',
			'description': 'Description of your Tip',
			# "imgatt": 'Image Attibution',
			"textatt": 'Please credit your source (if any)',

			# 'url': 'Web Link',
			# 'ytubeurl': 'Youtube Link',
			# 'fburl': 'Facebook Link',
			# 'googurl': 'Google Link',
			# 'yelpurl': 'Yelp Link',
		}

		widgets = {
			'title': Textarea(attrs={'cols': 10, 'rows': 2, 'maxlength': 200}),
			'description': SummernoteInplaceWidget(),
		}


	def __init__(self, *args, **kwargs):
		super(PollItemAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Preview', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))
		self.helper.layout = Layout(

		Fieldset(
			'',

			Div(Field('title'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),

			Div(Field('description'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),


			Div(Field('textatt'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),

			# HTML("""<div class="panel-group col-xs-12 col-sm-10 col-md-8" id="accordion">
			#             <div class="card cardstyle">
			# 					<div class="card-body" style='background-color: lightgrey;'>
			# 						<a data-toggle="collapse" data-parent="#accordion" href="#collapseOne"><b>Upload Thumbnail</b></a>
			# 					</div>
   #          				<div id="collapseOne" class="panel-collapse collapse">
			# 					<div class="panel-body">"""),

			# HTML("""<div class="row"><br></div>"""),

			# Div(Field('image'), css_class='col-xs-12 col-sm-10 col-md-8'),

			# HTML("""<div class="row"><br></div>"""),

			# HTML("""<div class="col-xs-12 col-sm-10 col-md-8"><b> -- Or -- </b></div><br><br>"""),

			# Div(Field('imageurl'), css_class='col-xs-12 col-sm-10 col-md-8'),
			# HTML("""<div class="row"></div>"""),

			# Div(Field('imgatt'), css_class='col-xs-12 col-sm-10 col-md-8'),
			# HTML("""<div class="row"></div>"""),
			
			# HTML("""</div></div></div>

   #      <div class="panel panel-default">
   #          <div class="panel-heading">
   #              <h4 class="panel-title">
   #                  <a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">Submit Link (Optional)</a>
   #              </h4>
   #          </div>
   #          <div id="collapseTwo" class="panel-collapse collapse">
   #              <div class="panel-body">"""),


			# Div(Field('url'), css_class='col-xs-12 col-sm-10 col-md-8'),
			# HTML("""<div class="row"></div>"""),

			# Div(Field('ytubeurl'), css_class='col-xs-12 col-sm-10 col-md-8'),
			# HTML("""<div class="row"></div>"""),

			# Div(Field('fburl'), css_class='col-xs-12 col-sm-10 col-md-8'),
			# HTML("""<div class="row"></div>"""),

			# Div(Field('googurl'), css_class='col-xs-12 col-sm-10 col-md-8'),
			# HTML("""<div class="row"></div>"""),

			# Div(Field('yelpurl'), css_class='col-xs-12 col-sm-10 col-md-8'),
			# HTML("""<div class="row"></div>"""),

			# Div(Field('captcha'), css_class='col-xs-12 col-sm-10 col-md-8'),
			# HTML("""<div class="row"></div>"""),

		),
		)



	image = forms.ImageField(
		label="Load image",
		required=False,
	)

	def common_clean_images(self, name):

		image = self.cleaned_data.get(name, False)
		if image and getattr(self.instance, name) != image:
			if image.size > 2.0*1024*1024:
				raise forms.ValidationError("Image file too large ( > 2.0 mb )")
		return image


	def clean_image(self):
		return self.common_clean_images('image')

	# poll item
	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(str(title)) > 120:
			raise forms.ValidationError("Please limit your title to less than 120 characters")
		if len(str(title)) < 20:
			raise forms.ValidationError("Please do your title with more than the 20 characters")
		return title

	# poll item
	def clean_description(self):
		description = self.cleaned_data['description']

		if len(str(description)) > 5000:
			raise forms.ValidationError("Please limit your description to less than 2400 characters")
		if len(str(description)) < 20:
			raise forms.ValidationError("Please input your tip description with more then 20 characters")
		return description







	# def clean_ytubeurl(self):
	# 	ytubeurlu = self.cleaned_data.get("ytubeurl", False)
	# 	ytubeurl = ytubeurlu[0:23]
	# 	if ytubeurl != "https://www.youtube.com" and ytubeurlu != "":
	# 		raise forms.ValidationError("Please use a youtube url")
	# 	return ytubeurlu


	# def clean_fburl(self):
	# 	fburlu = self.cleaned_data.get("fburl", False)
	# 	fburl = fburlu[0:24]
	# 	if fburl != "https://www.facebook.com" and fburlu != "":
	# 		raise forms.ValidationError("Please use a facebook url")
	# 	return fburlu


	# def clean_googurl(self):
	# 	googurlu = self.cleaned_data.get("googurl", False)
	# 	googurl = googurlu[0:22]
	# 	if googurl != "https://www.google.com" and googurlu != "":
	# 		raise forms.ValidationError("Please use a google url")
	# 	return googurlu


	# def clean_yelpurl(self):
	# 	yelpurlu = self.cleaned_data.get("yelpurl", False)
	# 	yelpurl = yelpurlu[0:20]
	# 	if yelpurl != "https://www.yelp.com" and yelpurlu != "":
	# 		raise forms.ValidationError("Please use a yelp url")
	# 	return yelpurlu




class PollItemEditForm(forms.ModelForm):
    # tags = forms.CharField(label='Please add relevant skills - special needs, piano, java-programming', required=False)

	class Meta:
		model = PollItem
		fields = [

			"title",
			# "image",
			# "imageurl",
			# "imgatt",
			"description",
			"textatt",
			# "url",
			# "ytubeurl",
			# "fburl",
			# "googurl",
			# "yelpurl",
		]

		labels = {
			'title': 'Title of your Tip',
			'image': 'Upload your image',
			'imageurl': 'Link to image',
			'description': 'Description of your Tips',
			# "imgatt": 'Image Attibution',
			"textatt": 'Please credit your source (if any)',

			# 'url': 'Source Link',
			# 'ytubeurl': 'Youtube Link',
			# 'fburl': 'Facebook Link',
			# 'googurl': 'Google Link',
			# 'yelpurl': 'Yelp Link',
		}

		widgets = {
			'title': Textarea(attrs={'cols': 10, 'rows': 2, 'maxlength': 200}),
			'description': SummernoteInplaceWidget(),
		}



	def __init__(self, *args, **kwargs):

		# this line should be before a super call
		self.request = kwargs.pop('request', None)

		super(PollItemEditForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Preview', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))


		self.helper.layout = Layout(

			# HTML("""<br><br>"""),

			Fieldset(
				'',

				Div(Field('title'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				Div(Field('description'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				Div(Field('textatt'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				# HTML("""<div class="panel-group col-xs-12 col-sm-10 col-md-8" id="accordion">
				#             <div class="card cardstyle">
				# 					<div class="card-body" style='background-color: lightgrey;'>
				# 						<a data-toggle="collapse" data-parent="#accordion" href="#collapseOne"><b>Upload Thumbnail</b></a>
				# 					</div>
	   #          				<div id="collapseOne" class="panel-collapse collapse">
				# 					<div class="panel-body">"""),

				# HTML("""<div class="row"><br></div>"""),

				# Div(Field('image'), css_class='col-xs-12 col-sm-10 col-md-8'),

				# HTML("""<div class="row"><br></div>"""),

				# HTML("""<div class="col-xs-12 col-sm-10 col-md-8"><b> -- Or -- </b></div><br><br>"""),

				# Div(Field('imageurl'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# Div(Field('imgatt'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# HTML("""</div></div></div>

    #         <div class="panel panel-default">
    #             <div class="panel-heading">
    #                 <h4 class="panel-title">
    #                     <a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">Submit Link (Optional)</a>
    #                 </h4>
    #             </div>
    #             <div id="collapseTwo" class="panel-collapse collapse">
    #                 <div class="panel-body">"""),

				# Div(Field('url'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# Div(Field('ytubeurl'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# Div(Field('fburl'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# Div(Field('googurl'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# Div(Field('yelpurl'), css_class='col-xs-12 col-sm-10 col-md-8'),
				# HTML("""<div class="row"></div>"""),

				# HTML("""</div></div></div></div>"""),



			),

        )

	def common_clean_images(self, name):

		image = self.cleaned_data.get(name, False)
		if image and getattr(self.instance, name) != image:
			if image.size > 2.0*1024*1024:
				raise forms.ValidationError("Image file too large ( > 2.0 mb )")
		return image


	def clean_image(self):
		return self.common_clean_images('image')


	# poll item
	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(str(title)) > 120:
			raise forms.ValidationError("Please limit your title to less than 120 characters")
		if len(str(title)) < 20:
			raise forms.ValidationError("Please do your title with more than the 20 characters")
		return title

	# poll item
	def clean_description(self):
		description = self.cleaned_data['description']

		if len(str(description)) > 5000:
			raise forms.ValidationError("Please limit your description to less than 2400 characters")
		if len(str(description)) < 20:
			raise forms.ValidationError("Please input your tip description with more then 20 characters")
		return description


	# def clean_ytubeurl(self):
	# 	ytubeurlu = self.cleaned_data.get("ytubeurl", False)
	# 	ytubeurl = ytubeurlu[0:23]
	# 	if ytubeurl != "https://www.youtube.com" and ytubeurlu != "":
	# 		raise forms.ValidationError("Please use a youtube url")
	# 	return ytubeurlu


	# def clean_fburl(self):
	# 	fburlu = self.cleaned_data.get("fburl", False)
	# 	fburl = fburlu[0:24]
	# 	if fburl != "https://www.facebook.com" and fburlu != "":
	# 		raise forms.ValidationError("Please use a facebook url")
	# 	return fburlu


	# def clean_googurl(self):
	# 	googurlu = self.cleaned_data.get("googurl", False)
	# 	googurl = googurlu[0:22]
	# 	if googurl != "https://www.google.com" and googurlu != "":
	# 		raise forms.ValidationError("Please use a google url")
	# 	return googurlu


	# def clean_yelpurl(self):
	# 	yelpurlu = self.cleaned_data.get("yelpurl", False)
	# 	yelpurl = yelpurlu[0:20]
	# 	if yelpurl != "https://www.yelp.com" and yelpurlu != "":
	# 		raise forms.ValidationError("Please use a yelp url")
	# 	return yelpurlu



# class PollDetailStaffPreviewForm(forms.Form):

# 	def __init__(self, *args, **kwargs):

# 		super(PollDetailStaffPreviewForm, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_method = 'post'
# 		self.helper.add_input(Submit('submit', value='Save', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))
# 		self.helper.layout = Layout(

# 			Div(Field('termsandconditions'), css_class='col-xs-12 col-md-12'),

#         )

# 	termsandconditions = forms.BooleanField(
# 		required=True,
# 		label="""
# 		<p>
# 		<b>
# 		This preview is ok
# 		</b>
# 		</p>
# 		"""
# 	)


























class PollItemDeleteForm(forms.ModelForm):
    # tags = forms.CharField(label='Please add relevant skills - special needs, piano, java-programming', required=False)

	class Meta:
		model = PollItem
		fields = [

			# "title",

		]

		# labels = {
		# 	'title': 'Title of your Entry',

		# }


	def __init__(self, *args, **kwargs):

		# this line should be before a super call
		self.request = kwargs.pop('request', None)

		super(PollItemDeleteForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Delete Post', css_class='buttonspace btn-sm btn-success', style='font-weight: bold;'))


		self.helper.layout = Layout(

			# HTML("""<br><br>"""),

			Fieldset(
				# '',

				# Div(Field('title'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				HTML("""<div class="col-xs-12">

					<p>
					Please confirm post deletion.
					</p>

					</div>"""),


			),

        )



















#this works
class SearchForm(forms.Form):
    search = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):

        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(

            Fieldset(
                '',
                FieldWithButtons('search', Submit('submit', value='Search', css_class='btn-primary', style='font-weight: bold;'))
            ),
        )
    
    search = forms.CharField(
        required=True,
        label=""
    )

