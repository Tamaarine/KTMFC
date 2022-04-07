$(document).ready(function(){
    $('#searchForm').click(function(event) {
        childTextBox = $('#searchForm').find('#search');
        if(childTextBox.val() === '') {
            event.preventDefault();
        }
    })
});   

