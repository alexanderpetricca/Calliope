/**
 * Initializes auto resizing for a text area.
 * @param {HTMLElement} textarea - The text area element to be initialized.
 */
function initializeAutoResize(textarea) {
    function autoResize() {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    textarea.addEventListener("input", autoResize, false);

    // Immediately adjust the height in case of pre-filled content
    autoResize();
}


document.body.addEventListener('htmx:afterSwap', function(event) {
    // Select all text areas on the page and apply autoresize.
    const textAreas = event.target.querySelectorAll('textarea');
    textAreas.forEach(initializeAutoResize);
});