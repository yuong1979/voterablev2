from django import forms
from captcha.fields import ReCaptchaField
# from home.models import Registration
# from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Education, Region, Education_School, Expertise_Type
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios, FieldWithButtons, StrictButton
from django.forms import ModelForm, Textarea


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


class ContactForm(forms.Form):
    # full_name = forms.CharField(required=False)
    # email = forms.EmailField()
    # message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):

        #pop will remove the keyword that has been stored inside the kwargs after extracting it.
        loggedin = kwargs.pop('loggedin', None)

        super(ContactForm, self).__init__(*args, **kwargs)

        if loggedin:
            #kwargs has confirm that user has logged in therefore we dont need full name and email
            self.fields["message"] = forms.CharField(widget=forms.Textarea, label="Ask questions or send us your feedback here")

        else:
            # print ("not loggedin")
            self.fields["full_name"] = forms.CharField(required=True)
            self.fields["email"] = forms.EmailField()
            self.fields["message"] = forms.CharField(widget=forms.Textarea, label="Ask questions or send us your feedback here")


    # full_name = forms.CharField(
    #     # widget=forms.RadioSelect,
    #     # empty_label=None,
    #     # queryset=TypeLocation.objects.filter(active=True),
    #     # label="Location",
    #     help_text="name",
    #     required=False
    # )



class AllauthSignupForm(forms.Form):
 
    # captcha = ReCaptchaField()
 
    # def __init__(self, *args, **kwargs):
    #     super(AllauthSignupForm, self).__init__(*args, **kwargs)

    #     # original signup form includes captcha, but the problem with captcha might be that it doesnt work on mobile
    #     # captcha needs to be tested on mobile first
    #     field_order = ['username', 'email', 'password1', 'password2', 'captcha']
 
    #     field_order = ['username', 'email', 'password1', 'password2', 'captcha']
    #     self.order_fields(field_order)
 
    # def signup(self, request, user):
    #     """ Required, or else it throws deprecation warnings """
    #     pass





    #without recapture
 
    def __init__(self, *args, **kwargs):
        super(AllauthSignupForm, self).__init__(*args, **kwargs)

        # original signup form includes captcha, but the problem with captcha might be that it doesnt work on mobile
        # captcha needs to be tested on mobile first
        field_order = ['username', 'email', 'password1', 'password2']
 
        field_order = ['username', 'email', 'password1', 'password2']
        self.order_fields(field_order)
 
    def signup(self, request, user):
        """ Required, or else it throws deprecation warnings """
        pass

