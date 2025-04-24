// hero-animations.js - Place in static/js/hero-animations.js

document.addEventListener('DOMContentLoaded', function() {
    // Text typing animation
    const typedTextElement = document.getElementById('typed-text');
    const cursorElement = document.getElementById('cursor');
    
    const textOptions = [
        "Digital Marketing Solutions",
        "Full Stack Development",
        "Custom Software",
        "CRM Integration",
        "HRMS Solutions",
        "VOIP Services",
        "API Development",
        "Autodialer Technology"
    ];
    
    let currentTextIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;
    
    function typeText() {
        const currentText = textOptions[currentTextIndex];
        
        if (isDeleting) {
            // Deleting text
            typedTextElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50; // Faster when deleting
        } else {
            // Typing text
            typedTextElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100; // Normal speed when typing
        }
        
        // When finished typing
        if (!isDeleting && charIndex === currentText.length) {
            isDeleting = true;
            typingSpeed = 1500; // Pause at the end of typing
        } 
        // When finished deleting
        else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            currentTextIndex = (currentTextIndex + 1) % textOptions.length;
            typingSpeed = 500; // Pause before typing the next text
        }
        
        setTimeout(typeText, typingSpeed);
    }
    
    // Start the typing animation
    typeText();
    
    // Particles animation
    const particlesContainer = document.getElementById('particles-container');
    
    function createParticles() {
        // Clear existing particles
        particlesContainer.innerHTML = '';
        
        // Create new particles
        for (let i = 0; i < 100; i++) {
            const particle = document.createElement('div');
            
            // Random position, size and opacity
            const size = Math.random() * 5 + 1;
            const posX = Math.random() * 100;
            const posY = Math.random() * 100;
            const opacity = Math.random() * 0.5 + 0.1;
            const duration = Math.random() * 20 + 10;
            const delay = Math.random() * 5;
            
            // Set styling
            particle.className = 'absolute rounded-full bg-blue-400';
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${posX}%`;
            particle.style.top = `${posY}%`;
            particle.style.opacity = opacity;
            particle.style.boxShadow = `0 0 ${size * 2}px rgba(59, 130, 246, ${opacity})`;
            
            // Animation
            particle.style.animation = `float ${duration}s linear ${delay}s infinite`;
            
            particlesContainer.appendChild(particle);
        }
    }
    
    // Create and inject CSS animation for particles
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
        @keyframes float {
            0% {
                transform: translateY(0) translateX(0);
            }
            25% {
                transform: translateY(-20px) translateX(10px);
            }
            50% {
                transform: translateY(-40px) translateX(-10px);
            }
            75% {
                transform: translateY(-60px) translateX(5px);
            }
            100% {
                transform: translateY(-100px) translateX(0);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(styleSheet);
    
    // Initialize particles
    createParticles();
    
    // Re-create particles periodically for better performance
    setInterval(createParticles, 20000);
    
    // Intersection Observer for reveal animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    // Apply to tech icon wrappers
    document.querySelectorAll('.tech-icon-wrapper').forEach(element => {
        observer.observe(element);
    });
});

// Main navigation functionality - Place in static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Scroll reveal effect
    const revealElements = document.querySelectorAll('.reveal');
    
    function checkReveal() {
        const windowHeight = window.innerHeight;
        const revealPoint = 150;
        
        revealElements.forEach(element => {
            const revealTop = element.getBoundingClientRect().top;
            
            if (revealTop < windowHeight - revealPoint) {
                element.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', checkReveal);
    checkReveal(); // Check on load
});