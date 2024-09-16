// Scroll boutique row functionality
const boutiqueRow = document.querySelector('.boutique-row');

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
        boutiqueRow.scrollLeft += 200;
    } else if (event.key === 'ArrowLeft') {
        boutiqueRow.scrollLeft -= 200;
    }
});

// Fetching boutiques and displaying them dynamically
document.addEventListener('DOMContentLoaded', function() {
    fetch('/boutiques/list')
        .then(response => response.json())
        .then(boutiques => {
            const boutiqueContainer = document.getElementById('boutique-container');
            boutiqueContainer.innerHTML = boutiques.map(boutique => `
                <div class="boutique-card">
                    <img src="{{ url_for('static', filename='images/shop-placeholder.jpg') }}" alt="${boutique.name}">
                    <h4>${boutique.name}</h4>
                    <p>${boutique.description}</p>
                </div>
            `).join('');
        })
        .catch(error => console.error('Error fetching boutiques:', error));
});


// Add to Bucket List functionality
document.querySelectorAll('.add-to-bucket').forEach(button => {
    button.addEventListener('click', function() {
        const itemId = this.dataset.itemId;
        fetch('/bucketlist/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ item_id: itemId }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
    });
});

// Remove from Bucket List functionality
document.querySelectorAll('.remove-from-bucket').forEach(button => {
    button.addEventListener('click', function() {
        const itemId = this.dataset.itemId;
        fetch(`/bucketlist/remove/${itemId}`, {  // Changed to include item_id in URL
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
    });
});

// Proceed to Checkout functionality
document.querySelector('.checkout-button').addEventListener('click', function() {
    alert('Proceeding to checkout...');
});

// Basic form validation example
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(event) {
        const fields = Array.from(form.querySelectorAll('input')).map(input => input.value);
        if (fields.some(field => !field)) {
            alert('Please fill in all fields');
            event.preventDefault();
        }
    });
});
