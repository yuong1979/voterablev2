from django import forms
from users.models import PUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios, FieldWithButtons, StrictButton





class TagSearchForm(forms.Form):
    search = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):

        super(TagSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        # self.helper.layout = Layout(
        # 
        #     Fieldset(
        #         '',
        #         FieldWithButtons('search', Submit('submit', value='Search', css_class='btn-primary', style='font-weight: bold;'))
        #     ),
        # )
    
    search = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Search', 
            'autocomplete':'off'
            }),


    )



class TagPollSearchForm(forms.Form):
    search = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):

        super(TagPollSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        # self.helper.layout = Layout(
        # 
        #     Fieldset(
        #         '',
        #         FieldWithButtons('search', Submit('submit', value='Search', css_class='btn-primary', style='font-weight: bold;'))
        #     ),
        # )
    
    search = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Tips', 
            'autocomplete':'off'
            })
    )