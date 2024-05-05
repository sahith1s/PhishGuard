window.addEventListener('scroll', function() {
    let sections = document.querySelectorAll(".movie-info");
    sections.forEach(sec => {
      let top = window.scrollY;
      let offset = sec.offsetTop - 150;
      let height = sec.offsetHeight;
      if (top >= offset && top < offset + height) {
        sec.classList.add('show-animate');
      } else {
        sec.classList.remove('show-animate')
      }
    });
  });