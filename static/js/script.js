// Navbar Fixed
window.onscroll = function() {
    const header = document.querySelector('header');
    const fixedNav = header.offsetTop;

    if (window.pageYOffset > fixedNav) {
        header.classList.add('navbar-fixed');
    } else {
        header.classList.remove('navbar-fixed');
    }
};

// Hamburger
const hamburger = document.querySelector('#hamburger');
const navMenu = document.querySelector('#nav-menu');

hamburger.addEventListener('click', function() {
    hamburger.classList.toggle('hamburger-active');
    navMenu.classList.toggle('hidden')
});

//input file
// const label = ["Dos", "Probe", "R2L", "U2R", "Normal"]
// async function predict(file) {
//     file = file.files[0]
//     const form = new FormData()
//     form.append("file", file)
//     const response = await fetch("http://localhost:5000/home", {
//         method: "POST",
//         body: form
//     })
//     const result = await response.json()
//     const ol = document.getElementById("hasil")
//     result.forEach(hasil => {
//         const li = document.createElement("li")
//         li.innerHTML = label[hasil.indexOf(Math.max(...hasil))] + " => " + Math.max(...hasil) * 100 + " %"
//         ol.appendChild(li)
//     })
// }

const label = ["Anomali", "Normal"]
async function predict(file) {
    file = file.files[0]
    const form = new FormData()
    form.append("file", file)
    const response = await fetch("http://localhost:5000/home", {
        method: "POST",
        body: form
    })
    const result = await response.json()
    const ol = document.getElementById("hasil")
    result.forEach(hasil => {
        const li = document.createElement("li")
        li.innerHTML = label[hasil.indexOf(Math.max(...hasil))] + " => " + Math.max(...hasil) * 100 + " %"
        ol.appendChild(li)
    })
}