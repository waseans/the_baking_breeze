// static/js/slider.js
let slideIndex = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.card');
    const totalSlides = slides.length;
    if (index >= totalSlides) {
        slideIndex = 0;
    } else if (index < 0) {
        slideIndex = totalSlides - 1;
    } else {
        slideIndex = index;
    }
    const offset = -slideIndex * 100;
    document.querySelector('.slider-container').style.transform = `translateX(${offset}%)`;
}

function moveSlide(step) {
    showSlide(slideIndex + step);
}

document.addEventListener('DOMContentLoaded', () => {
    showSlide(slideIndex);
});
