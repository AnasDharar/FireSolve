# Example: accounts/forms.py or users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm # Use Django's built-in UserCreationForm as a base if it fits your needs
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from potd import settings
import time
from django.core.cache import cache
from django.contrib.auth.models import User


class CustomUserCreationForm(DjangoUserCreationForm): 
    first_name = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.")
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    signup_secret_key = forms.CharField(
        max_length=100,
        required=True,
        help_text="Required. This is a secret key for signup verification.",
        widget=forms.HiddenInput
    )
    
    # Honeypot field - hidden field that should remain empty
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    
    # Timestamp field to prevent too-fast submissions
    form_timestamp = forms.CharField(widget=forms.HiddenInput, required=False)

    # Add the reCAPTCHA field
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, required=True, error_messages={'required': 'Please complete the reCAPTCHA.'})

    class Meta(DjangoUserCreationForm.Meta):
        model = DjangoUserCreationForm.Meta.model # Use the same model as the base form
        fields = DjangoUserCreationForm.Meta.fields + ('email','first_name','last_name','signup_secret_key','website','form_timestamp','captcha') # Add email to fields if not there

    def clean_website(self):
        """Honeypot field - should be empty"""
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError("Bot detected")
        return website
    
    def clean_form_timestamp(self):
        """Prevent too-fast form submissions"""
        timestamp = self.cleaned_data.get('form_timestamp')
        if timestamp:
            try:
                form_time = float(timestamp)
                current_time = time.time()
                time_diff = current_time - form_time
                
                # Require at least 5 seconds to fill the form
                if time_diff < 5:
                    raise forms.ValidationError("Form submitted too quickly")
                    
                # Reject forms older than 1 hour
                if time_diff > 3600:
                    raise forms.ValidationError("Form expired, please refresh")
                    
            except (ValueError, TypeError):
                raise forms.ValidationError("Invalid form timestamp")
        return timestamp
    
    def clean_email(self):
        """Check for duplicate emails"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_signup_secret_key(self):
        secret_key = self.cleaned_data.get('signup_secret_key')
        if secret_key != settings.SIGNUP_SECRET_KEY:
            raise forms.ValidationError("Invalid signup secret key")
        return secret_key
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise forms.ValidationError("Username can only contain letters and numbers.")
        if len(username) < 3 or len(username) > 20:
            raise forms.ValidationError("Username must be between 3 and 20 characters long.")
        return username