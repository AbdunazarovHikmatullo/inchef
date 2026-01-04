// Product Catalog and Detail Page JavaScript

// Change main image on thumbnail click
function changeMainImage(thumbnail) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage && thumbnail) {
        mainImage.src = thumbnail.src;

        // Update active thumbnail
        document.querySelectorAll('.thumbnail').forEach(thumb => {
            thumb.classList.remove('active');
        });
        thumbnail.classList.add('active');
    }
}

// Quantity controls
function increaseQuantity() {
    const input = document.getElementById('quantityInput');
    if (input) {
        const currentValue = parseInt(input.value) || 1;
        const maxValue = parseInt(input.max) || 10;
        if (currentValue < maxValue) {
            input.value = currentValue + 1;
        }
    }
}

function decreaseQuantity() {
    const input = document.getElementById('quantityInput');
    if (input) {
        const currentValue = parseInt(input.value) || 1;
        const minValue = parseInt(input.min) || 1;
        if (currentValue > minValue) {
            input.value = currentValue - 1;
        }
    }
}

// Add to cart with animation
document.addEventListener('DOMContentLoaded', function () {
    const addToCartForm = document.getElementById('addToCartForm');

    if (addToCartForm) {
        addToCartForm.addEventListener('submit', function (e) {
            const button = this.querySelector('.add-to-cart-btn');
            if (button) {
                button.textContent = '✓ Добавлено!';
                button.style.backgroundColor = '#4CAF50';

                setTimeout(() => {
                    button.textContent = '🛒 Добавить в корзину';
                    button.style.backgroundColor = '';
                }, 2000);
            }
        });
    }

    // Smooth scroll for breadcrumb links
    document.querySelectorAll('.breadcrumb a').forEach(link => {
        link.addEventListener('click', function (e) {
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // Image zoom effect on main image
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.addEventListener('click', function () {
            this.style.cursor = this.style.cursor === 'zoom-out' ? 'zoom-in' : 'zoom-out';
            this.style.transform = this.style.transform === 'scale(1.5)' ? 'scale(1)' : 'scale(1.5)';
            this.style.transition = 'transform 0.3s ease';
        });
    }
});

// Search autocomplete (можно расширить позже)
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    searchInput.addEventListener('input', function (e) {
        const query = e.target.value;
        // Здесь можно добавить AJAX запрос для автодополнения
        console.log('Searching for:', query);
    });
}

// Card hover effect enhancement
document.addEventListener('DOMContentLoaded', function () {
    const productCards = document.querySelectorAll('.product-card');

    productCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transition = 'all 0.3s ease';
        });
    });
});

// Filter animations
const categoryLinks = document.querySelectorAll('.category-link');
categoryLinks.forEach(link => {
    link.addEventListener('click', function (e) {
        // Add loading animation
        const grid = document.querySelector('.products-grid');
        if (grid) {
            grid.style.opacity = '0.5';
            setTimeout(() => {
                grid.style.opacity = '1';
            }, 300);
        }
    });
});

// Image lazy loading enhancement
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('.product-image, .main-image').forEach(img => {
        imageObserver.observe(img);
    });
}
