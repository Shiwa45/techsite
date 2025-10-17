from django import forms
from .models import Lead, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    """
    Form for contact form submissions
    """
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'interest', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Your Name*'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Email Address*'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Phone Number (optional)'}),
            'company': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Company Name (optional)'}),
            'interest': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 4, 'placeholder': 'How can we help you?*'}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'company': 'Company Name',
            'interest': 'I am interested in',
            'message': 'Message',
        }
        error_messages = {
            'name': {
                'required': 'Please enter your name',
            },
            'email': {
                'required': 'Please enter your email address',
                'invalid': 'Please enter a valid email address',
            },
            'message': {
                'required': 'Please enter a message',
            }
        }


class NewsletterForm(forms.ModelForm):
    """
    Form for newsletter subscriptions
    """
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Email Address*'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Your Name (optional)'}),
        }
        labels = {
            'email': 'Email Address',
            'name': 'Your Name',
        }
        error_messages = {
            'email': {
                'required': 'Please enter your email address',
                'invalid': 'Please enter a valid email address',
                'unique': 'This email is already subscribed to our newsletter',
            }
        }


class CityServiceContactForm(forms.ModelForm):
    """
    Form for contact from city-service pages
    """
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Your Name*'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Email Address*'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Phone Number (optional)'}),
            'company': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Company Name (optional)'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 4, 'placeholder': 'How can we help you?*'}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'company': 'Company Name',
            'message': 'Message',
        }