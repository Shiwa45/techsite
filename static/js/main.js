// Main JavaScript file for Tech Solutions website

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Add scroll effect to navigation
    const navigation = document.querySelector('nav');
    
    if (navigation) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 10) {
                navigation.classList.add('bg-gray-900', 'bg-opacity-95', 'shadow-lg');
            } else {
                navigation.classList.remove('bg-gray-900', 'bg-opacity-95', 'shadow-lg');
            }
        });
    }
    
    // Form field animations
    const formFields = document.querySelectorAll('.form-field input, .form-field textarea, .form-field select');
    
    formFields.forEach(field => {
        // Initial check for pre-filled fields (e.g., after form submission error)
        if (field.value !== '') {
            field.classList.add('not-empty');
        }
        
        // Add event listeners
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        field.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            
            if (this.value === '') {
                this.classList.remove('not-empty');
            } else {
                this.classList.add('not-empty');
            }
        });
    });
    
    
    // Add animation to elements when they come into view
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const animateObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-visible');
                animateObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        animateObserver.observe(element);
    });
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span>Processing...</span>';
            }
        });
    });
});