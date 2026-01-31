function InicioForgotPassword() {
  var contenedor = document.getElementById("derecha");

  contenedor.classList.add("hide");

  let request = new XMLHttpRequest();

  const url = `/ForgotPassword`;

  // data.append('InputBuscarPlatillo', cadena);
  request.open("GET", url);
  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status === 200) {
        console.log("INICIO FORGOT AFTER GET");
        
        setTimeout(() => {
            if (contenedor) {
                contenedor.innerHTML = this.responseText;
                contenedor.classList.remove("hide");
        }}, 500);
    }};

    request.send();
}
 