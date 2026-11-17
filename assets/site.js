// Soliko Games — header slider: two phrases that trade places (the active one rises, shrinks and fades
// away; the next one rises from below and grows), with the background crossfading. Autoplay every 5 s,
// paused while the pointer or the focus is in the header and under reduced motion.
(function () {
	"use strict";

	var top = document.querySelector(".top");
	if (!top) return;

	var slides = top.querySelectorAll(".slide");
	var bgs = top.querySelectorAll(".top__bg");
	var dots = top.querySelectorAll(".dots span");
	var counter = top.querySelector(".counter");
	var n = slides.length;
	var active = 0;

	var slider = top.querySelector(".slider");

	// the next phrase waits just under the active one, whatever its number of lines
	function measure() {
		if (slider) slider.style.setProperty("--shift", slides[active].offsetHeight + 28 + "px");
	}

	function render() {
		for (var j = 0; j < n; j++) {
			var pos = j === active ? "active" : j > active ? "next" : "prev";
			slides[j].setAttribute("data-pos", pos);
			slides[j].setAttribute("aria-hidden", j === active ? "false" : "true");
			if (bgs[j]) bgs[j].setAttribute("data-pos", j === active ? "active" : "off");
			if (dots[j]) dots[j].classList.toggle("is-on", j === active);
		}
		if (counter) counter.textContent = active + 1 + "/" + n;
	}

	function go(i) {
		active = (i + n) % n;
		measure();
		render();
	}

	var prev = top.querySelector("[data-prev]");
	var next = top.querySelector("[data-next]");
	if (prev) prev.addEventListener("click", function () { go(active - 1); restart(); });
	if (next) next.addEventListener("click", function () { go(active + 1); restart(); });

	var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
	var timer = null;
	var paused = false;

	function restart() {
		if (timer) clearInterval(timer);
		if (reduced) return;
		timer = setInterval(function () {
			if (!paused && !document.hidden) go(active + 1);
		}, 5000);
	}

	top.addEventListener("mouseenter", function () { paused = true; });
	top.addEventListener("mouseleave", function () { paused = false; });
	top.addEventListener("focusin", function () { paused = true; });
	top.addEventListener("focusout", function () { paused = false; });

	measure();
	window.addEventListener("resize", measure);
	if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
	render();
	restart();
})();
