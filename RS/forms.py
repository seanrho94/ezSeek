from .models import Post
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from crispy_forms.bootstrap import FieldWithButtons

class JobSearchForm(forms.Form):
    search_text =  forms.CharField(
                    required = False,
                    label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Search job...'})
                  )

    def __init__(self, *args, **kwargs):
        super(JobSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'

        self.helper.layout = Layout(
                    FieldWithButtons('search_text', ButtonHolder(Submit('submit', 'Search', css_class='btn btn-info')))

        )
