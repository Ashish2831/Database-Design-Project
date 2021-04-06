from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext as _
from .models import *

class Registration_Form(UserCreationForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class' : 'form-control'}), required=False)
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput(attrs={'class' : 'form-control'}), required=False)

    def __init__(self, *args, **kwargs):
        super(Registration_Form, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields.get('username').required = False

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        labels = {
            'first_name' : _('First Name'),
            'last_name' : _('Last Name'),
            'email' : _('Email'),
        }

        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control'}),
            'first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
        }

        help_texts = {
            'username' : ''
        }

    def clean_username(self):
        inp_username = self.cleaned_data.get('username')
        if len(inp_username.strip()) == 0:
            raise ValidationError(_("Please Enter The Username!!"))
        return inp_username

    def clean_first_name(self):
        inp_first_name = self.cleaned_data.get('first_name')
        if len(inp_first_name.strip()) == 0:
            raise ValidationError(_("Please Enter Your First Name!!"))
        return inp_first_name

    def clean_last_name(self):
        inp_last_name = self.cleaned_data.get('last_name')
        if len(inp_last_name.strip()) == 0:
            raise ValidationError(_("Please Enter Your Last Name!!"))
        return inp_last_name

    def clean_email(self):
        inp_email = self.cleaned_data.get('email')
        validator = EmailValidator(_("Please Provide Valid Email!!"))
        validator(inp_email)
        if User.objects.filter(email = inp_email).exists():
            raise ValidationError(_(f"{inp_email} is Already Exists!!"))
        return inp_email

    def clean_password1(self):
        inp_password1 = self.cleaned_data.get('password1')
        if len(inp_password1) == 0:
            raise ValidationError(_("Please Enter The Password!!"))
        return inp_password1

    def clean_password2(self):
        inp_password2 = self.cleaned_data.get('password2')
        inp_password1 = self.data.get('password1')
        if len(inp_password2) == 0:
            raise ValidationError(_("Please Confirm Your Password!!"))
        if inp_password1 != inp_password2:
            raise ValidationError(_("Password Must Matched!!"))
        return inp_password2

class Order_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Order_Form, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields.get(field).required = False
        self.label_suffix = False

    class Meta:
        model = Order
        fields = ['contact_person', 'contact_number', 'email', 'quantity', 'shipping_address', 'date']

        widgets = {
            'quantity' : forms.TextInput(attrs={'class' : 'form-control input-number', 'value' : '1', 'min' : '1', 'max' : '50'}),
            'shipping_address' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : '5'}),
            'contact_person' : forms.TextInput(attrs={'class' : 'form-control'}),
            'contact_number' : forms.TextInput(attrs={'class' : 'form-control'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
            'date' : forms.DateInput(attrs={'class' : 'form-control'}),
        }

        help_texts = {
            'date' : 'MM/DD/YYYY'
        }

    def clean_contact_person(self):
        input_contact_person = self.cleaned_data['contact_person']
        if len(input_contact_person.strip()) == 0:
            raise ValidationError(_("Please Enter Name of Contact Person!!"))
        return input_contact_person

    def clean_contact_number(self):
        input_contact_number = self.cleaned_data['contact_number']
        if len(input_contact_number.strip()) == 0:
            raise ValidationError(_("Please Enter Contact Number!!"))
        if input_contact_number == None or len(input_contact_number) != 10:
            raise ValidationError(_("Please Enter Valid Contact Number!!"))
        return input_contact_number

    def clean_email(self):
        input_email = self.cleaned_data['email']
        validate = EmailValidator(_("Please Enter Valid Email"))
        validate(input_email)
        return input_email

    def clean_shipping_address(self):
        input_shipping_address = self.cleaned_data['shipping_address']
        if len(input_shipping_address.strip()) == 0:
            raise ValidationError(_("Please Enter Shipping Address!!"))
        return input_shipping_address

    def clean_date(self):
        input_date = self.cleaned_data['date']
        if input_date == None:
            raise ValidationError(_("Please Enter Date!!"))
        return input_date