
function handleSortUpdate(divElement) {
    var options = {
        method: 'POST',
        mode: 'same-origin'
    }
    sortable(divElement, {
        forcePlaceHolderSize: true,
        placeholderClass: 'border border-5 p-10'
    })[0].addEventListener('sortupdate', function(e) {
        var order = {};
        if (divElement === '#modules') {
            var module_elements = document.querySelectorAll('#modules li');
            module_elements.forEach(function (element, index) {order[element.dataset.id] = index + 1;});
            options['body'] = JSON.stringify(order)
            fetch(moduleOrderUrl, options)
            .then(response => {
                if (!response.ok) {
                    window.alert('There was error, try again later.')
                    return;
                }
                window.alert('Order was changed successfully')
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
        }   else if (divElement === '#content') {
            elements = document.querySelectorAll('#content .content-item')
            elements.forEach(function (element, index)
            {order[element.dataset.id] = index + 1;});
            options['body'] = JSON.stringify(order)
            fetch(contentOrderUrl, options)
            .then(response => {
                if (!response.ok) {
                    window.alert('There was error, try again later.')
                    return;
                }
                window.alert('Order was changed successfully')
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
        }
    });
}

handleSortUpdate('#modules')
handleSortUpdate('#content')

function handleDelete(contentId) {
    var options = {
        method: 'POST',
        mode: 'same-origin'
    }
    order = {};
    model = '';
    content = document.querySelectorAll('.content-item .delete' )
    // get deleteButton and find its closests content-item to delete it from page
    var deleteButton = document.querySelector(`.content-item [data-id="${contentId}"]`);
    var contentDiv = deleteButton.closest('.content-item');
    console.log(contentDiv);
    content.forEach(
        function(element, index) {
            order[element.dataset.id] = index + 1;
            if (element.dataset.id===contentId){
                model = element.dataset.model;
            }
        }
    );
    options['body'] = JSON.stringify({
        'content_id': contentId,
        'model': model,
        'order': order
    })
    console.log(order);
    fetch(ccontentDeleteUrl, options)
    .then(response => {
        if (!response.ok) {
            // Handle error response
            return response.json(); // Parse JSON response
        }
        contentDiv.remove();
        window.alert('Item was deleted successfully');
    })
    .then(data => {
        // Check for error message in the parsed JSON response
        if (data && data.status === 'error') {
            window.alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}


// get all delete buttons for content and handleDelete() to each
content = document.querySelectorAll('.content-item .delete' )
content.forEach(function (element){
    var contentId = element.dataset.id;
    element.addEventListener('click', function () {
        handleDelete(contentId);
    });
});