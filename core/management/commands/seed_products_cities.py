# core/management/commands/seed_products_cities.py

from django.core.management.base import BaseCommand
from core.models import City, Product, ProductFeature, ProductCity
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with cities and products'

    def handle(self, *args, **options):
        # Create cities
        cities_data = [
            {'name': 'Delhi'},
            {'name': 'Gurgaon'},
            {'name': 'Hyderabad'},
            {'name': 'Mumbai'},
            {'name': 'Noida'},
            {'name': 'Bangalore'},
            {'name': 'Pune'},
            {'name': 'Chennai'}
        ]
        
        cities_created = 0
        for city_data in cities_data:
            city, created = City.objects.get_or_create(
                name=city_data['name'],
                defaults={
                    'slug': slugify(city_data['name']),
                    'is_active': True
                }
            )
            if created:
                cities_created += 1
                self.stdout.write(f"Created city: {city.name}")
        
        # Create products
        products_data = [
            {
                'name': 'Software Development',
                'short_description': 'Custom software solutions designed to meet your unique business requirements.',
                'icon_path': 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'
            },
            {
                'name': 'Website Development',
                'short_description': 'Professional websites built with cutting-edge technology for maximum impact.',
                'icon_path': 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9'
            },
            {
                'name': 'CRM Solutions',
                'short_description': 'Streamline customer relationships and boost sales with our powerful CRM systems.',
                'icon_path': 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z'
            },
            {
                'name': 'HRMS Solutions',
                'short_description': 'Optimize your HR processes with our comprehensive human resource management systems.',
                'icon_path': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01'
            },
            {
                'name': 'Autodialer Solutions',
                'short_description': 'Enhance your call center productivity with our advanced autodialer technology.',
                'icon_path': 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z'
            }
        ]
        
        products_created = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': slugify(product_data['name']),
                    'short_description': product_data['short_description'],
                    'icon_path': product_data['icon_path'],
                    'is_active': True
                }
            )
            if created:
                products_created += 1
                self.stdout.write(f"Created product: {product.name}")
        
        # Create sample features for each product
        features_data = {
            'Software Development': [
                {'title': 'Custom Applications', 'description': 'Bespoke software tailored to your unique business needs'},
                {'title': 'Enterprise Solutions', 'description': 'Scalable systems designed for large organizations'},
                {'title': 'Mobile Apps', 'description': 'Native and cross-platform mobile applications'},
                {'title': 'Legacy Modernization', 'description': 'Updating older systems with modern technologies'}
            ],
            'Website Development': [
                {'title': 'Responsive Design', 'description': 'Websites that work perfectly on all devices'},
                {'title': 'E-commerce', 'description': 'Online stores with secure payment processing'},
                {'title': 'CMS Integration', 'description': 'Easy content management systems'},
                {'title': 'SEO Optimization', 'description': 'Built-in search engine optimization'}
            ],
            'CRM Solutions': [
                {'title': 'Lead Management', 'description': 'Track and nurture potential customers'},
                {'title': 'Sales Automation', 'description': 'Streamline your sales process'},
                {'title': 'Customer Support', 'description': 'Integrated ticketing and support systems'},
                {'title': 'Analytics', 'description': 'Insights into your customer relationships'}
            ],
            'HRMS Solutions': [
                {'title': 'Employee Management', 'description': 'Comprehensive employee data management'},
                {'title': 'Payroll Automation', 'description': 'Streamlined payroll processing'},
                {'title': 'Performance Tracking', 'description': 'Monitor and improve employee performance'},
                {'title': 'Recruitment', 'description': 'Simplified hiring and onboarding'}
            ],
            'Autodialer Solutions': [
                {'title': 'Predictive Dialing', 'description': 'Intelligent call routing and management'},
                {'title': 'Call Analytics', 'description': 'Detailed reporting on call performance'},
                {'title': 'CRM Integration', 'description': 'Seamless connection with your customer data'},
                {'title': 'Compliance Tools', 'description': 'Stay within regulatory guidelines'}
            ]
        }
        
        features_created = 0
        for product_name, features in features_data.items():
            try:
                product = Product.objects.get(name=product_name)
                
                for i, feature_data in enumerate(features):
                    feature, created = ProductFeature.objects.get_or_create(
                        product=product,
                        title=feature_data['title'],
                        defaults={
                            'description': feature_data['description'],
                            'order': i
                        }
                    )
                    if created:
                        features_created += 1
                        self.stdout.write(f"Created feature: {feature.title} for {product.name}")
            except Product.DoesNotExist:
                continue
        
        # Create sample product-city pages
        sample_cities = City.objects.all()[:3]  # Get first 3 cities
        sample_products = Product.objects.all()[:3]  # Get first 3 products
        
        pages_created = 0
        for product in sample_products:
            for city in sample_cities:
                slug = f"{product.slug}_services_in_{city.slug}"
                
                product_city, created = ProductCity.objects.get_or_create(
                    product=product,
                    city=city,
                    defaults={
                        'page_title': f"{product.name} Services in {city.name} | Tech Solutions",
                        'meta_description': f"Professional {product.name} services in {city.name}. Custom solutions for your business needs with local expertise and support.",
                        'headline': f"{product.name} in {city.name}",
                        'slug': slug,
                        'intro_content': f"<p>Looking for professional {product.name} services in {city.name}? Tech Solutions provides industry-leading {product.name.lower()} solutions tailored to the unique needs of {city.name} businesses.</p><p>Our local team has extensive experience working with companies across various industries in the {city.name} region.</p>",
                        'main_content': f"<h2>Why Choose Our {product.name} Services in {city.name}</h2><p>Tech Solutions has been delivering exceptional {product.name.lower()} services to businesses in {city.name} for over 8 years. Our deep understanding of the local business landscape allows us to create solutions that perfectly align with your requirements.</p><h3>Our {city.name} {product.name} Process</h3><p>We follow a proven methodology to deliver high-quality {product.name.lower()} solutions:</p><ol><li><strong>Discovery:</strong> We learn about your business goals and challenges</li><li><strong>Planning:</strong> We create a detailed roadmap for your solution</li><li><strong>Development:</strong> Our expert team builds your custom solution</li><li><strong>Testing:</strong> Rigorous quality assurance ensures perfection</li><li><strong>Deployment:</strong> Smooth implementation with minimal disruption</li><li><strong>Support:</strong> Ongoing assistance and maintenance</li></ol>",
                        'city_specific_content': f"<h4>Why {city.name} Businesses Choose Us</h4><ul><li>Local expertise and understanding of the {city.name} market</li><li>Rapid response times with on-site support</li><li>Customized solutions for {city.name} business requirements</li><li>Competitive pricing for the {city.name} region</li></ul>",
                        'is_active': True
                    }
                )
                if created:
                    pages_created += 1
                    self.stdout.write(f"Created page: {product.name} in {city.name}")
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {cities_created} cities, {products_created} products, ' +
            f'{features_created} features, and {pages_created} product-city pages'
        ))