// scene-specific always-on loops
tl.to(".sun-rays", { rotation: 90, duration: 4.3, ease: "none" }, 0);
tl.to(".cf-blades", { rotation: 360 * 9, duration: 5.1, ease: "none" }, 13.5);

// ---------- heat haze ----------
tl.fromTo(".h1", { y: 0, opacity: 0.8 }, { y: -260, opacity: 0, duration: 1.4, repeat: 2, ease: "sine.in", stagger: 0.35 }, 0);
tl.fromTo(".h7", { y: 0, opacity: 0.8 }, { y: -260, opacity: 0, duration: 1.2, repeat: 2, ease: "sine.in", stagger: 0.3 }, 22.8);

// ---------- S1 hook (frame 0 already shows the hook) ----------
show("#wk-sweat", 0, 1);
tl.fromTo("#s1-title", { scale: 0.96 }, { scale: 1, duration: 0.5, ease: "elastic.out(1, 0.4)" }, 0);
tl.fromTo("#s1-sun", { y: 40, rotation: -10 }, { y: 0, rotation: 6, duration: 1.2, yoyo: true, repeat: 2, ease: "sine.inOut" }, 0);
tl.fromTo("#wk-sweat .drop", { y: 0 }, { y: 40, duration: 0.6, repeat: 6, ease: "power1.in", stagger: 0.2 }, 0);
earWiggle(3.3, 3);

// ---------- S2 "I checked" ----------
whip("#s2", 4.1);
place(4.1, 540, 1390, 1.0, 0.3);
show("#wk-sweat", 4.1, 0);
smug(4.4, 1.4);
tl.fromTo("#s2-stamp", { scale: 3, opacity: 0, rotation: -20 }, { scale: 1, opacity: 1, rotation: -8, duration: 0.25, ease: "power4.in" }, 5.25);
shake(5.5, 14);

// ---------- S3 10 AM: lifts a car ----------
whip("#s3", 6.05);
place(6.05, 230, 1390, 0.72, 0.25);
pop("#s3-clock", 6.15);
tl.to("#s3-robot .rb-armR", { rotation: -150, duration: 0.5, ease: "back.out(2)" }, 7.2);
tl.to("#s3-car", { x: 230, y: -560, rotation: -8, duration: 0.55, ease: "back.out(1.6)" }, 7.25);
tl.to("#s3-car", { y: -575, duration: 0.3, yoyo: true, repeat: 4, ease: "sine.inOut" }, 7.8);
shock(7.5, 1.2);
pop("#p-mass", 8.55); shake(8.6); punch("#s3", 8.6); earWiggle(8.7, 3);

// ---------- S4 12 noon: dosa on his head ----------
whip("#s4", 9.55);
place(9.55, 220, 1390, 0.72, 0.25);
show("#wk-sweat", 9.55, 1);
pop("#s4-clock", 9.65);
tl.to("#s4-robot .rb-hot", { opacity: 0.85, duration: 0.9, ease: "power1.in" }, 10.1);
tl.to("#s4-robot .rb-steam", { opacity: 1, duration: 0.3 }, 10.7);
tl.fromTo("#s4-robot .rb-steam circle", { y: 0 }, { y: -60, duration: 0.6, repeat: 4, stagger: 0.15, ease: "sine.out" }, 10.7);
tl.fromTo("#s4-hand", { x: -820, y: -60 }, { x: 0, y: 0, duration: 0.35, ease: "back.out(1.7)" }, 11.0);
tl.fromTo("#s4-hand .batter", { scaleY: 0 }, { scaleY: 1, duration: 0.3 }, 11.45);
tl.to("#s4-hand .batter", { opacity: 0, duration: 0.15 }, 11.95);
tl.fromTo("#s4-robot .rb-dosa", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, 11.8);
tl.to("#s4-robot .rb-dosa", { y: -70, rotation: 360, duration: 0.45, yoyo: true, repeat: 1, ease: "power2.out" }, 12.9);
tl.to("#s4-hand", { x: -900, duration: 0.3, ease: "power2.in" }, 13.1);
tl.to("#wk-armR", { rotation: -25, duration: 0.06, yoyo: true, repeat: 30, ease: "none" }, 9.8);
pop("#p-bro", 12.55); shake(12.6); earWiggle(12.6, 3);

// ---------- S5 2 PM: fighting over the ceiling-fan spot ----------
whip("#s5", 13.5);
show("#wk-sweat", 13.5, 0);
place(13.5, 420, 1310, 0.8, 0.25);
pop("#s5-clock", 13.6);
// shove-off: robot leans left, Whiskers leans right
for (let i = 0; i < 6; i++) {
  const t = 15.0 + i * 0.28;
  tl.to("#wk-wrap", { x: 420 - 220 * 0.8 + (i % 2 ? 50 : -10), rotation: i % 2 ? 8 : -4, duration: 0.14, ease: "power2.out" }, t);
  tl.to("#s5-robot", { x: i % 2 ? 40 : -60, rotation: i % 2 ? 4 : -6, duration: 0.14, ease: "power2.out" }, t);
}
// robot wins: Whiskers flies out to the left
tl.to("#wk-wrap", { x: 60 - 220 * 0.8, y: 1390 - 680 * 0.8, rotation: -18, duration: 0.3, ease: "power3.out" }, 16.7);
tl.to("#s5-robot", { x: -200, rotation: 0, duration: 0.3, ease: "power3.out" }, 16.7);
tl.to("#wk-wrap", { rotation: 0, duration: 0.3 }, 17.4);
show("#wk-tears", 16.8, 1); show("#wk-tears", 18.3, 0);
pop("#p-nooo", 16.7); shake(16.75, 22);

// ---------- S6 Uh-oh: overheated, try again in November ----------
tl.fromTo("#s6", { opacity: 0 }, { opacity: 1, duration: 0.08 }, 18.3);
place(18.3, 220, 1390, 0.74);
tl.set("#wk-wrap", { rotation: 0 }, 18.3);
shock(18.45, 1.6);
tl.fromTo("#s6-robot", { scale: 1.12 }, { scale: 1, duration: 0.4, ease: "power2.out" }, 18.3);
tl.set("#s6-robot .rb-ok", { opacity: 0 }, 19.2);
tl.set("#s6-robot .rb-msg", { opacity: 1 }, 19.2);
for (let i = 0; i < 6; i++) tl.set("#s6-robot .rb-msg", { opacity: i % 2 ? 1 : 0.25 }, 19.5 + i * 0.25);
tl.set("#s6-robot .rb-msg", { opacity: 1 }, 21.0);
tl.to("#s6-robot .rb-steam", { opacity: 1, duration: 0.2 }, 19.2);
tl.fromTo("#s6-robot .rb-steam circle", { y: 0 }, { y: -70, duration: 0.6, repeat: 5, stagger: 0.12, ease: "sine.out" }, 19.2);
tl.fromTo("#s6-cal", { y: -500, rotation: -30 }, { y: 0, rotation: -6, duration: 0.45, ease: "bounce.out" }, 21.3);
pop("#p-what", 20.2); shake(20.25, 24); earWiggle(20.4, 3);

// ---------- S7 fanning with ears -> toasted bunny ----------
whip("#s7", 22.8);
place(22.8, 470, 1390, 1.0, 0.3);
tl.to("#wk-earL", { rotation: -30, duration: 0.09, yoyo: true, repeat: 17, ease: "sine.inOut" }, 23.0);
tl.to("#wk-earR", { rotation: 30, duration: 0.09, yoyo: true, repeat: 17, ease: "sine.inOut" }, 23.0);
tl.to(["#wk-earL-toast", "#wk-earR-toast"], { opacity: 1, duration: 0.35 }, 24.75);
tl.to("#wk-smoke", { opacity: 1, duration: 0.2 }, 24.9);
tl.fromTo("#wk-smoke circle", { y: 0 }, { y: -50, duration: 0.6, repeat: 2, stagger: 0.12, ease: "sine.out" }, 24.9);
show("#wk-tears", 25.3, 1);
pop("#p-toast", 25.15); shake(25.2, 18);
tl.to("#wk-smoke", { opacity: 0, duration: 0.3 }, 26.1);
show("#wk-tears", 26.2, 0);
tl.to(["#wk-earL-toast", "#wk-earR-toast"], { opacity: 0, duration: 0.2 }, 26.2);

// ---------- S8 Why so ----------
whip("#s8", 26.2);
place(26.2, 540, 1390, 0.66, 0.3);
tl.fromTo("#s8-stamp", { scale: 3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "power4.in" }, 26.3);
shake(26.55, 14);
tl.fromTo("#s8-phone", { y: 700 }, { y: 0, duration: 0.45, ease: "back.out(1.5)" }, 27.3);
tl.fromTo("#s8-therm", { y: 800 }, { y: 0, duration: 0.45, ease: "back.out(1.5)" }, 29.9);
tl.fromTo("#s8-therm .merc", { scaleY: 0.25 }, { scaleY: 1.0, duration: 1.2, ease: "power2.in" }, 30.4);
tl.set("#s8-hot", { opacity: 0 }, 26.2);
pop("#s8-hot", 31.55); shake(31.6, 22); shock(31.6, 1.0);
tl.to("#s8-therm", { rotation: 4, duration: 0.05, yoyo: true, repeat: 9 }, 31.6);

// ---------- S9 end card ----------
whip("#s9", 33.3);
place(33.3, 540, 1390, 0.85, 0.3);
tl.fromTo("#s9-tag", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }, 33.45);
tl.set("#s9-follow", { opacity: 0 }, 33.3);
pop("#s9-follow", 35.75);
tl.to("#wk-armL", { rotation: 55, duration: 0.18, yoyo: true, repeat: 9, ease: "sine.inOut" }, 35.6);
smug(33.6, 1.5);
