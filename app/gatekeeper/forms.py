from django import forms
from django.contrib.auth.models import User

from gatekeeper.mail import send_moderation_notices
from gatekeeper.models import UserProfile


attrs_dict = { 'class': 'required span4' }
req_attrs_dict = { 'class': 'required span4' }

class UserProfileForm(forms.Form):
    """
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs=req_attrs_dict), label='First name')
    last_name = forms.CharField(widget=forms.TextInput(attrs=req_attrs_dict), label='Last name')
    location = forms.CharField(widget=forms.TextInput(attrs=req_attrs_dict), 
                                label='Location (city, country)')
    profession = forms.CharField(widget=forms.TextInput(attrs=req_attrs_dict), 
                                label='Profession')
    focus = forms.CharField(widget=forms.TextInput(attrs=attrs_dict), 
                            required=False, 
                            label='Focus', )
    blog_url = forms.URLField(widget=forms.TextInput(attrs=attrs_dict), 
                                required=False, 
                                label='Blog URL',
                                initial='http://',
                                help_text='The URL of your blog, complete with leading protocol')
    twitter_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict), 
                                    required=False, 
                                    label='Twitter account',
                                    help_text='Your twitter account name without the leading @')
    notify_recent_changes = forms.BooleanField(required=False,
                                                label='Wiki mail notifications',
                                                help_text='Get notified of wiki changes by email')

    def clean_twitter_name(self):
        """
        Strip leading @-signs from the the field
        """
        if 'twitter_name' in self.cleaned_data:
            return self.cleaned_data['twitter_name'].strip('@')


class GatekeeperRegistrationForm(UserProfileForm):
    """
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(req_attrs_dict, maxlength=75)),
                             label='Email address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=req_attrs_dict, render_value=False),
                                label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=req_attrs_dict, render_value=False),
                                label='Password (again)')
    
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError('You must type the same password each time')
        return self.cleaned_data

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return self.cleaned_data['email']