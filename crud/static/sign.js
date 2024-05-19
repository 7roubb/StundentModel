const wrapper = document.querySelector('.wraapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
setTimeout(() => {
   const messages = document.querySelectorAll('.message');
   messages.forEach(message => {
       message.style.opacity = '0';
       setTimeout(() => message.remove(), 500); // remove after transition
   });
 }, 3000);
registerLink.addEventListener('click', () => {
   wrapper.classList.add('active');
});

loginLink.addEventListener('click', () => {
wrapper.classList.remove('active');
});