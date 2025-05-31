const boxes = document.querySelectorAll('.box');

boxes.forEach(box => {
  const buttonLink = box.querySelector('.button-link');
  
  if (!buttonLink) return;
  
  box.addEventListener('mouseenter', () => {
    buttonLink.style.backgroundColor = 'rgb(70, 69, 69)';
    buttonLink.style.animation = 'none';
  });

  box.addEventListener('mouseleave', () => {
    buttonLink.style.backgroundColor = 'rgb(105, 105, 105)';
    buttonLink.style.animation = '';
  });
});