from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import *

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Your Search")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']

class WikiForm(forms.Form):
    text = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'style': 'width:40%'}))

class ConversionForm(forms.Form):
    CHOICES = [('temperature', 'Temperature'), ('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionTempForm(forms.Form):
    CHOICES = [('celsius', 'Celsius'), ('fahrenheit', 'Fahrenheit'), ('kelvin', 'Kelvin')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter the Number'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot'), ('meter', 'Meter')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter the Number'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter the Number'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

