// Resize text area on page load and when the user enter text.

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


// Indicator upon requesting an AI prompt

const promptBtn = document.querySelector('#request-prompt-btn')

promptBtn.addEventListener('click', () => {
    const currentContent = promptBtn.textContent;
    promptBtn.disabled = true;
    promptBtn.getComputedStyle;
    promptBtn.innerHTML = `    
        <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
            <style>.spinner_qM83{animation:spinner_8HQG 1.05s infinite}.spinner_oXPr{animation-delay:.1s}.spinner_ZTLf{animation-delay:.2s}@keyframes spinner_8HQG{0%,57.14%{animation-timing-function:cubic-bezier(0.33,.66,.66,1);transform:translate(0)}28.57%{animation-timing-function:cubic-bezier(0.33,0,.66,.33);transform:translateY(-6px)}100%{transform:translate(0)}}</style>
            <circle class="spinner_qM83" cx="4" cy="12" r="3"/>
            <circle class="spinner_qM83 spinner_oXPr" cx="12" cy="12" r="3"/>
            <circle class="spinner_qM83 spinner_ZTLf" cx="20" cy="12" r="3"/>
        </svg>
    `

    setTimeout(() => {
        promptBtn.disabled = false;
        promptBtn.textContent = currentContent;
        promptBtn.classList.remove('prompt-fade');
    }, 2000)
})