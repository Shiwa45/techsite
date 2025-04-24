from django import forms
from .models import Lead, NewsletterSubscriber

class ContactForm(forms.ModelForm):
    """
    Form for handling contact page submissions that generate leads
    """
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'interest', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'placeholder': ' '}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'placeholder': ' '}),
            'company': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'placeholder': ' '}),
            'interest': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus appearance-none', 'placeholder': ' '}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'rows': 5, 'placeholder': ' '}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'company': 'Company Name (Optional)',
            'interest': 'What are you interested in?',
            'message': 'Your Message',
        }
    
    # Add newsletter subscription checkbox (not in model)
    newsletter = forms.BooleanField(
        required=False, 
        label='Subscribe to our newsletter for tech insights and updates',
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-500 rounded focus:ring-blue-500 bg-gray-700'})
    )


class NewsletterForm(forms.ModelForm):
    """
    Form for newsletter subscriptions
    """
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full md:flex-1 px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'placeholder': 'Your email address'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'placeholder': 'Your name (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False


class CourseInquiryForm(forms.ModelForm):
    """
    Form for course inquiries that also generate leads
    """
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'placeholder': ' '}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'placeholder': ' '}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded cyber-input text-white form-focus placeholder-transparent', 'rows': 3, 'placeholder': ' '}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'message': 'Your Questions or Comments',
        }
    
    # Hidden field to store which course the user is inquiring about
    course_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    # Newsletter checkbox
    newsletter = forms.BooleanField(
        required=False, 
        label='Subscribe to our newsletter for course updates and tech insights',
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-500 rounded focus:ring-blue-500 bg-gray-700'})
    )