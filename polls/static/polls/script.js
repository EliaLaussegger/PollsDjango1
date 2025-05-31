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
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.box').forEach(box => {
    box.addEventListener('click', (event) => {
      // Falls direkt auf Link geklickt wurde, nichts tun, damit Link normal funktioniert
      if (event.target.closest('.button-link')) {
        return;
      }

      // Sonst Link im .box finden und dahin navigieren
      const link = box.querySelector('.button-link');
      if (link) {
        window.location.href = link.href;
      }
    });
  });
});