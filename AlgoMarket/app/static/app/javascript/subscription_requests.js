//function to get the CSRF-token from cookies
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

//function to send POST request to initialize a creator's subscription
function createSubscription(event) {
    event.preventDefault();
    data = {
        'proPrice': event.target.elements.proPrice.value,
        'premiumPrice': event.target.elements.premiumPrice.value
    }
    fetch('/subscription', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify(data)
    }).then(response => {
        return response.text();
    }).then(html => {
        document.open();
        document.write(html);
        document.close();
    });
}