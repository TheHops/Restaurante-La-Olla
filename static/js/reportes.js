const fechaDesde = document.getElementById("fechaDesde");
const fechaHasta = document.getElementById("fechaHasta");
const errorFechas = document.getElementById("errorFechas");
const listaEstado = document.getElementById("listaEstadoOrdenesExportar");
const btnAplicarFiltros = document.getElementById("btnAplicarFiltrosOrdenes");

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
  verificarFilasTabla();
});

function inicializarFechas()
{
  const hoy = new Date();
  const yyyy = hoy.getFullYear();
  const mm = String(hoy.getMonth() + 1).padStart(2, "0");
  const dd = String(hoy.getDate()).padStart(2, "0");
  
  fechaDesde.value = `${yyyy}-${mm}-${dd}`;
  fechaHasta.value = `${yyyy}-${mm}-${dd}`;

  filtrosAplicados.fechaDesde = fechaDesde.value;
  filtrosAplicados.fechaHasta = fechaHasta.value;

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
  filtrosAplicados.fechaPredefinida = null;
  filtrosAplicados.fechaDesde = fechaDesde.value;
  filtrosTemp.fechaDesde = fechaDesde.value;

  document
    .querySelectorAll('input[name="fecha"]')
    .forEach((r) => (r.checked = false));

  actualizarIndicadorFiltros();

  if (validarFechas())
  {
    btnAplicarFiltros.disabled = false;
    filtrarOrdenesFecha();
  }
  else btnAplicarFiltros.disabled = true;
});

fechaHasta.addEventListener("change", () => {
  filtrosAplicados.fechaPredefinida = null;
  filtrosAplicados.fechaHasta = fechaHasta.value;
  filtrosTemp.fechaHasta = fechaHasta.value;

  document
    .querySelectorAll('input[name="fecha"]')
    .forEach((r) => (r.checked = false));

  actualizarIndicadorFiltros();
  
  if (validarFechas()) 
  {
    btnAplicarFiltros.disabled = false;
    filtrarOrdenesFecha();
  }
  else btnAplicarFiltros.disabled = true;
});

listaEstado.addEventListener("change", () => {
  if (validarFechas()) filtrarOrdenesFecha();
});

function rellenarParaMostrarOrden(idOrden) {
  let request = new XMLHttpRequest();

  const url = `/InicioMostrar?IdOrden=${idOrden}`;

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
  estadoAFiltrar = document.getElementById("listaEstadoOrdenesExportar");

  console.log("ESTADO");
  console.log(estadoAFiltrar.value);
  
  const params = new URLSearchParams({
    FechaInicio: fechaDesde.value,
    FechaFin: fechaHasta.value,
    Estado: estadoAFiltrar.value
  });

  const areasSeleccionadas = filtrosAplicados.areas;
  const areasParam = areasSeleccionadas.join(",");

  const xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `/ReportesOrdenesFiltradas?${params.toString()}&AreasSeleccionadas=${encodeURIComponent(
      areasParam
    )}`,
    true
  );

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      $(".tablaInventario").DataTable().destroy();
      document.querySelector("#cuerpoInventario").innerHTML = this.responseText;

      $(".tablaInventario").DataTable({
        scrollY: "43vh",
        paging: true,
        language: { url: "/static/json/es-ES.json" },
      });

      verificarFilasTabla();
    }
  };

  xhr.send();
}

function obtenerAreasSeleccionadas() {
  const checkboxes = document.querySelectorAll(
    '#areasBusqueda input[type="checkbox"]:checked'
  );
  const areasSeleccionadas = Array.from(checkboxes).map(
    (checkbox) => checkbox.value
  );

  return areasSeleccionadas;
}

/****************************************************************************/
/****************************************************************************/
/****************************************************************************/

let filtrosAplicados = {
  fechaPredefinida: null,
  areas: [],
  fechaDesde: null,
  fechaHasta: null,
};

let filtrosTemp = {
  fechaPredefinida: null,
  areas: [],
  fechaDesde: null,
  fechaHasta: null,
};

// Funcion que verifica si hay algún filtro seleccionado
function hayFiltrosActivos() {
  return (
    filtrosAplicados.fechaPredefinida !== null ||
    filtrosAplicados.areas.length > 0
  );
}

function hayFiltrosActivosTemp() {
  return (
    filtrosTemp.fechaPredefinida !== null ||
    filtrosTemp.areas.length > 0
  );
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

function aplicarFechaPredefinidaTemp(tipo) {
  const hoy = new Date();
  let desde, hasta;

  hasta = new Date(hoy);

  switch (tipo) {
    case "1":
      desde = new Date(hoy);
      break;
    case "2":
      desde = new Date(hoy);
      desde.setDate(hoy.getDate() - 1);
      hasta = new Date(desde);
      break;
    case "3":
      desde = new Date(hoy);
      desde.setDate(hoy.getDate() - 7);
      break;
    case "4":
      desde = new Date(hoy);
      desde.setDate(hoy.getDate() - 15);
      break;
    case "5":
      desde = new Date(hoy);
      desde.setDate(hoy.getDate() - 30);
      break;
  }

  // filtrosTemp.fechaDesde = desde.toISOString().split("T")[0];
  // filtrosTemp.fechaHasta = hasta.toISOString().split("T")[0];

  filtrosTemp.fechaDesde = formatLocalDate(desde);
  filtrosTemp.fechaHasta = formatLocalDate(hasta);

  // fechaDesde.value = filtrosTemp.fechaDesde;
  // fechaHasta.value = filtrosTemp.fechaHasta;
}

function formatLocalDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}


document.querySelectorAll('input[name="fecha"]').forEach((radio) => {
  radio.addEventListener("change", function () {
    filtrosTemp.fechaPredefinida = this.value;
    aplicarFechaPredefinidaTemp(this.value);

    // document.querySelector("#btnAplicarFiltros").disabled = !hayFiltrosActivosTemp();
  });
});

document.querySelectorAll('input[name="areas[]"]').forEach((check) => {
  check.addEventListener("change", function () {
    filtrosTemp.areas = Array.from(
      document.querySelectorAll('input[name="areas[]"]:checked')
    ).map((el) => el.value);

    // document.querySelector("#btnAplicarFiltros").disabled = !hayFiltrosActivosTemp();
  });
});

$("#FiltrarOrdenes").on("shown.bs.modal", function () {
  // Clonar filtros aplicados → temporales
  filtrosTemp = JSON.parse(JSON.stringify(filtrosAplicados));

  // Restaurar radios
  document.querySelectorAll('input[name="fecha"]').forEach((r) => {
    r.checked = r.value === filtrosTemp.fechaPredefinida;
  });

  // Restaurar áreas
  document.querySelectorAll('input[name="areas[]"]').forEach((check) => {
    check.checked = filtrosTemp.areas.includes(check.value);
  });

  // document.querySelector("#btnAplicarFiltros").disabled = !hayFiltrosActivos();
});

document
  .getElementById("btnAplicarFiltros")
  .addEventListener("click", function () {
    if (!validarFechas()) return;

    // Commit
    filtrosAplicados = JSON.parse(JSON.stringify(filtrosTemp));

    // Aplicar fechas definitivas
    fechaDesde.value = filtrosAplicados.fechaDesde || "";
    fechaHasta.value = filtrosAplicados.fechaHasta || "";

    filtrarOrdenesFecha();

    actualizarIndicadorFiltros();

    $("#FiltrarOrdenes").modal("hide");
  });

/**************************************************************/
/**************************************************************/
/**************************************************************/

function ExportarOrdenes(tipo)
{
  estadoAFiltrar = document.getElementById("listaEstadoOrdenesExportar");

  Swal.fire({
    toast: true,
    position: "top-start",
    title: "Procesando...",
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();
    },
  });

  // PREPARACION DE DATOS
  console.log("Exportación de tipo: " + (tipo == "1" ? "excel" : "pdf"));

  const payload = {
    FechaInicio: fechaDesde.value,
    FechaFin: fechaHasta.value,
    AreasSeleccionadas: filtrosAplicados.areas,
    TipoExportacion: tipo,
    IncluirDetalles: false,
    Estado: estadoAFiltrar.value
  };

  let incluirDetalle = document.getElementById("check_incluir_detalles");
  payload.IncluirDetalles = incluirDetalle.checked;

  console.log("Incluir detalles : " + incluirDetalle.checked) ;

  // PETICION AL SERVICIO
  let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  let xhr = new XMLHttpRequest();

  xhr.open("POST", "/ExportarOrdenes/", true);

  xhr.responseType = "blob";

  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", token);

  // Manejamos la respuesta del servidor
  xhr.onload = function () {
    const contentType = xhr.getResponseHeader("Content-Type");
    
    // Si el backend devolvió JSON (error)
    if (contentType && contentType.includes("application/json")) {
      const reader = new FileReader();
      
      console.log("ES JSON");

      reader.onload = function () {
        try {
          const respuesta = JSON.parse(reader.result);
          Swal.fire({
            title: respuesta.message || "Error inesperado",
            icon: respuesta.status === "error" ? "error" : "success",
            confirmButtonColor: "#ff6464",
          });
        } catch (e) {
          Swal.fire({
            title: "Error",
            text: "Respuesta inválida del servidor",
            icon: "error",
          });
        }
      };

      reader.readAsText(xhr.response);
      return;
    }
    
    if (xhr.status === 200) {
      if (
        contentType.includes("application/vnd.openxmlformats-officedocument") ||
        contentType.includes("application/pdf")
      ) {
        // Si es archivo → descargar
        const blob = xhr.response;
        const url = window.URL.createObjectURL(blob);

        const disposition = xhr.getResponseHeader("Content-Disposition");

        let filename = "ordenes.xlsx";
        if (disposition && disposition.includes("filename=")) {
          filename = disposition.split("filename=")[1].replace(/"/g, "").trim();
        }

        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();

        window.URL.revokeObjectURL(url);
      }

      Swal.fire({
        icon: "success",
        title: "¡Se exportó el archivo con éxito!",
        toast: true,
        position: "top-start",
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: false,
      });
    } else {
      Swal.fire({
        title: "Error al exportar",
        text: "Error de servidor: " + xhr.status,
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
    }
  };

  xhr.onerror = function () {
    Swal.fire({
      title: "Error",
      text: "No se pudo conectar con el servidor",
      icon: "error",
      confirmButtonColor: "#ff6464",
    });
  };

  xhr.send(JSON.stringify(payload));
}

function verificarFilasTabla() {
  const tbody = document.querySelector(".tablaInventario tbody");
  const filas = tbody.querySelectorAll("tr");
  const btnExportar = document.getElementById("btnExportarOrdenes");

  if (filas.length > 0) {
    btnExportar.disabled = false;
  } else {
    btnExportar.disabled = true;
  }
}


