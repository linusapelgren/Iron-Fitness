document.addEventListener('DOMContentLoaded', function() {
    var stripe = Stripe('pk_test_51PehLIRvzCaZ4Xmpa3fAje2VRg7BUCSTIi1eXeCjW6BKOtupBc7NRanFDF8E4IH145jRufJGJgBHnvSPA3tnJeBV00AcetY068');
    var elements = stripe.elements();
    var cardElement = elements.create('card');
    cardElement.mount('#card-element');

    var planId = "{{ plan_id }}"; // This should be rendered correctly in the template

    console.log('Plan ID:', planId); // Debugging line

    // Fetch order information
    fetch(`/checkout/order/${planId}/overview/`)
        .then(response => response.json())
        .then(data => {
            console.log(data); // Debugging line
            if (data.error) {
                document.getElementById('order-overview').innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById('order-overview').innerHTML = `
                    <p><strong>Name:</strong> ${data.name}</p>
                    <p><strong>Description:</strong> ${data.description}</p>
                    <p><strong>Price:</strong> $${data.price}</p>
                    <p><strong>Duration:</strong> ${data.duration}</p>
                    <p><strong>Benefit:</strong> ${data.benefit}</p>
                    <img src="${data.image_url}" alt="${data.name}" style="width: 100%; max-width: 200px;">
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching order information:', error);
        });

    document.getElementById('next-to-payment').addEventListener('click', function() {
        var contactInfoForm = document.getElementById('contact-info-form');
        if (contactInfoForm.checkValidity()) {
            document.getElementById('step-contact-info').style.display = 'none';
            document.getElementById('step-payment-info').style.display = 'block';
        }
    });

    document.getElementById('payment-form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('{% url "create_checkout_session" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                plan_id: planId // Pass the plan_id in the POST request
            }),
        })
        .then(response => response.json())
        .then(data => {
            return stripe.redirectToCheckout({ sessionId: data.id });
        })
        .then(result => {
            if (result.error) {
                alert(result.error.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
