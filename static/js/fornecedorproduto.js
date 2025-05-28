const modal = document.querySelector('#productModal');
const openBtn = document.getElementById('openModal');
const closeBtn = document.querySelector('#close-btn');

console.log(modal);

openBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
);

