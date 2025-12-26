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

function agregarPlatillosIncluir(idOrden)
{
  let request = new XMLHttpRequest();

  const url = `/InicioIncluir?IdOrden=${idOrden}`;

  // data.append('InputBuscarPlatillo', cadena);
  request.open("GET", url);
  request.send();
  request.onreadystatechange = function () {
    if (this.readyState == 4) {
      let contenedor = document.getElementById(
        "contenidoModalBodyIncluirPlatillosEditar"
      );

      if (contenedor) {
        contenedor.innerHTML = this.responseText;
      }
    }
  };
}

function subirCantidad(id) {
  const span = document.getElementById(`cantidadDetalle-${id}`);
  const dataFinal = document.getElementById(
    `detalleOrdenEditarData${id}`
  );
  const btnConfirmar = document.getElementById(
    `btnConfirmarCambiosEditarOrden`
  );

  if (!span) return;

  let cantidad = parseInt(span.textContent) || 1;
  cantidad++;

  $("#EditarOrden").trigger("input");

  btnConfirmar.disabled = false;

  dataFinal.dataset.cantidad = cantidad;

  span.textContent = cantidad;
}

function bajarCantidad(id) {
  console.log("Subir cantidad detalle existente");

  const span = document.getElementById(`cantidadDetalle-${id}`);
  const dataFinal = document.getElementById(`detalleOrdenEditarData${id}`);
  const btnConfirmar = document.getElementById(
    `btnConfirmarCambiosEditarOrden`
  );

  if (!span) return;

  let cantidad = parseInt(span.textContent) || 1;

  if (cantidad > 1) {
    cantidad--;
  }

  $("#EditarOrden").trigger("input");

  btnConfirmar.disabled = false;

  dataFinal.dataset.cantidad = cantidad;

  span.textContent = cantidad;
}

/*///////////////////////////// POPOVER /////////////////////////////////*/

$("#EditarOrden").on("hidden.bs.modal", function () {
  destruirPopovers();
});

/* Mostrar popovers */

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
          <button type="button" class="btn btn-sm btn-danger" onclick="confirmarQuitar(${btn.dataset.idPlatillo})">Sí</button>
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
    $("#btnConfirmarCambiosEditarOrden").prop("disabled", false);
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

  let detalle = $("#filaDetalleOrdenEditar" + idDetalle);
  const dataFinal = $("#detalleOrdenEditarData" + idDetalle);
  let btnConfirmar = $("#btnConfirmarCambiosEditarOrden");

  btnConfirmar.prop("disabled", false);

  detalle.addClass("quitar");

  dataFinal.attr("data-es-activo", "0");

  setTimeout(() => {
    detalle.hide();
  }, 500);
}

async function ConfirmarEditarOrden(idOrden) {
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

      const respuesta = await enviarDatosEditar(idOrden);

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

function enviarDatosEditar(idOrden) {
  console.log("ENTRA A CONFIRMAR EDITAR");

  let descripcionElement = document.getElementById("descripcionOrdenEditar");

  let detalles = document.querySelectorAll(".detalleOrdenData" + idOrden);

  console.log(descripcionElement);

  console.log(detalles);

  // Estructura base
  const payload = {
    idOrden: parseInt(idOrden),
    descripcion: descripcionElement.value,
    detalles: [],
  };

  detalles.forEach((el) => {
    const isNew = el.dataset.isNew === "1";

    const detalle = {
      idDetalle: el.dataset.idDetalle || null,
      idPlatillo: el.dataset.idPlatillo,
      cantidad: parseInt(el.dataset.cantidad),
      esActivo: el.dataset.esActivo,
      isNew: isNew,
    };

    payload.detalles.push(detalle);
  });

  console.log("PAYLOAD FINAL:", payload);

  /* Se realiza la petición al backend */

  return new Promise((resolve, reject) => {
    let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/EditarOrden/", true);

    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", token);

    // Manejamos la respuesta del servidor
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          try {
            let respuesta = JSON.parse(xhr.responseText);
            resolve(respuesta); // se devuelve el resultado al .then()
          } catch (e) {
            reject("Error al procesar la respuesta del servidor.");
          }
        } else {
          reject("Error de red o servidor: " + xhr.status);
        }
      }
    };

    xhr.onerror = function () {
      reject("Error al conectar con el servidor.");
    };

    xhr.send(JSON.stringify(payload));
  });
}