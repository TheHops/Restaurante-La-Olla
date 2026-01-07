const fechaDesde = document.getElementById("fechaDesde");
const fechaHasta = document.getElementById("fechaHasta");
const errorFechas = document.getElementById("errorFechas");

document.addEventListener("DOMContentLoaded", () => {
  $(".tablaInventario").DataTable({
    scrollY: "43vh",
    scrollCollapse: true,
    paging: true,
    language: {
      url: "/static/json/es-ES.json",
    },
  });

  inicializarFechas();
});

function inicializarFechas()
{
  const hoy = new Date();
  const yyyy = hoy.getFullYear();
  const mm = String(hoy.getMonth() + 1).padStart(2, "0");
  const dd = String(hoy.getDate()).padStart(2, "0");
  
  fechaDesde.value = `${yyyy}-${mm}-${dd}`;
  fechaHasta.value = `${yyyy}-${mm}-${dd}`;

  filtrarOrdenesFecha();
}

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
  if (validarFechas()) filtrarOrdenesFecha();
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
        contenedor.innerHTML = this.responseText;
      }
    }
  };
}

function filtrarOrdenesFecha() {
  const fechaInicio = fechaDesde.value;
  const fechaFin = fechaHasta.value;

  const url = `/ReportesOrdenesFiltradas?FechaInicio=${encodeURIComponent(
    fechaInicio
  )}&FechaFin=${encodeURIComponent(fechaFin)}`;

  const xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        $(".tablaInventario").DataTable().destroy();

        const tbody = document.querySelector("#cuerpoInventario");
        tbody.innerHTML = this.responseText;

        $(".tablaInventario").DataTable({
          scrollY: "43vh",
          scrollCollapse: true,
          paging: true,
          language: {
            url: "/static/json/es-ES.json",
          },
        });
      } else {
        alert(xhr.message);
      }
    }
  };

  xhr.onerror = function () {
    reject("Error al conectar con el servidor.");
  };

  xhr.send();
}
