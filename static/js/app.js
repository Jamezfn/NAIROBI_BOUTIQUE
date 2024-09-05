// Example: Moving the boutique row (like sliding)
const boutiqueRow = document.querySelector('.boutique-row');

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
        boutiqueRow.scrollLeft += 200;
    } else if (event.key === 'ArrowLeft') {
        boutiqueRow.scrollLeft -= 200;
    }
});

// Add to Bucket List functionality
document.querySelectorAll('.add-to-bucket').forEach(button => {
    button.addEventListener('click', function() {
        alert('Added to Bucket List!');
    });
});

// Remove from Bucket List functionality
document.querySelectorAll('.remove-from-bucket').forEach(button => {
    button.addEventListener('click', function() {
        alert('Removed from Bucket List!');
    });
});

// Proceed to Checkout functionality
document.querySelector('.checkout-button').addEventListener('click', function() {
    alert('Proceeding to checkout...');
});

// Basic form validation example
document.querySelector('form').addEventListener('submit', function(event) {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert('Please fill in all fields');
        event.preventDefault();
    }
});

// Basic form validation example
document.querySelector('form').addEventListener('submit', function(event) {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const accountType = document.getElementById('account-type').value;

    if (!name || !email || !password || !accountType) {
        alert('Please fill in all fields');
        event.preventDefault();
    }
});
