function rellenarParaEditarOrden(idOrden) {
  let request = new XMLHttpRequest();

  const url = `/InicioEditar?IdOrden=${idOrden}`;

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

function subirCantidad(idDetalle) {
  const span = document.getElementById(`cantidadDetalle-${idDetalle}`);
  if (!span) return;

  let cantidad = parseInt(span.textContent) || 1;
  cantidad++;

  $("#EditarOrden").trigger("input");

  span.textContent = cantidad;
}

function bajarCantidad(idDetalle) {
  const span = document.getElementById(`cantidadDetalle-${idDetalle}`);
  if (!span) return;

  let cantidad = parseInt(span.textContent) || 1;

  if (cantidad > 1) {
    cantidad--;
  }

  $("#EditarOrden").trigger("input");

  span.textContent = cantidad;
}

/*///////////////////////////// POPOVER /////////////////////////////////*/

$("#EditarOrden").on("hidden.bs.modal", function () {
  destruirPopovers();
});

function mostrarPopover(btn, e) {
  if (e) e.stopPropagation();

  $(".btn-popover").popover("hide");

  const $btn = $(btn);

  if (!$btn.data("bs.popover")) {
    $btn.popover({
      container: "#EditarOrden",
      html: true,
      trigger: "manual",
      placement: "top",
      sanitize: false,
      content: `
        <div class="text-center">
          <p class="mb-2">¿Quitar consumo?</p>
          <button type="button" class="btn btn-sm btn-secondary mr-1">No</button>
          <button type="button" class="btn btn-sm btn-danger" onclick="confirmarQuitar(${btn.dataset.idDetalle})">Sí</button>
        </div>
      `,
    });
  }

  $btn.popover("show");
}

$(document).on("mousedown", ".modal-backdrop", function () {
  $(".btn-popover").popover("hide");
});

function cerrarPopover() {
  $(".btn-popover").popover("hide");
}

function destruirPopovers() {
  $(".btn-popover").popover("dispose");
}

/*//////////////////////////////////////////////////////////////*/

let cambiosDetectados = false;

$("#EditarOrden").on("input change", "input, textarea, select", function () {
  if (!cambiosDetectados) {
    $("#btnConfirmarCambiosOrden").prop("disabled", false);
    cambiosDetectados = true;
  }
});

$("#EditarOrden").on("hidden.bs.modal", function () {
  var btnModificarOrden = document.getElementById("#btnConfirmarCambiosOrden");
  btnModificarOrden.disabled = false;
  
  $("#btnConfirmarCambiosOrden").prop("disabled", true);
  cambiosDetectados = false;
});

function confirmarQuitar(idDetalle) {
  console.log("Quitar detalle:", idDetalle);

  let detalle = $("#detalleOrdenEditar" + idDetalle);

  console.log(detalle);
  // $("#EditarOrden").trigger("input");

  detalle.addClass("quitar");

  setTimeout(() => {
    detalle.hide(); 
  }, 500);
  

  // aquí tu lógica real:
  // - eliminar fila
  // - enviar AJAX
  // - marcar como inactivo
}