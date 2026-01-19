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

function agregarPlatillosIncluir(idOrden) {
  let request = new XMLHttpRequest();

  const url = `/InicioIncluir?IdOrden=${idOrden}`;

  // data.append('InputBuscarPlatillo', cadena);
  request.open("GET", url);
  request.send();
  request.onreadystatechange = function () {
    if (this.readyState == 4) {
      let contenedor = document.getElementById(
        "contenidoModalBodyIncluirPlatillosEditar",
      );

      if (contenedor) {
        contenedor.innerHTML = this.responseText;
      }
    }
  };
}

function subirCantidad(id) {
  const span = document.getElementById(`cantidadDetalle-${id}`);
  const dataFinal = document.getElementById(`detalleOrdenEditarData${id}`);
  const btnConfirmar = document.getElementById(
    `btnConfirmarCambiosEditarOrden`,
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
    `btnConfirmarCambiosEditarOrden`,
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
  $("#btnConfirmarCambiosOrden").prop("disabled", true);
  cambiosDetectados = false;
});

function confirmarQuitar(idPlatillo) {
  console.log("Quitar detalle:", idPlatillo);

  let fila = $("#filaDetalleOrdenEditar" + idPlatillo);
  let dataFinal = $("#detalleOrdenEditarData" + idPlatillo);
  let btnConfirmar = $("#btnConfirmarCambiosEditarOrden");

  btnConfirmar.prop("disabled", false);

  let esNuevo = dataFinal.data("is-new") == 1;

  if (esNuevo) {
    // Nunca existió → eliminar del DOM
    fila.addClass("quitar");

    setTimeout(() => {
      fila.remove();

      cerrarPopover();
    }, 500);
    return;
  }

  dataFinal.attr("data-es-activo", "0");

  setTimeout(() => {
    fila.hide();
  }, 500);

  cerrarPopover();
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

/* * * * * * * * *  INCLUIR CONSUMO  * * * * * * * * * * */

// Selecciona o deselecciona un platillo
$(document).on("keyup", "#buscarPlatilloEditar", function () {
  const texto = $(this).val().toLowerCase().trim();

  $("#contenidoIncluirPlatillosEditar .nombreConsumoIncluir").each(function () {
    const nombre = $(this).find(".chkPlatilloEditar").data("nombre");

    if (texto === "" || nombre.includes(texto)) {
      $(this).show();
    } else {
      $(this).hide();
    }
  });
});

// Se obtienen los platillos seleccionados
function obtenerPlatillosSeleccionadosEditar() {
  let seleccionados = [];

  $(".chkPlatilloEditar:checked").each(function () {
    const $chk = $(this);

    seleccionados.push({
      id: $chk.val(),
      nombre: $chk.data("nombre"),
      precio: parseFloat($chk.data("precio")),
    });
  });

  return seleccionados;
}

// Verifica si hay consumos seleccionados
$(document).on("change", ".chkPlatilloEditar", function () {
  const haySeleccionados = $(".chkPlatilloEditar:checked").length > 0;

  $("#btnConfirmarIncluirDetalles").prop("disabled", !haySeleccionados);
});

$("#IncluirDetalle").on("hidden.bs.modal", function () {
  $(".chkPlatilloEditar").prop("checked", false);
  $("#btnConfirmarIncluirDetalles").prop("disabled", true);
  $("#buscarPlatilloEditar").val("");
  $(".nombreConsumoIncluir").show();
});

$("#IncluirDetalle").on("hide.bs.modal", function () {
  document.getElementById("focusSink").focus();
});

$("#EditarOrden").on("hide.bs.modal", function () {
  var focusSink = document.getElementById("focusSink");

  focusSink.focus();
});

// Se ejecuta cuando da click al botón 'incluir'
$("#btnConfirmarIncluirDetalles").on("click", function () {
  const platillosSeleccionados = obtenerPlatillosSeleccionadosEditar();

  console.log("Platillos seleccionados:", platillosSeleccionados);

  platillosSeleccionados.forEach((p) => {
    // Evitar duplicados
    if ($("#filaDetalleOrdenEditar" + p.id).length === 0) {
      agregarFilaDetalleEditar(p);
    }
  });

  // Cerrar modal
  $("#IncluirDetalle").modal("hide");

  // Habilitar botón de confirmar cambios
  $("#btnConfirmarCambiosEditarOrden").prop("disabled", false);
});

function agregarFilaDetalleEditar(platillo) {
  const idOrden = $("#idOrdenEditar").val();

  const fila = `
    <tr id="filaDetalleOrdenEditar${
      platillo.id
    }" class="filaDetalleOrden filaDetalleOrdenNuevo">
      <td style="text-transform: capitalize; padding-left: 10px;">
        ${platillo.nombre.toLowerCase()}
      </td>
      <td>C$${platillo.precio.toFixed(2)}</td>

      <td style="text-align: center;">
        <button class="btnControlCantidad" style="min-width: 30px;"
          onclick="bajarCantidad('${platillo.id}')">-</button>

        <span id="cantidadDetalle-${platillo.id}"
              class="cantidadConsumoEditar">1</span>

        <button class="btnControlCantidad" style="min-width: 30px;"
          onclick="subirCantidad('${platillo.id}')">+</button>
      </td>

      <td class="actions btnQuitarEditar">
        <div class="botonQuitar">
          <button type="button"
            class="btnQuitar2 btn-popover"
            data-id-detalle=""
            data-id-platillo="${platillo.id}"
            onclick="mostrarPopover(this, event)">
            Quitar
          </button>
        </div>
      </td>

      <input type="hidden"
        id="detalleOrdenEditarData${platillo.id}"
        class="detalleOrdenData${idOrden}"
        data-is-new="1"
        data-id-detalle=""
        data-id-platillo="${platillo.id}"
        data-cantidad="1"
        data-es-activo="1">
    </tr>
  `;

  $("#cuerpoTablaEditarOrdenDetalles").append(fila);
}

/* ****************************************************** */
/* ****************** EDITAR MESAS ********************** */
/* ****************************************************** */

function editarMesas(idOrden) {
  let request = new XMLHttpRequest();

  const url = `/InicioEditarMesas?IdOrden=${idOrden}`;

  // data.append('InputBuscarPlatillo', cadena);
  request.open("GET", url);
  request.send();
  request.onreadystatechange = function () {
    if (this.readyState == 4) {
      if (this.status === 200) {
        let contenedor = document.getElementById(
          "contenidoModalBodyEditarMesas",
        );

        console.log(this.responseText);

        if (contenedor) {
          contenedor.innerHTML = this.responseText;
        }
      }
    }
  };
}

$("#EditarMesas").on("shown.bs.modal", function () {
  const select = document.getElementById("selectAreaMesa");
  const btnConfirmar = document.getElementById("btnConfirmarEditarMesas");

  function filtrarMesas() {
    const areaSeleccionada = select.value;
    const mesas = document.querySelectorAll(".mesa-item");

    mesas.forEach((mesa) => {
      if (!areaSeleccionada) {
        mesa.classList.add("d-none");
        return;
      }

      if (mesa.dataset.area === areaSeleccionada) {
        mesa.classList.remove("d-none");
      } else {
        mesa.classList.add("d-none");
      }
    });

    validarSeleccion();
  }

  function validarSeleccion() {
    const areaSeleccionada = select.value;

    if (!areaSeleccionada) {
      btnConfirmar.disabled = true;
      return;
    }

    const mesasSeleccionadas = document.querySelectorAll(
      `.mesa-item[data-area="${areaSeleccionada}"] .chkMesaEditar:checked`,
    );

    btnConfirmar.disabled = mesasSeleccionadas.length === 0;
  }

  function sincronizarMesasDesdeHidden() {
    const areaId = document.getElementById("ValorIdAreaMesaOrdenEditar").value;

    const mesasIdsStr = document.getElementById(
      "ValorIdMesasOrdenEditar",
    ).value;

    const mesasIds = mesasIdsStr ? mesasIdsStr.split(",") : [];

    const selectArea = document.getElementById("selectAreaMesa");

    // Seleccionar área
    selectArea.value = areaId;

    // Resetear todas las mesas
    document.querySelectorAll(".chkMesaEditar").forEach((cb) => {
      cb.checked = false;
    });

    // Marcar solo mesas del área seleccionada
    document.querySelectorAll(".mesa-item").forEach((label) => {
      const perteneceArea = label.dataset.area === areaId;
      const idMesa = label.dataset.idmesa;

      if (perteneceArea && mesasIds.includes(idMesa)) {
        const checkbox = label.querySelector(".chkMesaEditar");
        checkbox.checked = true;
      }
    });

    // Mostrar solo las mesas del área
    filtrarMesas();
  }

  // Eventos
  select.addEventListener("change", filtrarMesas);

  document.addEventListener("change", function (e) {
    if (e.target.classList.contains("chkMesaEditar")) {
      validarSeleccion();
    }
  });

  // Ejecutar al abrir
  sincronizarMesasDesdeHidden();

  document
    .getElementById("btnConfirmarEditarMesas")
    .addEventListener("click", confirmarMesas);
});

// document
//   .getElementById("btnConfirmarEditarMesas")
//   .addEventListener("click", function () {
//     const select = document.getElementById("selectAreaMesa");
//     const areaId = select.value;
//     const areaNombre = select.options[selectArea.selectedIndex].text;

//     const inputArea = document.getElementById("ValorIdAreaMesaOrdenEditar");
//     const inputMesas = document.getElementById("ValorIdMesasOrdenEditar");

//     const inputAreaVisible = document.getElementById("NombreAreaMesaOrden");
//     const inputMesasVisible = document.getElementById("MesasOrden");

//     const areaSeleccionada = select.value;

//     if (!areaSeleccionada) return;

//     // Guardar área
//     inputArea.value = areaSeleccionada;
//     inputAreaVisible.value = areaNombre;

//     // Obtener mesas seleccionadas SOLO del área actual
//     const mesasSeleccionadas = document.querySelectorAll(
//       `.mesa-item[data-area="${areaSeleccionada}"] .chkMesaEditar:checked`,
//     );

//     const idsMesas = Array.from(mesasSeleccionadas).map((cb) => cb.value);

//     // Guardar mesas separadas por coma
//     inputMesas.value = idsMesas.join(",");

//     // Cerrar modal
//     $("#EditarMesas").modal("hide");
//   });

function confirmarMesas() {
  const areaSeleccionada = document.getElementById("selectAreaMesa").value;

  const checkboxes = document.querySelectorAll(".chkMesaEditar");

  const idsMesas = [];
  const numerosMesas = [];

  checkboxes.forEach((cb) => {
    if (!cb.checked) return;

    const label = cb.closest(".mesa-item");

    // 👉 VALIDACIÓN CLAVE: solo mesas del área seleccionada
    if (label.dataset.area !== areaSeleccionada) return;

    idsMesas.push(label.dataset.idmesa);
    numerosMesas.push("#" + label.dataset.numero);
  });

  // Seguridad extra (por si acaso)
  if (idsMesas.length === 0) {
    alert("Debes seleccionar al menos una mesa del área seleccionada.");
    return;
  }

  // Hidden inputs (para backend)
  document.getElementById("ValorIdAreaMesaOrdenEditar").value =
    areaSeleccionada;
  document.getElementById("ValorIdMesasOrdenEditar").value = idsMesas.join(",");

  // Inputs visibles
  document.getElementById("MesasOrden").value = numerosMesas.join(" - ");

  const areaTexto = document.querySelector(
    "#selectAreaMesa option:checked",
  ).text;

  document.getElementById("NombreAreaMesaOrden").value = areaTexto;

  $("#EditarMesas").modal("hide");
}