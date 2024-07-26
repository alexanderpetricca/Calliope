
function resizeTextArea(textarea) {
    textarea.rows = 1;
    const lines = Math.floor(textarea.scrollHeight / parseFloat(getComputedStyle(textarea).lineHeight));
    textarea.rows = Math.max(lines, 1);
}


const textarea = document.querySelector('#id_content')
textarea.addEventListener('input', () => resizeTextArea(textarea));

document.addEventListener('DOMContentLoaded', () => {
    resizeTextArea(textarea)
})