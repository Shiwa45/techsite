"""
URL Configuration for core app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('landing/', views.landing, name='landing'),
    
    # Services
    path('services/', views.services, name='services'),
    path('services/<slug:service_slug>/', views.service_detail, name='service_detail'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/category/<slug:category_slug>/', views.blog_category, name='blog_category'),
    
    # Legal pages
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    
    # Form submissions
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    
    # New city-specific URLs
    path('cities/', views.city_list, name='city_list'),
    path('<slug:city_slug>/', views.city_home, name='city_home'),
    path('<slug:city_slug>/services/', views.city_services, name='city_services'),
    path('<slug:city_slug>/contact/', views.city_contact, name='city_contact'),
    path('<slug:city_slug>/blog/', views.city_blog, name='city_blog'),
    
    # Dynamic service-in-city pages
    path('<slug:service_slug>-services-in-<slug:city_slug>/', views.city_service_detail, name='city_service_detail'),
    
    # API endpoints for frontend
    path('api/cities/', views.api_cities, name='api_cities'),
    path('api/services/', views.api_services, name='api_services'),
    path('api/city/<slug:city_slug>/services/', views.api_city_services, name='api_city_services'),
]