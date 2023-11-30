var stripe = Stripe('your_publishable_key');  // Replace with your actual Stripe publishable key
var elements = stripe.elements();

// Create an instance of the card Element.
var card = elements.create('card');

// Add an instance of the card Element into the `card-element` div.
card.mount('#card-element');

// Handle form submission
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    stripe.createToken(card).then(function(result) {
        if (result.error) {
            // Inform the user if there was an error.
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            // Send the token to your server.
            stripeTokenHandler(result.token);
        }
    });
});

function stripeTokenHandler(token) {
    // You can send the token to your server here.
    // For example, using fetch():
    fetch('/charge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token.id }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // You may redirect or show a success message here
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle the error, show an error message, etc.
    });
}
