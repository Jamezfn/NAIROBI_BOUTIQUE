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

// Function to handle adding items to the bucket list
function addToBucketList(itemId) {
    fetch('/bucketlist/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ item_id: itemId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Item added to bucket list!');
        }
    })
    .catch(error => console.error('Error adding to bucket list:', error));
}

// Function to handle removing items from the bucket list
function removeFromBucketList(itemId) {
    fetch(`/bucketlist/remove/${itemId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Item removed from bucket list!');
        }
    })
    .catch(error => console.error('Error removing from bucket list:', error));
}

// Function to handle proceeding to checkout
function proceedToCheckout() {
    alert('Proceeding to checkout...');
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Scroll boutique row functionality
    const boutiqueRow = document.querySelector('.boutique-row');
    if (boutiqueRow) {
        document.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowRight') {
                boutiqueRow.scrollLeft += 200;
            } else if (event.key === 'ArrowLeft') {
                boutiqueRow.scrollLeft -= 200;
            }
        });
    }

    // Add to Bucket List functionality
    document.querySelectorAll('.add-to-bucket-list').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            addToBucketList(itemId);
        });
    });

    // Remove from Bucket List functionality
    document.querySelectorAll('.remove-from-bucket').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            removeFromBucketList(itemId);
        });
    });

    // Proceed to Checkout functionality
    const checkoutButton = document.querySelector('.checkout-button');
    if (checkoutButton) {
        checkoutButton.addEventListener('click', proceedToCheckout);
    }

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
});
