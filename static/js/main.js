// Funtastik Toy Store JavaScript

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    initializeProductCards();
    initializeCartFunctionality();
    initializeFormValidation();
    initializeImageLazyLoading();
    initializeTooltips();
    initializeAnimations();
}

// Product Cards Enhancement
function initializeProductCards() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-lg');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-lg');
        });
        
        // Add click tracking
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.btn')) {
                const productLink = this.querySelector('a[href*="product"]');
                if (productLink) {
                    window.location.href = productLink.href;
                }
            }
        });
    });
}

// Cart Functionality
function initializeCartFunctionality() {
    // Add to cart forms
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('button[type="submit"]');
            const originalText = button.innerHTML;
            
            // Show loading state
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Добавляем...';
            button.disabled = true;
            
            // Re-enable button after form submission
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
        });
    });
    
    // Quantity input validation
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const min = parseInt(this.min) || 1;
            const max = parseInt(this.max) || 100;
            let value = parseInt(this.value);
            
            if (value < min) {
                this.value = min;
                showNotification('Минимальное количество: ' + min, 'warning');
            } else if (value > max) {
                this.value = max;
                showNotification('Максимальное количество: ' + max, 'warning');
            }
        });
    });
    
    // Update cart item forms
    const updateCartForms = document.querySelectorAll('form[action*="update"]');
    
    updateCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('button[type="submit"]');
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            button.disabled = true;
        });
    });
}

// Form Validation Enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showNotification('Пожалуйста, заполните все обязательные поля', 'error');
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input[required], select[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

// Validate individual field
function validateField(field) {
    const isValid = field.checkValidity();
    
    if (!isValid) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
    } else {
        field.classList.add('is-valid');
        field.classList.remove('is-invalid');
    }
    
    return isValid;
}

// Validate entire form
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('input[required], select[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Image Lazy Loading
function initializeImageLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('loading');
                    observer.unobserve(img);
                }
            });
        });
        
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => imageObserver.observe(img));
    }
}

// Initialize Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize Animations
function initializeAnimations() {
    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated', 'animate__fadeInUp');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.card, .feature-item');
    animatedElements.forEach(el => observer.observe(el));
}

// Utility Functions

// Show notification
function showNotification(message, type = 'info') {
    const alertClass = getAlertClass(type);
    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Get Bootstrap alert class
function getAlertClass(type) {
    const classes = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    };
    return classes[type] || 'alert-info';
}

// Format price
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
    }).format(price);
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search functionality
const searchInput = document.querySelector('input[name="search"]');
if (searchInput) {
    const debouncedSearch = debounce(function(e) {
        if (e.target.value.length >= 3 || e.target.value.length === 0) {
            // Auto-submit search form when user stops typing
            const form = e.target.closest('form');
            if (form) {
                form.submit();
            }
        }
    }, 500);
    
    searchInput.addEventListener('input', debouncedSearch);
}

// Price range filter (if implemented)
function initializePriceRange() {
    const priceInputs = document.querySelectorAll('input[type="range"]');
    
    priceInputs.forEach(input => {
        input.addEventListener('input', function() {
            const output = document.querySelector(`output[for="${this.id}"]`);
            if (output) {
                output.textContent = formatPrice(this.value);
            }
        });
    });
}

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    // Escape key closes modals and dropdowns
    if (e.key === 'Escape') {
        const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(dropdown => {
            const toggle = dropdown.previousElementSibling;
            if (toggle) {
                bootstrap.Dropdown.getInstance(toggle)?.hide();
            }
        });
    }
    
    // Ctrl+K for search focus
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// Performance monitoring
function measurePerformance() {
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log(`Page load time: ${loadTime}ms`);
            
            // Send to analytics if needed
            if (loadTime > 3000) {
                console.warn('Page load time is slow:', loadTime);
            }
        });
    }
}

// Initialize performance monitoring
measurePerformance();

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateForm,
        validateField,
        formatPrice,
        debounce
    };
}
