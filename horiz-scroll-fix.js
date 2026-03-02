// Convert vertical scroll to horizontal scroll on horizontal scroll containers 
// to aid desktop users in scrolling horizontally with mouse wheel.
//
// also helps with inexperienced users.
const horizontalScrollers = document.querySelectorAll('.scroll-h');

horizontalScrollers.forEach((scroller) => {
  scroller.addEventListener('wheel', (e) => {
    // Only convert vertical scrolling
    if (e.deltaY !== 0) {
      e.preventDefault();
      scroller.scrollLeft += e.deltaY;
    }
  });
});
