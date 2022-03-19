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

//function to send a PUT request for updating a service in the database
async function updateService(event) {
    event.preventDefault();
    const response = await fetch('/services', {
        method: 'PUT',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: event.target.elements
    });
}