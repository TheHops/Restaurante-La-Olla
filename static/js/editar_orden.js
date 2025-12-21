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
  const cantidadFinal = document.getElementById(`cantidadDetalleOrdenEditar${idDetalle}`);
  const btnConfirmar = document.getElementById(`btnConfirmarCambiosEditarOrden`);
  
  if (!span) return;

  let cantidad = parseInt(span.textContent) || 1;
  cantidad++;

  $("#EditarOrden").trigger("input");

  btnConfirmar.disabled = false;
  cantidadFinal.value = cantidad;
  span.textContent = cantidad;
}

function bajarCantidad(idDetalle) {
  const span = document.getElementById(`cantidadDetalle-${idDetalle}`);
  const cantidadFinal = document.getElementById(`cantidadDetalleOrdenEditar${idDetalle}`);
  const btnConfirmar = document.getElementById(`btnConfirmarCambiosEditarOrden`);

  if (!span) return;

  let cantidad = parseInt(span.textContent) || 1;

  if (cantidad > 1) {
    cantidad--;
  }

  $("#EditarOrden").trigger("input");

  btnConfirmar.disabled = false;
  cantidadFinal.value = cantidad;
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
  let estadoFinal = $("#esActivoDetalleOrdenEditar" + idDetalle);
  let btnConfirmar = $("#btnConfirmarCambiosEditarOrden");

  btnConfirmar.prop("disabled", false);

  detalle.addClass("quitar");
  estadoFinal.val("0");

  setTimeout(() => {
    detalle.hide();
  }, 500);
}

async function ConfirmarEditarOrden() {
  const { value: isConfirmed } = await Swal.fire({
    title: "¿Los cambios están correctos?",
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Confirmar",
    confirmButtonColor: "#ff6464",
    icon: "question",
    iconColor: "#ff964e",
    reverseButtons: true,
  });

  if (isConfirmed) {
    try {
      // Muestra un modal de carga mientras se envían los datos
      Swal.fire({
        title: "Editando orden...",
        text: "Por favor espere",
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading(),
      });

      const respuesta = await enviarDatosEditar();

      // Supongamos que Django responde con algo como:
      // { "status": "ok", "message": "Orden creada exitosamente" }

      if (respuesta.status === "ok") {
        await Swal.fire({
          title: respuesta.message,
          icon: "success",
          confirmButtonColor: "#ff6464",
        });
        location.reload();
      } else {
        await Swal.fire({
          title: "Error",
          text: respuesta.message || "No se pudo editar la orden.",
          icon: "error",
          confirmButtonColor: "#ff6464",
        });
      }
    } catch (error) {
      await Swal.fire({
        title: "Error",
        text: error,
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
    }
  }
}

function enviarDatosEditar() {
  console.log("ENTRA A CONFIRMAR EDITAR");
}