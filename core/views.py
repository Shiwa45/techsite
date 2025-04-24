from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lead, NewsletterSubscriber, ResourceDownload
from .forms import ContactForm, NewsletterForm, CourseInquiryForm
from .models import BlogPost, BlogCategory
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    """
    View for the homepage with the cyber-themed hero section
    """
    # Handle newsletter subscription form on homepage
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
        
    context = {
        'page_title': 'Easyian - Innovative Technology Services',
        'meta_description': 'Leading provider of technology solutions including software development, CRM, HRMS, VOIP, API, and more.',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'home.html', context)

def services(request):
    """
    View for the services page
    """
    # Services data - in a real application, this might come from a database
    services_list = [
        {
            'title': 'Software Development',
            'icon': 'code',
            'description': 'Custom software solutions designed to meet your unique business requirements.',
            'features': [
                'Custom applications',
                'Enterprise software',
                'Mobile applications',
                'Legacy system modernization',
            ]
        },
        {
            'title': 'CRM Solutions',
            'icon': 'users',
            'description': 'Streamline customer relationships and boost sales with our powerful CRM systems.',
            'features': [
                'Lead management',
                'Sales automation',
                'Customer support integration',
                'Analytics and reporting',
            ]
        },
        {
            'title': 'HRMS Solutions',
            'icon': 'clipboard',
            'description': 'Optimize your HR processes with our comprehensive human resource management systems.',
            'features': [
                'Employee management',
                'Payroll automation',
                'Performance tracking',
                'Recruitment and onboarding',
            ]
        },
        {
            'title': 'VOIP Services',
            'icon': 'phone',
            'description': 'Advanced voice communication solutions for your business needs.',
            'features': [
                'Cloud PBX systems',
                'SIP trunking',
                'Call center solutions',
                'Unified communications',
            ]
        },
        {
            'title': 'API Development',
            'icon': 'code-bracket',
            'description': 'Connect your systems and applications with custom API solutions.',
            'features': [
                'RESTful API design',
                'API integration',
                'Third-party API connections',
                'API documentation',
            ]
        },
        {
            'title': 'Autodialer Solutions',
            'icon': 'phone-arrow-up-right',
            'description': 'Enhance your outbound call operations with our advanced autodialer systems.',
            'features': [
                'Predictive dialing',
                'IVR integration',
                'Call analytics',
                'Campaign management',
            ]
        },
    ]
    
    # Handle newsletter subscription form on services page
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('services')
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': 'Our Services - Easyian',
        'meta_description': 'Explore our wide range of technology services including software development, CRM, HRMS, and more.',
        'services': services_list,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'services/services.html', context)

def service_detail(request, service_slug):
    """
    View for individual service details
    """
    # In a real application, you would fetch the service from a database
    # Here we're using a dictionary for demonstration
    services_dict = {
        'software-development': {
            'title': 'Software Development',
            'description': 'Custom software solutions designed to meet your unique business requirements.',
            'long_description': 'Our team of experienced developers creates tailored software solutions that address your specific business challenges. We follow industry best practices and use cutting-edge technologies to deliver high-quality, scalable, and maintainable software.',
            'icon': 'code',
            'features': [
                'Custom applications',
                'Enterprise software',
                'Mobile applications',
                'Legacy system modernization',
            ],
            'benefits': [
                'Increased operational efficiency',
                'Reduced costs',
                'Improved customer satisfaction',
                'Competitive advantage',
            ],
            'process': [
                'Requirements gathering',
                'Design and planning',
                'Development',
                'Testing',
                'Deployment',
                'Maintenance and support',
            ]
        },
        # Add more services as needed
    }
    
    service = services_dict.get(service_slug)
    if not service:
        # Handle case when service doesn't exist
        return redirect('services')
    
    # Handle newsletter subscription form
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('service_detail', service_slug=service_slug)
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': f"{service['title']} - Easyian",
        'meta_description': service['description'],
        'service': service,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'services/service_detail.html', context)

def courses(request):
    """
    View for the courses page
    """
    # Courses data - in a real application, this might come from a database
    courses_list = [
        {
            'title': 'Digital Marketing Mastery',
            'duration': '12 Weeks',
            'description': 'Comprehensive training in SEO, SEM, social media marketing, content creation, and analytics to drive business growth.',
            'completion_rate': 92,
            'tags': ['SEO', 'Google Ads', 'Social Media', 'Analytics'],
            'price': 599,
            'popular': True,
        },
        {
            'title': 'Full Stack Development',
            'duration': '16 Weeks',
            'description': 'Master both front-end and back-end technologies to build complete web applications from scratch.',
            'completion_rate': 88,
            'tags': ['HTML/CSS', 'JavaScript', 'React', 'Python', 'Django'],
            'price': 899,
            'popular': False,
        },
        {
            'title': 'Data Science & Analytics',
            'duration': '14 Weeks',
            'description': 'Learn to analyze and interpret complex data sets to drive business decisions using cutting-edge tools and techniques.',
            'completion_rate': 85,
            'tags': ['Python', 'SQL', 'Machine Learning', 'Tableau'],
            'price': 799,
            'new': True,
        },
        {
            'title': 'UI/UX Design Fundamentals',
            'duration': '10 Weeks',
            'description': 'Learn the principles of user-centered design to create intuitive, engaging, and visually appealing digital experiences.',
            'completion_rate': 94,
            'tags': ['Figma', 'Adobe XD', 'User Research', 'Prototyping'],
            'price': 649,
            'popular': False,
        },
        {
            'title': 'Cybersecurity Essentials',
            'duration': '12 Weeks',
            'description': 'Develop the skills to protect organizations from cyber threats, vulnerabilities, and attacks in today\'s digital landscape.',
            'completion_rate': 90,
            'tags': ['Network Security', 'Ethical Hacking', 'Risk Assessment', 'Incident Response'],
            'price': 749,
            'popular': False,
        },
        {
            'title': 'Cloud Computing & DevOps',
            'duration': '14 Weeks',
            'description': 'Learn to design, deploy, and manage cloud infrastructure and implement DevOps practices for continuous integration and delivery.',
            'completion_rate': 87,
            'tags': ['AWS', 'Docker', 'Kubernetes', 'CI/CD'],
            'price': 849,
            'high_demand': True,
        },
    ]
    
    # Handle course inquiry form
    if request.method == 'POST':
        if 'course_inquiry' in request.POST:
            inquiry_form = CourseInquiryForm(request.POST)
            if inquiry_form.is_valid():
                inquiry = inquiry_form.save(commit=False)
                inquiry.source = 'course_inquiry'
                inquiry.interest = request.POST.get('course_name', 'course_inquiry')
                inquiry.save()
                messages.success(request, "Thank you for your interest! We'll contact you soon with more information.")
                return redirect('courses')
        elif 'newsletter_email' in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                newsletter_form.save()
                messages.success(request, "Thank you for subscribing to our newsletter!")
                return redirect('courses')
    
    inquiry_form = CourseInquiryForm()
    newsletter_form = NewsletterForm()
    
    context = {
        'page_title': 'Our Courses - Easyian',
        'meta_description': 'Browse our training courses in Digital Marketing, Full Stack Development, and more.',
        'courses': courses_list,
        'inquiry_form': inquiry_form,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'courses/courses.html', context)

def course_detail(request, course_slug):
    """
    View for individual course details
    """
    # In a real application, you would fetch the course from a database
    # Here we're using a dictionary for demonstration
    courses_dict = {
        'digital-marketing-mastery': {
            'title': 'Digital Marketing Mastery',
            'duration': '12 Weeks',
            'description': 'Comprehensive training in SEO, SEM, social media marketing, content creation, and analytics to drive business growth.',
            'long_description': 'Our Digital Marketing Mastery course provides you with in-depth knowledge and practical skills to excel in the dynamic world of digital marketing. From search engine optimization to social media strategy, you\'ll learn how to create and execute successful digital marketing campaigns.',
            'completion_rate': 92,
            'tags': ['SEO', 'Google Ads', 'Social Media', 'Analytics'],
            'price': 599,
            'popular': True,
            'modules': [
                'Introduction to Digital Marketing',
                'Search Engine Optimization (SEO)',
                'Search Engine Marketing (SEM)',
                'Social Media Marketing',
                'Content Marketing',
                'Email Marketing',
                'Analytics and Reporting',
                'Digital Marketing Strategy',
                'Capstone Project',
            ],
            'skills': [
                'SEO optimization',
                'PPC campaign management',
                'Social media strategy',
                'Content creation',
                'Marketing analytics',
                'Conversion optimization',
            ],
            'requirements': [
                'Basic computer skills',
                'Interest in marketing',
                'No prior experience required',
            ]
        },
        # Add more courses as needed
    }
    
    course = courses_dict.get(course_slug)
    if not course:
        # Handle case when course doesn't exist
        return redirect('courses')
    
    # Handle forms
    if request.method == 'POST':
        if 'course_inquiry' in request.POST:
            inquiry_form = CourseInquiryForm(request.POST)
            if inquiry_form.is_valid():
                inquiry = inquiry_form.save(commit=False)
                inquiry.source = 'course_detail'
                inquiry.interest = course['title']
                inquiry.save()
                messages.success(request, "Thank you for your interest! We'll contact you soon with more information.")
                return redirect('course_detail', course_slug=course_slug)
        elif 'newsletter_email' in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                newsletter_form.save()
                messages.success(request, "Thank you for subscribing to our newsletter!")
                return redirect('course_detail', course_slug=course_slug)
    
    inquiry_form = CourseInquiryForm()
    newsletter_form = NewsletterForm()
    
    context = {
        'page_title': f"{course['title']} - Easyian",
        'meta_description': course['description'],
        'course': course,
        'inquiry_form': inquiry_form,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'courses/course_detail.html', context)

def about(request):
    """
    View for the about page
    """
    # Team members data - in a real application, this might come from a database
    team_members = [
        {
            'name': 'John Smith',
            'position': 'CEO & Founder',
            'bio': 'With over 15 years of experience in technology leadership, John has driven innovation across multiple industries.',
            'image': 'team/john-smith.jpg',
        },
        {
            'name': 'Sarah Johnson',
            'position': 'CTO',
            'bio': 'Sarah brings extensive expertise in software architecture and emerging technologies to lead our technical strategy.',
            'image': 'team/sarah-johnson.jpg',
        },
        {
            'name': 'Michael Chen',
            'position': 'Head of Product',
            'bio': "Michael's background in user experience and product development ensures our solutions deliver exceptional value.",
            'image': 'team/michael-chen.jpg',
        },
        {
            'name': 'Emily Rodriguez',
            'position': 'Lead Developer',
            'bio': 'Emily specializes in full-stack development and has led numerous successful projects for enterprise clients.',
            'image': 'team/emily-rodriguez.jpg',
        },
    ]
    
    # Company milestones - in a real application, this might come from a database
    milestones = [
        {
            'year': 2015,
            'title': 'Company Founded',
            'description': 'Easyian was established with a mission to deliver innovative technology solutions.',
        },
        {
            'year': 2017,
            'title': 'Expanded Service Offerings',
            'description': 'Added CRM and HRMS solutions to our portfolio of services.',
        },
        {
            'year': 2019,
            'title': 'Launched Training Academy',
            'description': 'Introduced comprehensive tech courses to help professionals advance their careers.',
        },
        {
            'year': 2021,
            'title': 'Global Expansion',
            'description': 'Opened offices in three new countries to serve international clients.',
        },
        {
            'year': 2023,
            'title': 'Industry Recognition',
            'description': 'Received multiple awards for innovation and excellence in technology services.',
        },
    ]
    
    # Handle newsletter subscription form
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('about')
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': 'About Us - Easyian',
        'meta_description': 'Learn about Easyian and our mission to deliver innovative technology solutions.',
        'team_members': team_members,
        'milestones': milestones,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'about.html', context)

def contact(request):
    """
    View for the contact page with lead generation form
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Save the lead
            lead = contact_form.save(commit=False)
            lead.source = 'contact_form'
            lead.save()
            
            # Check if user wants to subscribe to the newsletter
            if request.POST.get('newsletter', False):
                email = request.POST.get('email')
                name = request.POST.get('name')
                if not NewsletterSubscriber.objects.filter(email=email).exists():
                    NewsletterSubscriber.objects.create(
                        email=email,
                        name=name
                    )
            
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect('contact_success')
    else:
        contact_form = ContactForm()
    
    context = {
        'page_title': 'Contact Us - Easyian',
        'meta_description': 'Get in touch with Easyian for all your technology needs.',
        'form': contact_form,
    }
    
    return render(request, 'contact/contact.html', context)

def contact_success(request):
    """
    View for contact form submission confirmation
    """
    context = {
        'page_title': 'Message Sent - Easyian',
        'meta_description': 'Your message has been successfully sent to Easyian.',
    }
    
    return render(request, 'contact/contact_success.html', context)

def newsletter_signup(request):
    """
    View for handling newsletter signup submissions
    """
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            
            # Redirect back to the referring page, or home if no referrer
            referer = request.META.get('HTTP_REFERER')
            if referer:
                return redirect(referer)
            else:
                return redirect('home')
    
    # If not POST or form invalid, redirect to home
    return redirect('home')





def service_detail(request, service_slug):
    """
    View for individual service details
    """
    # Comprehensive service data dictionary
    services_dict = {
        'software-development': {
            'title': 'Software Development',
            'description': 'Custom software solutions designed to meet your unique business requirements.',
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
            ]
        },
        'crm-solutions': {
            'title': 'CRM Solutions',
            'description': 'Streamline customer relationships and boost sales with our powerful CRM systems.',
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
            ]
        },
        'hrms-solutions': {
            'title': 'HRMS Solutions',
            'description': 'Optimize your HR processes with our comprehensive human resource management systems.',
            'long_description': 'Our Human Resource Management Systems streamline and automate HR functions from recruitment to retirement. We provide integrated solutions that handle employee data management, payroll processing, benefits administration, performance tracking, and more, allowing your HR team to focus on strategic initiatives.',
            'icon_path': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01',
            'features': [
                'Employee Management',
                'Payroll Automation',
                'Time and Attendance Tracking',
                'Performance Management',
                'Recruitment and Onboarding',
                'Benefits Administration'
            ],
            'benefits': [
                'Reduced administrative workload',
                'Improved HR data accuracy',
                'Enhanced compliance management',
                'Better employee experience',
                'Streamlined HR processes'
            ],
            'process': [
                'Requirements Gathering',
                'System Configuration',
                'Data Import',
                'Process Integration',
                'User Training',
                'Go-Live & Support'
            ]
        },
        'voip-services': {
            'title': 'VoIP Services',
            'description': 'Advanced voice communication solutions for your business needs.',
            'long_description': 'Our Voice over Internet Protocol (VoIP) services provide advanced communication solutions that use internet technology to deliver voice calls, video conferencing, and messaging. We offer reliable, cost-effective VoIP systems that enhance communication while reducing costs compared to traditional phone systems.',
            'icon_path': 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z',
            'features': [
                'Cloud PBX Systems',
                'SIP Trunking',
                'Call Center Solutions',
                'Unified Communications',
                'Video Conferencing',
                'Mobile Integration'
            ],
            'benefits': [
                'Reduced communication costs',
                'Enhanced mobility and flexibility',
                'Improved call quality and reliability',
                'Scalable to grow with your business',
                'Advanced features not available with traditional phones'
            ],
            'process': [
                'Network Assessment',
                'Solution Design',
                'System Configuration',
                'Number Porting',
                'Installation & Testing',
                'Training & Support'
            ]
        },
        'api-development': {
            'title': 'API Development',
            'description': 'Connect your systems and applications with custom API solutions.',
            'long_description': 'Our API (Application Programming Interface) development services enable seamless communication between different software systems. We create custom, secure, and scalable APIs that integrate your existing systems, third-party services, and new applications, ensuring efficient data exchange and workflow automation.',
            'icon_path': 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
            'features': [
                'RESTful API Design',
                'GraphQL APIs',
                'API Integration',
                'Third-party API Connections',
                'API Documentation',
                'API Security & Authentication'
            ],
            'benefits': [
                'Seamless system integration',
                'Improved data accessibility',
                'Enhanced operational efficiency',
                'Reduced manual data entry',
                'Support for mobile and web applications'
            ],
            'process': [
                'Requirements Analysis',
                'API Design',
                'Development',
                'Testing & Security Validation',
                'Documentation',
                'Deployment & Maintenance'
            ]
        },
        'autodialer-solutions': {
            'title': 'Autodialer Solutions',
            'description': 'Enhance your outbound call operations with our advanced autodialer systems.',
            'long_description': 'Our Autodialer Solutions automate outbound calling for sales, marketing, customer service, and debt collection. We provide sophisticated dialing systems with features like predictive dialing, call scripting, and analytics to maximize agent productivity and improve campaign results.',
            'icon_path': 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z',
            'features': [
                'Predictive Dialing',
                'Preview Dialing',
                'Progressive Dialing',
                'IVR Integration',
                'Call Analytics',
                'Campaign Management'
            ],
            'benefits': [
                'Increased agent productivity',
                'Higher contact rates',
                'Improved campaign ROI',
                'Advanced reporting capabilities',
                'Reduced idle time for agents'
            ],
            'process': [
                'Needs Assessment',
                'System Configuration',
                'Campaign Setup',
                'Integration with CRM',
                'Agent Training',
                'Performance Optimization'
            ]
        }
    }
    
    # Get the service data based on the slug
    service = services_dict.get(service_slug)
    if not service:
        # Handle case when service doesn't exist
        return redirect('services')
    
    # Handle newsletter subscription form
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('service_detail', service_slug=service_slug)
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': f"{service['title']} - Easyian",
        'meta_description': service['description'],
        'service': service,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'services/service_detail.html', context)




# Add these new views
def blog_list(request):
    """
    View for the blog list page
    """
    posts = BlogPost.objects.filter(is_published=True)
    categories = BlogCategory.objects.annotate(post_count=Count('posts'))
    featured_posts = BlogPost.objects.filter(is_published=True, featured=True)[:3]
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:5]
    
    # Handle newsletter subscription form
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('blog_list')
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': 'Blog - Easyian',
        'meta_description': 'Latest insights, news, and articles on technology, software development, and digital transformation.',
        'posts': posts,
        'categories': categories,
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    """
    View for individual blog post detail
    """
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        category=post.category, 
        is_published=True
    ).exclude(id=post.id)[:3]
    
    # Get recent posts for sidebar
    recent_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id).order_by('-created_at')[:5]
    
    # Handle newsletter subscription form
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('blog_detail', slug=slug)
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': f"{post.title} - Easyian Blog",
        'meta_description': post.summary,
        'post': post,
        'related_posts': related_posts,
        'recent_posts': recent_posts,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'blog/blog_detail.html', context)

def blog_category(request, category_slug):
    """
    View for blog posts filtered by category
    """
    category = get_object_or_404(BlogCategory, slug=category_slug)
    posts = BlogPost.objects.filter(category=category, is_published=True)
    
    context = {
        'page_title': f"{category.name} - Easyian Blog",
        'meta_description': f"Articles and insights about {category.name} from Easyian.",
        'category': category,
        'posts': posts,
    }
    
    return render(request, 'blog/blog_category.html', context)

# Modify your home function to include actual blog posts
def home(request):
    """
    View for the homepage with the cyber-themed hero section
    """
    # Handle newsletter subscription form on homepage
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
    
    # Get latest blog posts for the homepage
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
        
    context = {
        'page_title': 'Easyian - Innovative Technology Services',
        'meta_description': 'Leading provider of technology solutions including software development, CRM, HRMS, VOIP, API, and more.',
        'newsletter_form': newsletter_form,
        'latest_posts': latest_posts,
    }
    return render(request, 'home.html', context)




def privacy_policy(request):
    """
    View for privacy policy page
    """
    context = {
        'page_title': 'Privacy Policy - Easyian',
        'meta_description': 'Our privacy policy outlines how we collect, use, and protect your personal information.',
    }
    return render(request, 'legal/privacy_policy.html', context)

def terms_of_service(request):
    """
    View for terms of service page
    """
    context = {
        'page_title': 'Terms of Service - Easyian',
        'meta_description': 'Our terms of service outline the rules, guidelines, and legal agreements for using our website and services.',
    }
    return render(request, 'legal/terms_of_service.html', context)