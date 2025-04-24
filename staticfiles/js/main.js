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
    
    // Simple form validation
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    
                    // Add error message if it doesn't exist
                    const errorMessage = field.parentElement.querySelector('.error-message');
                    if (!errorMessage) {
                        const errorElement = document.createElement('p');
                        errorElement.className = 'text-red-500 text-xs mt-1 error-message';
                        errorElement.textContent = 'This field is required';
                        field.parentElement.appendChild(errorElement);
                    }
                } else {
                    field.classList.remove('border-red-500');
                    
                    // Remove error message if it exists
                    const errorMessage = field.parentElement.querySelector('.error-message');
                    if (errorMessage) {
                        errorMessage.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
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
});