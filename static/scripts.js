const form = document.querySelector('form');
const button = document.querySelector('form button');

let isSubmited = false;

form.addEventListener('submit', event => {
    if (isSubmited) {
        event.preventDefault();
    } else {
        button.disabled = true;
        isSubmited = true;
    }
});