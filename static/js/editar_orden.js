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
        contenedor.innerHTML = this.responseText;
      }
    }
  };
}

$("#EditarOrden").on("shown.bs.modal", function () {
  inicializarPopovers();
});

function inicializarPopovers() {
  $('[data-toggle="popover"]').popover({
    container: "body",
    html: true,
    trigger: "focus",
  });
}

function subirCantidad(idDetalle) {
  const span = document.getElementById(`cantidadDetalle-${idDetalle}`);
  if (!span) return;

  let cantidad = parseInt(span.textContent) || 1;
  cantidad++;

  span.textContent = cantidad;
}

function bajarCantidad(idDetalle) {
  const span = document.getElementById(`cantidadDetalle-${idDetalle}`);
  if (!span) return;

  let cantidad = parseInt(span.textContent) || 1;

  if (cantidad > 1) {
    cantidad--;
  }

  span.textContent = cantidad;
}

function mostrarPopover(btn) {
  // 1️⃣ Inicializar popover si no está inicializado
  let $btn = $(btn);

  if (!$btn.data("bs.popover")) {
    // Bootstrap 4
    $btn.popover({
      container: "body",
      html: true,
      trigger: "manual", // importante: manual para controlar con JS
      placement: "top",
      content: `
        <div class="text-center">
          <p class="mb-2">¿Quitar consumo?</p>
          <button type="button" class="btn btn-sm btn-secondary mr-1" onclick="cerrarPopover(this)">No</button>
          <button type="button" class="btn btn-sm btn-danger" onclick="confirmarQuitar(${btn.dataset.idDetalle})">Sí</button>
        </div>
      `,
    });
  }

  // 2️⃣ Mostrar el popover manualmente
  $btn.popover("show");
}

function cerrarPopover(btn) {
  $(btn).closest(".popover").prev().popover("hide");
}

function confirmarQuitar(idDetalle) {
  console.log("Quitar detalle:", idDetalle);

  // aquí tu lógica real:
  // - eliminar fila
  // - enviar AJAX
  // - marcar como inactivo
}