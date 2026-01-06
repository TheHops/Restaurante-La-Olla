const fechaDesde = document.getElementById("fechaDesde");
const fechaHasta = document.getElementById("fechaHasta");
const errorFechas = document.getElementById("errorFechas");

function validarFechas() {
  if (!fechaDesde.value || !fechaHasta.value) {
    errorFechas.style.display = "none";
    return false;
  }

  const desde = new Date(fechaDesde.value);
  const hasta = new Date(fechaHasta.value);

  if (desde > hasta) {
    errorFechas.style.display = "block";
    fechaHasta.setCustomValidity("Fecha inválida");
    return false;
  }

  errorFechas.style.display = "none";
  fechaHasta.setCustomValidity("");
  return true;
}

fechaDesde.addEventListener("change", () => {
  if(validarFechas()) filtrarOrdenesFecha();
});
fechaHasta.addEventListener("change", () => {
  if (validarFechas()) filtrarOrdenesFecha();
});

function rellenarParaMostrarOrden(idOrden) {
  let request = new XMLHttpRequest();

  const url = `/InicioMostrar?IdOrden=${idOrden}`;

  // data.append('InputBuscarPlatillo', cadena);
  request.open("GET", url);
  request.send();
  request.onreadystatechange = function () {
    if (this.readyState == 4) {
      let contenedor = document.getElementById("contenidoDetalleOrden");

      if (contenedor) {
        destruirPopovers();
        contenedor.innerHTML = this.responseText;
      }
    }
  };
}

function filtrarOrdenesFecha(){
  console.log("FECHA VALIDA");

  console.log("Desde " + fechaDesde.value);
  console.log("Hasta " + fechaHasta.value);
}
