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

//function to sent POST request for creating a new service
function addService(event) {
    event.preventDefault();
    data = {
        'name': event.target.elements.name.value,
        'description': event.target.elements.description.value,
        'price': event.target.elements.price.value
    }
    fetch('/services', {
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

//function to send a PUT request for updating a service in the database
function updateService(event) {
    event.preventDefault();
    data = {
        'id': event.target.elements.id.value,
        'name': event.target.elements.name.value,
        'description': event.target.elements.description.value,
        'price': event.target.elements.price.value
    }
    fetch('/services', {
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