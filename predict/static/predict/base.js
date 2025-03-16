let arrow = document.querySelectorAll(".arrow");
for (var i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", (e) => {
    let arrowParent = e.target.parentElement.parentElement;
    arrowParent.classList.toggle("showMenu");
  });
}
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");
console.log(sidebarBtn);
sidebarBtn.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});

window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'AW-16453183002');

(function (h, o, t, j, a, r) {
  h.hj = h.hj || function () { (h.hj.q = h.hj.q || []).push(arguments) };
  h._hjSettings = { hjid: 3730209, hjsv: 6 };
  a = o.getElementsByTagName('head')[0];
  r = o.createElement('script'); r.async = 1;
  r.src = t + h._hjSettings.hjid + j + h._hjSettings.hjsv;
  a.appendChild(r);
})(window, document, 'https://static.hotjar.com/c/hotjar-', '.js?sv=');

document.addEventListener('DOMContentLoaded', (event) => {
  const currentTheme = localStorage.getItem('theme') || 'default';
  if (currentTheme === 'alternate') {
    document.documentElement.classList.add('alternate-theme');
  }
});

function resizeAllCharts() {
  var allCanvases = document.querySelectorAll('canvas');
  allCanvases.forEach(function (canvas) {
    if (canvas.chart instanceof Chart) {
      canvas.chart.update();
    }
  });
}

resizeAllCharts();
document.addEventListener('DOMContentLoaded', (event) => {
  resizeAllCharts();
});
setTimeout(function () {
  resizeAllCharts();
}, 100);

var Tawk_API = Tawk_API || {}, Tawk_LoadStart = new Date();
(function () {
  var s1 = document.createElement("script"), s0 = document.getElementsByTagName("script")[0];
  s1.async = true;
  s1.src = 'https://embed.tawk.to/65a414068d261e1b5f533b49/1hk4eseud';
  s1.charset = 'UTF-8';
  s1.setAttribute('crossorigin', '*');
  s0.parentNode.insertBefore(s1, s0);
})();

$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
});
var r = document.querySelector(':root');
function myFunction_set() {
  var randomNumber = Math.floor(Math.random() * 60) + 1;
  r.style.setProperty('--rotation', randomNumber + 'deg');
}
myFunction_set();

document.addEventListener('DOMContentLoaded', function () {
  if (navigator.userAgent.indexOf("Win") != -1) {
    console.log('windows detected');
    var containers = document.querySelectorAll('.container-fluid');
    containers.forEach(function (container) {
      container.style.maxWidth = '1100px';
    });
  }
});
