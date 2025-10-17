"""
Script to populate the database with initial cities and services,
and create the city-service relationships.

Run this script after creating and applying migrations:

python manage.py shell < scripts/create_cities_and_services.py
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tailwind_site.settings')
django.setup()

from django.utils.text import slugify
from core.models import City, Service, CityService


def create_cities():
    """Create initial set of cities"""
    cities = [
        {'name': 'Delhi', 'state': 'Delhi'},
        {'name': 'Mumbai', 'state': 'Maharashtra'},
        {'name': 'Bangalore', 'state': 'Karnataka'},
        {'name': 'Hyderabad', 'state': 'Telangana'},
        {'name': 'Chennai', 'state': 'Tamil Nadu'},
        {'name': 'Kolkata', 'state': 'West Bengal'},
        {'name': 'Pune', 'state': 'Maharashtra'},
        {'name': 'Ahmedabad', 'state': 'Gujarat'},
        {'name': 'Jaipur', 'state': 'Rajasthan'},
        {'name': 'Gurgaon', 'state': 'Haryana'},
        {'name': 'Noida', 'state': 'Uttar Pradesh'},
    ]
    
    for city_data in cities:
        city, created = City.objects.get_or_create(
            name=city_data['name'],
            defaults={
                'slug': slugify(city_data['name']),
                'state': city_data['state'],
                'is_active': True
            }
        )
        
        if created:
            print(f"Created city: {city.name}")
        else:
            print(f"City already exists: {city.name}")


def create_services():
    """Create initial set of services"""
    services = [
        {
            'title': 'Software Development',
            'slug': 'software-development',
            'short_description': 'Custom software solutions designed to meet your unique business requirements.',
            'long_description': 'Our expert team of developers creates tailored software solutions that address your specific business challenges. We follow industry best practices and use cutting-edge technologies to deliver high-quality, scalable, and maintainable software that drives business growth and efficiency.',
            'icon_path': 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4',
            'features': [
                'Custom Application Development',
                'Enterprise Software Solutions',
                'Mobile App Development',
                'Legacy System Modernization',
                'Web Application Development',
                'Cross-Platform Solutions'
            ],
            'benefits': [
                'Increased operational efficiency',
                'Reduced costs and improved ROI',
                'Enhanced customer experience',
                'Competitive advantage in your market',
                'Scalable solutions that grow with your business'
            ],
            'process': [
                'Requirements Analysis',
                'Design & Planning',
                'Development',
                'Testing & QA',
                'Deployment',
                'Maintenance & Support'
            ],
            'display_order': 1
        },
        {
            'title': 'Website Development',
            'slug': 'website-development',
            'short_description': 'Professional websites that attract visitors, engage users, and convert leads.',
            'long_description': 'We create stunning, responsive websites that not only look great but also perform exceptionally well. Our web development team combines attractive design with optimized functionality to ensure your site delivers an outstanding user experience across all devices while achieving your business objectives.',
            'icon_path': 'M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4',
            'features': [
                'Responsive Web Design',
                'E-commerce Websites',
                'Content Management Systems',
                'Landing Pages',
                'Progressive Web Apps',
                'Website Redesign & Optimization'
            ],
            'benefits': [
                'Professional brand representation',
                'Mobile-friendly user experience',
                'Improved conversion rates',
                'SEO optimization',
                'Easy content management'
            ],
            'process': [
                'Discovery & Planning',
                'Wireframing & Design',
                'Development',
                'Content Integration',
                'Testing & Launch',
                'Maintenance & Support'
            ],
            'display_order': 2
        },
        {
            'title': 'CRM Solutions',
            'slug': 'crm-solutions',
            'short_description': 'Streamline customer relationships and boost sales with our powerful CRM systems.',
            'long_description': 'Our Customer Relationship Management solutions help you manage interactions with current and potential customers. We provide robust CRM systems that centralize customer data, automate sales processes, and provide valuable insights to improve customer relationships and increase revenue.',
            'icon_path': 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
            'features': [
                'Lead Management',
                'Sales Automation',
                'Contact Management',
                'Pipeline Management',
                'Analytics and Reporting',
                'Customer Support Integration'
            ],
            'benefits': [
                'Improved lead conversion rates',
                'Enhanced customer retention',
                'Streamlined sales processes',
                'Data-driven decision making',
                'Increased team collaboration'
            ],
            'process': [
                'Needs Assessment',
                'Solution Design',
                'Implementation',
                'Data Migration',
                'Training',
                'Ongoing Support'
            ],
            'display_order': 3
        },
        {
            'title': 'HRMS Solutions',
            'slug': 'hrms-solutions',
            'short_description': 'Optimize your HR processes with our comprehensive human resource management systems.',
            'long_description': 'Our Human Resource Management Systems streamline and automate HR functions from recruitment to retirement. We provide integrated solutions that handle employee data management, payroll processing, benefits administration, performance tracking, and more, allowing your HR team to focus on strategic initiatives.',
            'icon_path': 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
            'features': [
                'Employee Data Management',
                'Payroll Processing',
                'Attendance & Leave Management',
                'Performance Management',
                'Recruitment & Onboarding',
                'Training & Development'
            ],
            'benefits': [
                'Streamlined HR operations',
                'Reduced administrative overhead',
                'Improved employee experience',
                'Better data security',
                'Enhanced compliance'
            ],
            'process': [
                'Requirements Analysis',
                'System Configuration',
                'Implementation',
                'Data Migration',
                'User Training',
                'Support & Maintenance'
            ],
            'display_order': 4
        },
        {
            'title': 'Autodialer Solutions',
            'slug': 'autodialer-solutions',
            'short_description': 'Enhance your outbound call operations with our advanced autodialer systems.',
            'long_description': 'Our Autodialer Solutions automate outbound calling for sales, marketing, customer service, and debt collection. We provide sophisticated dialing systems with features like predictive dialing, call scripting, and analytics to maximize agent productivity and improve campaign results.',
            'icon_path': 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 01.991-.416l2.354.49a1 1 0 01.818.983V18a2 2 0 01-2 2h-1.162a2 2 0 01-1.962-1.608l-.265-1.326c-.727.224-1.494.39-2.29.471a2 2 0 01-2.191-1.45l-1.604-6.5',
            'features': [
                'Predictive Dialing',
                'Call Scripting',
                'Campaign Management',
                'CRM Integration',
                'Call Recording',
                'Real-time Analytics'
            ],
            'benefits': [
                'Increased agent productivity',
                'Improved contact rates',
                'Enhanced campaign performance',
                'Better lead qualification',
                'Data-driven decision making'
            ],
            'process': [
                'Requirements Analysis',
                'Solution Design',
                'Implementation',
                'Integration',
                'Training',
                'Support & Optimization'
            ],
            'display_order': 5
        }
    ]
    
    for service_data in services:
        service, created = Service.objects.get_or_create(
            slug=service_data['slug'],
            defaults={
                'title': service_data['title'],
                'short_description': service_data['short_description'],
                'long_description': service_data['long_description'],
                'icon_path': service_data['icon_path'],
                'features': service_data['features'],
                'benefits': service_data['benefits'],
                'process': service_data['process'],
                'display_order': service_data['display_order'],
                'is_active': True
            }
        )
        
        if created:
            print(f"Created service: {service.title}")
        else:
            print(f"Service already exists: {service.title}")
            # Update existing service with new data
            for key, value in service_data.items():
                if key != 'slug':
                    setattr(service, key, value)
            service.save()
            print(f"Updated service: {service.title}")


def create_city_services():
    """Create relationships between cities and services"""
    cities = City.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)
    
    # Create city-service relationships for all combinations
    for city in cities:
        for service in services:
            city_service, created = CityService.objects.get_or_create(
                city=city,
                service=service,
                defaults={
                    'is_active': True,
                    'custom_content': f"Get professional {service.title} services in {city.name}. Our local team provides expert solutions tailored to businesses in {city.name} and surrounding areas."
                }
            )
            
            if created:
                print(f"Created city-service: {service.title} in {city.name}")
            else:
                print(f"City-service already exists: {service.title} in {city.name}")


if __name__ == "__main__":
    print("Starting to populate database...")
    create_cities()
    create_services()
    create_city_services()
    print("Database population complete!")