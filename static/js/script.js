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

async function readFile(input) {
    // const label = ["Dos", "Probe", "R2L", "U2R", "normal"]
    const label = ["normal", "anomali"]
    let file = input.files[0];
    let reader = new FileReader();
    reader.readAsText(file);
    reader.onload = function () {
        let text = reader.result;
        let lines = text.split("\n");
        let data = [];
        for (let i = 0; i < lines.length - 1; i++) {
            data.push(lines[i].split(","));
        }
        let table = document.getElementById("tabel_hasil");
        let tbody = table.getElementsByTagName("tbody")[0];
        tbody.innerHTML = "";
        for (let i = 1; i < data.length; i++) {
            let row = tbody.insertRow();
            for (let j = 0; j < 8; j++) {
                if (j == 5) {
                    let cell = row.insertCell();
                    cell.innerHTML = "...";
                } else if (j == 7) {
                    let cell = row.insertCell();
                    cell.innerHTML = "Progress...";
                } else if (j == 6) {
                    let cell = row.insertCell();
                    cell.innerHTML = label[parseInt(data[i][44])];
                } else {
                    let cell = row.insertCell();
                    cell.innerHTML = data[i][j + 1];
                }
            }
        }
    };
    reader.onerror = function () {
        console.log(reader.error);
    };
    const formData = new FormData();
    formData.append('file', file);
    const predict = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
    });
    const result = await predict.json();
    let tbody = document.getElementById("tabel_hasil").getElementsByTagName("tbody")[0];
    console.log(result)
    result.forEach((element, index) => {
        let row = tbody.rows[index];
        let cell = row.cells[7];
        console.log(element)
        console.log(element < 0.8)
        cell.innerHTML = label[element[0] < 0.0001 ? 0 : 1];
        // cell.innerHTML = element[0] < 0.4 ? 0 : 1;
    })
}