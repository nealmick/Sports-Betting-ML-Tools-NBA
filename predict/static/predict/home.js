var shopLoad = localStorage.getItem('shopLoad');

if (shopLoad === null) {
    localStorage.setItem('shopLoad', true);
}

document.addEventListener("DOMContentLoaded", function() {
  if (!localStorage.getItem('welcomeShown6')) {
    // Show the popup and apply blur effect
    //document.getElementById("welcomePopup").style.display = "flex";
    //document.getElementById("mainContent").classList.add("blur");
  }

  document.getElementById("closePopup").addEventListener("click", function() {
    document.getElementById("welcomePopup").style.display = "none";
    document.getElementById("mainContent").classList.remove("blur");
    localStorage.setItem('welcomeShown6', 'true');
  });
});
