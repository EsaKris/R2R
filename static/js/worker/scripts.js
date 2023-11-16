const okjhvg = document.getElementById("form-box");
const djs = document.getElementById('mianeor')

function openmodal() {
    okjhvg.style.display ="block";
    djs.style.overflow = "hidden";
    djs.style.height = "90vh";
}

function closemodal() {
    okjhvg.style.display ="none";
    djs.style.overflow = "scroll";
    djs.style.height = "100%";
}