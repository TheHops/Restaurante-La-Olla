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
  actualizarIndicadorFiltros();
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
  estadoFiltros.fechaPredefinida = null;
  document
    .querySelectorAll('input[name="fecha"]')
    .forEach((r) => (r.checked = false));
  actualizarIndicadorFiltros();

  if (validarFechas()) filtrarOrdenesFecha();
});

fechaHasta.addEventListener("change", () => {
  estadoFiltros.fechaPredefinida = null;
  document
    .querySelectorAll('input[name="fecha"]')
    .forEach((r) => (r.checked = false));
  actualizarIndicadorFiltros();
  
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
  const params = new URLSearchParams({
    FechaInicio: fechaDesde.value,
    FechaFin: fechaHasta.value,
  });

  estadoFiltros.areas.forEach((id) => params.append("areas[]", id));

  const xhr = new XMLHttpRequest();
  xhr.open("GET", `/ReportesOrdenesFiltradas?${params.toString()}`, true);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      $(".tablaInventario").DataTable().destroy();
      document.querySelector("#cuerpoInventario").innerHTML = this.responseText;

      $(".tablaInventario").DataTable({
        scrollY: "43vh",
        paging: true,
        language: { url: "/static/json/es-ES.json" },
      });
    }
  };

  xhr.send();
}

/****************************************************************************/
/****************************************************************************/
/****************************************************************************/

// Funcion que verifica si hay algún filtro seleccionado
function hayFiltrosActivos() {
  const hayFecha = estadoFiltros.fechaPredefinida !== null;
  const hayAreas = estadoFiltros.areas.length > 0;

  return hayFecha || hayAreas;
}

// Agrega un indicador para decir que hay un filtro aplicado
function actualizarIndicadorFiltros() {
  const indicador = document.getElementById("indicadorFiltros");

  if (hayFiltrosActivos()) {
    indicador.style.display = "inline-block";
  } else {
    indicador.style.display = "none";
  }
}

let estadoFiltros = {
  fechaPredefinida: null,
  areas: [],
};

document.querySelectorAll('input[name="fecha"]').forEach((radio) => {
  radio.addEventListener("change", function () {
    estadoFiltros.fechaPredefinida = this.value;
    aplicarFechaPredefinida(this.value, false);
    actualizarIndicadorFiltros();
  });
});

function aplicarFechaPredefinida(tipo, filtrar = true) {
  const hoy = new Date();
  let desde, hasta;

  hasta = new Date(hoy);

  switch (tipo) {
    case "1": // Hoy
      desde = new Date(hoy);
      break;

    case "2": // Ayer
      desde = new Date(hoy);
      desde.setDate(hoy.getDate() - 1);
      hasta = new Date(desde);
      break;

    case "3": // Últimos 7 días
      desde = new Date(hoy);
      desde.setDate(hoy.getDate() - 7);
      break;

    case "4": // Últimos 15 días
      desde = new Date(hoy);
      desde.setDate(hoy.getDate() - 15);
      break;

    case "5": // Últimos 30 días
      desde = new Date(hoy);
      desde.setDate(hoy.getDate() - 30);
      break;
  }

  fechaDesde.value = desde.toISOString().split("T")[0];
  fechaHasta.value = hasta.toISOString().split("T")[0];

  if (filtrar){
    filtrarOrdenesFecha();
  }
}

document.querySelectorAll('input[name="areas[]"]').forEach((check) => {
  check.addEventListener("change", function () {
    estadoFiltros.areas = Array.from(
      document.querySelectorAll('input[name="areas[]"]:checked')
    ).map((el) => el.value);

    actualizarIndicadorFiltros();
  });
});

$("#FiltrarOrdenes").on("shown.bs.modal", function () {
  // Restaurar radio
  document.querySelectorAll('input[name="fecha"]').forEach((r) => {
    r.checked = r.value === estadoFiltros.fechaPredefinida;
  });

  // Áreas
  document.querySelectorAll('input[name="areas[]"]').forEach((check) => {
    check.checked = estadoFiltros.areas.includes(check.value);
  });
});

document
  .getElementById("btnAplicarFiltros")
  .addEventListener("click", function () {
    // Validar fechas si existen
    if (!validarFechas()) return;

    filtrarOrdenesFecha();

    $("#FiltrarOrdenes").modal("hide");
  });






