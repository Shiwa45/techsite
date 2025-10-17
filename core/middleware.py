"""
Middleware for city detection based on visitor IP address
"""
import requests
from django.conf import settings
from .models import City


class CityDetectionMiddleware:
    """
    Middleware to detect user's city based on their IP address.
    This is optional functionality that can be enabled/disabled
    via settings.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialize once, used for all requests
        self.enabled = getattr(settings, 'ENABLE_CITY_DETECTION', False)
        self.geolocation_api_url = getattr(
            settings, 
            'GEOLOCATION_API_URL', 
            'http://ip-api.com/json/'
        )

    def __call__(self, request):
        # Skip city detection if disabled or user already has a city in session
        if not self.enabled or 'detected_city' in request.session:
            return self.get_response(request)
        
        # Try to detect city based on IP
        try:
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Skip for local IPs during development
            if ip in ('127.0.0.1', 'localhost', '::1'):
                return self.get_response(request)
            
            # Make API request to get location info
            response = requests.get(f"{self.geolocation_api_url}{ip}", timeout=2)
            location_data = response.json()
            
            # If we have a valid city, try to match it to our cities
            if response.status_code == 200 and location_data.get('status') == 'success':
                city_name = location_data.get('city')
                if city_name:
                    # Try to find closest matching city in our database
                    try:
                        city = City.objects.get(name__iexact=city_name, is_active=True)
                        # Store just the slug in session
                        request.session['detected_city'] = city.slug
                    except City.DoesNotExist:
                        # If exact match not found, could implement fuzzy matching here
                        pass
        except Exception:
            # Silently fail if city detection doesn't work
            # We don't want this to break the site
            pass
        
        return self.get_response(request)