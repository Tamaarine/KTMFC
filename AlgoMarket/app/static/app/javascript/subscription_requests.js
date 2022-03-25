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

//function to add a perk in the subscription table
function addPerk() {
    const selectService = document.getElementById("inputService");
    const service_id = selectService.value;
    const service_name = selectService.options[selectService.selectedIndex].text;
    const table = document.getElementById('perkTable');
    const row = document.createElement('tr');
    row.innerHTML = "<th class='align-middle' scope='row'>"+service_name+"</th><td class='align-middle'><input class='form-control' name='perk-"+service_id+"-FreeAmount' type='number' value='0' required /></td><td class='align-middle'><input class='form-control' name='perk-"+service_id+"-ProAmount' type='number' value='0' required /></td><td class='align-middle'><input class='form-control' name='perk-"+service_id+"-PremiumAmount' type='number' value='0' required /></td><td class='align-middle'><button type='button' class='btn btn-danger'>Remove</button></td>";
    table.appendChild(row);
}

//function to remove a perk from the subscription table
function removePerk(event) {

}

//function to send a PUT request to update the subscription details
function updateSubscription(event) {
    event.preventDefault();
    const perk_list = {};
    for (index in event.target.elements) {
        let element = event.target.elements[index];
        if(element.name && element.name.startsWith('perk')) {
            let [, id, tier] = element.name.split('-');
            if (!(id in perk_list)) {
                perk_list[id] = {};
            }
            perk_list[id][tier] = element.value;
        }
    }
    const data = {
        'pro_price': event.target.elements.proPrice.value,
        'premium_price': event.target.elements.premiumPrice.value,
        'perk_list': perk_list
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