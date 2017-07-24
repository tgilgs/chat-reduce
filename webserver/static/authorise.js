// Letter reveal for the app name using GSAP Tween Lite
window.onload = function(){
  var tl = new TimelineLite({delay: 1}),
      firstBG = document.querySelectorAll('.letter1_bg'),
      secondBG = document.querySelectorAll('.letter2_bg'),
      thirdBG = document.querySelectorAll('.letter3_bg'),
      fourthBG = document.querySelectorAll('.letter4_bg'),
      fifthBG = document.querySelectorAll('.letter5_bg'),
      letter1 = document.querySelectorAll('.letter1'),
      letter2 = document.querySelectorAll('.letter2'),
      letter3 = document.querySelectorAll('.letter3'),
      letter4 = document.querySelectorAll('.letter4'),
      letter5 = document.querySelectorAll('.letter5'),
      redirect = document.querySelectorAll('.redirect');

  tl
    .to(firstBG, 0.2, {scaleX:1})
    .to(letter1, 0.1, {opacity:1}, "-=0.1")
    .to(firstBG, 0.2, {scaleX:0})
    .to(secondBG, 0.2, {scaleX:1})
    .to(letter2, 0.1, {opacity:1}, "-=0.1")
    .to(secondBG, 0.2, {scaleX:0})
    .to(thirdBG, 0.2, {scaleX:1})
    .to(letter3, 0.1, {opacity:1}, "-=0.1")
    .to(thirdBG, 0.2, {scaleX:0})
    .to(fourthBG, 0.2, {scaleX:1})
    .to(letter4, 0.1, {opacity:1}, "-=0.1")
    .to(fourthBG, 0.2, {scaleX:0})
    .to(fifthBG, 0.2, {scaleX:1})
    .to(letter5, 0.1, {opacity:1}, "-=0.1")
    .to(fifthBG, 0.2, {scaleX:0})
    .to(redirect, 0.1, {opacity:1}, "+=0.5");
}
