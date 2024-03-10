/**
 * Resizes a text areas height to the textareas scrollheights value, as the user
 * enters text. Intended for use with oninput. 
 * @param {textarea} - the text area element to be resized. 
*/

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px'; // Set to scroll height
    textarea.addEventListener("input", OnInput, false);
}