let currentSlide = 0;
const slides = document.querySelectorAll('.promo-item');
const dots = document.querySelectorAll('.dot');
const pauseBtn = document.getElementById('pauseBtn');

let autoSlide = true;
let slideInterval = setInterval(nextSlide, 4000);

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.style.display = (i === index) ? 'flex' : 'none';
    dots[i].classList.toggle('active', i === index);
  });
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

function prevSlide() {
  currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  showSlide(currentSlide);
}

function toggleAutoSlide() {
  autoSlide = !autoSlide;
  if (autoSlide) {
    slideInterval = setInterval(nextSlide, 4000);
    pauseBtn.textContent = '⏸';
  } else {
    clearInterval(slideInterval);
    pauseBtn.textContent = '▶';
  }
}

// Inicia exibindo apenas o primeiro slide
showSlide(currentSlide);

// Eventos
document.getElementById('nextBtn').addEventListener('click', () => {
  nextSlide();
  if (autoSlide) toggleAutoSlide(); // pausa se clicar manualmente
});

document.getElementById('prevBtn').addEventListener('click', () => {
  prevSlide();
  if (autoSlide) toggleAutoSlide();
});

pauseBtn.addEventListener('click', toggleAutoSlide);
