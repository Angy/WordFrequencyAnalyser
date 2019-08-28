from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.forms import HiddenInput, RadioSelect


def validate_file_extension(value):
    valid_extensions = ['.txt', '.doc', '.docx']

    if not value.name.endswith(tuple(valid_extensions)):
        raise ValidationError(u'Invalid File format')


choices = (('all', 'all'),
            ('word', 'words'))


class FrequencyAnalyserForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension],label='')
    word = forms.CharField(required=False,
                           widget=forms.TextInput(
                               attrs={'placeholder': 'the, hill, on'}
                           ),
                           help_text='Leave blank to view all '
                                     'the occurances')
    frequency = forms.IntegerField(required=False, help_text='Leave blank to '
                                                             'view the most '
                                                             'frequent '
                                                             'occurance')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Analyse',
                                     css_class='btn-primary'))
        self.helper.form_class = 'form-horizontal'

        self.helper.form_method = 'POST'
