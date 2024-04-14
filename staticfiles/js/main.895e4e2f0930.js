document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'page-content' && document.getElementById('id_body')) {
        document.getElementById('id_body').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); // Prevent adding a new line
                
                // Attach an event listener to htmx:afterOnLoad event to clear the textarea
                // This event is triggered after the response has been successfully received and processed
                var clearTextareaAfterSuccess = function() {
                    document.getElementById('id_body').value = ''; // Clear the textarea
                    // Detach the event listener to ensure it only runs once per submission
                    document.body.removeEventListener('htmx:afterOnLoad', clearTextareaAfterSuccess);
                };
                
                document.body.addEventListener('htmx:afterOnLoad', clearTextareaAfterSuccess);
                
                // Trigger HTMX to submit the form
                htmx.trigger(this.form, 'submit', {target: this.form});
            }
        });
    }
});


document.body.addEventListener('htmx:afterSwap', function(event) {
    // Check if the swapped content is inside #entry-message-list
    if (event.detail.target.id === 'entry-message-list') {
        // Apply the fadeIn class to all li elements inside #entry-message-list
        var items = document.querySelectorAll('#entry-message-list li');
        items.forEach(function(item) {
            item.classList.add('message-fade-in');
        });
    }
});