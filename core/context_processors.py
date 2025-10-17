"""
Context processors for adding common data to all templates
"""
from .models import City, Service


def common_data(request):
    """
    Context processor to add commonly used data to all templates
    """
    # Get all active cities
    all_cities = City.objects.filter(is_active=True).order_by('name')
    
    # Get all active services
    all_services = Service.objects.filter(is_active=True).order_by('display_order')
    
    # Get current city if in path
    current_city = None
    
    # Check if a city slug is in the URL path
    path_parts = request.path.strip('/').split('/')
    if path_parts:
        # Check for city in first part of URL (/<city_slug>/)
        if len(path_parts) >= 1:
            potential_city_slug = path_parts[0]
            try:
                current_city = City.objects.get(slug=potential_city_slug, is_active=True)
            except City.DoesNotExist:
                pass
        
        # Check for city in city-service URL (/<service_slug>-services-in-<city_slug>/)
        if not current_city and len(path_parts) == 1 and '-services-in-' in path_parts[0]:
            parts = path_parts[0].split('-services-in-')
            if len(parts) == 2:
                city_slug = parts[1]
                try:
                    current_city = City.objects.get(slug=city_slug, is_active=True)
                except City.DoesNotExist:
                    pass
    
    # Get detected city based on IP (if implemented)
    detected_city = request.session.get('detected_city', None)
    
    return {
        'all_cities': all_cities,
        'all_services': all_services,
        'current_city': current_city,
        'detected_city': detected_city,
    }