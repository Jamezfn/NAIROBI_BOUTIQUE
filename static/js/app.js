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
fetch('/boutiques/list')  // Changed to fetch boutiques from the backend
    .then(response => response.json())
    .then(boutiques => {
        boutiqueRow.innerHTML = ''; // Clear existing boutique cards
        boutiques.forEach(boutique => {
            const boutiqueCard = `
                <div class="col-md-4">
                    <div class="card mb-4">
                        <img src="static/images/shop-placeholder.jpg" class="card-img-top" alt="${boutique.name}">
                        <div class="card-body">
                            <h4 class="card-title">${boutique.name}</h4>
                            <p class="card-text">${boutique.description}</p>
                        </div>
                    </div>
                </div>
            `;
            boutiqueRow.innerHTML += boutiqueCard;
        });
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
