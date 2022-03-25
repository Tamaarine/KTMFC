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
function createSubscription() {
    fetch('/subscription', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')}
    }).then(response => {
        return response.text();
    }).then(html => {
        document.open();
        document.write(html);
        document.close();
    });
}

//function to send a PUT request to add a perk to the subscription
function addPerk(event) {
    event.preventDefault();
    data = {
        'service_id': event.target.elements.serviceSelect.value,
        'action': 'add-perk'
    }
    fetch('/subscription', {
        method: 'PUT',
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