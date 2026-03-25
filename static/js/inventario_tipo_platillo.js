function Impresion(id, nombre, estado) {
  $("#NameTipoPlatillo").val(nombre);
  // $("#EstadoTipoPlatillo").val(estado === "1" ? 1 : 0);
  $("#IDTipoPlatillo").val(id);

  if (estado == "1" || estado == 1) {
    $("#activoTipoConsumible").prop("checked", true);
  } else {
    $("#inactivoTipoConsumible").prop("checked", true);
  }
}

// document.getElementById("listaInventario").addEventListener(
//   "change",
//   function () {
//     window.location = this.value;
//   },
//   false,
// );

function ActualizarTipoPlatillo() {
  const nombre = $("#NameTipoPlatillo").val();
  const estado = $('input[name="estado"]:checked').val();
  const Id = $("#IDTipoPlatillo").val();

  Swal.fire({
    title: "Procesando...",
    text: "Por favor espere",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  $.ajax({
    url: "/ActualizarTipoPlatillo/",
    method: "POST",
    data: {
      Nombre: nombre,
      id: Id,
      estado: estado,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },

    success: function (response) {
      if (response.status === "ok") {
        Swal.fire({
          icon: "success",
          title: response.message,
          confirmButtonColor: "#ff6464",
        }).then(() => location.reload());
      } else {
        Swal.fire({
          icon: "warning",
          title: "Advertencia",
          text: response.message,
          confirmButtonColor: "#ff6464",
        });
      }
    },

    error: function (xhr) {
      let msg = "Ocurrió un error inesperado.";
      if (xhr.responseJSON && xhr.responseJSON.message) {
        msg = xhr.responseJSON.message;
      }

      Swal.fire({
        icon: "error",
        title: "Error",
        text: msg,
        confirmButtonColor: "#ff6464",
      });
    },
  });
}

function DarBajaImpresion(id) {
  $("#IdTipoPlatilloBaja").val(id);
}

async function DarBajaTipoPlatillo(idTipo) {
  // Confirmación inicial
  const confirmacion = await Swal.fire({
    title: "¿Realmente desea desactivar este tipo de consumible?",
    icon: "question",
    html: `
      <div style="margin-top:10px; padding:10px; background:#fff3cd; color:#856404; border-radius:6px;">
        Si desactiva un tipo de consumible, dejarán de estar disponibles en el menú
        todos aquellos consumibles relacionados.
      </div>
    `,
    iconColor: "#ff964e",
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Desactivar",
    confirmButtonColor: "#ff6464",
    reverseButtons: true,
  });

  if (!confirmacion.isConfirmed) return;

  try {
    // Modal de carga
    Swal.fire({
      title: "Procesando...",
      text: "Por favor espere",
      allowOutsideClick: false,
      didOpen: () => Swal.showLoading(),
    });

    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    // Enviar petición
    let datos = new FormData();
    datos.append("id", idTipo);
    datos.append("csrfmiddlewaretoken", token);

    let respuesta = await fetch("/DarBajaTipoPlatillo/", {
      method: "POST",
      body: datos,
    });

    let json = await respuesta.json();

    if (json.status === "ok") {
      await Swal.fire({
        title: "¡Tipo de consumible desactivado correctamente!",
        icon: "success",
        confirmButtonColor: "#ff6464",
      });
      location.reload();
    } else {
      await Swal.fire({
        title: "Error",
        text: json.message || "No se pudo realizar la acción.",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
    }
  } catch (error) {
    Swal.fire({
      title: "Error",
      text: error,
      icon: "error",
      confirmButtonColor: "#ff6464",
    });
  }
}

function Agregar_TipoPlatillo() {
  const nombre = $("#NameTipoPlatilloAgregar").val();
  const estado = $("#EstadoTipoPlatilloAgregar").val();

  Swal.fire({
    title: "Procesando...",
    text: "Por favor espere",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  $.ajax({
    url: "/AgregarTIpoPlatillo/",
    method: "POST",
    data: {
      Nombre: nombre,
      Estado: estado,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },

    success: function (response) {
      if (response.status === "ok") {
        Swal.fire({
          icon: "success",
          title: response.message,
          confirmButtonColor: "#ff6464",
        }).then(() => location.reload());
      } else {
        Swal.fire({
          icon: "warning",
          title: "Advertencia",
          text: response.message,
          confirmButtonColor: "#ff6464",
        });
      }
    },

    error: function (xhr) {
      let msg = "Ocurrió un error inesperado.";
      if (xhr.responseJSON && xhr.responseJSON.message) {
        msg = xhr.responseJSON.message;
      }

      Swal.fire({
        icon: "error",
        title: "Error",
        text: msg,
        confirmButtonColor: "#ff6464",
      });
    },
  });
}

////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", () => {
  const check = document.getElementById("checkVerTipoConsumiblesInactivos");
  const check2 = document.getElementById("checkVerTipoConsumiblesInactivos2");
  const key = "verEliminadosTipoPlatillos";

  // Restaurar estado guardado
  check.checked = localStorage.getItem(key) === "1";
  check2.checked = localStorage.getItem(key) === "1";

  // Cargar tabla al inicio
  cargarTipoPlatillos(check.checked);

  check.addEventListener("change", () => {
    localStorage.setItem(key, check.checked ? "1" : "0");

    check2.checked = check.checked;

    cargarTipoPlatillos(check.checked);
  });

  check2.addEventListener("change", () => {
    localStorage.setItem(key, check2.checked ? "1" : "0");
    
    check.checked = check2.checked;
    
    cargarTipoPlatillos(check2.checked);
  });
});

function cargarTipoPlatillos(ver) {
  document.getElementById("cuerpoInventario").style.transition = "all 0s ease";
  document.getElementById("cuerpoInventario").style.opacity = "0";

  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/FiltrarTipoPlatillos?verEliminados=" + (ver ? "1" : "0"));
  xhr.send();

  xhr.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      $(".tablaInventario").DataTable().destroy();

      const tbody = document.querySelector("#cuerpoInventario");
      tbody.innerHTML = this.responseText;

      let alto = calcularAltoTabla();

      $(".tablaInventario").DataTable({
        scrollY: alto,
        scrollCollapse: true,
        paging: true,
        language: {
          url: "/static/json/es-ES.json",
        },
      });

      setTimeout(() => {
        document.getElementById("cuerpoInventario").style.transition =
          "all .15s ease";
        document.getElementById("cuerpoInventario").style.opacity = "100%";
      }, 500);
    }
  };
}

$(window).on("resize", function () {
  let nuevoAlto = calcularAltoTabla();
  $(".dataTables_scrollBody").css("height", nuevoAlto);
  table.columns.adjust().draw();
});

function calcularAltoTabla() {
  // 1. Obtenemos el alto total de la ventana (viewport)
  let altoVentana = window.innerHeight;

  // 2. Obtenemos la distancia desde el tope de la página hasta tu tabla
  // Si la tabla no existe aún, usamos un valor por defecto
  let tablaElemento = document.querySelector(".tablaInventario");
  let offsetTop = tablaElemento
    ? tablaElemento.getBoundingClientRect().top
    : 200;

  // 3. Calculamos: Alto total - lo que ya ocupan los headers/filtros - margen de seguridad (ej. 100px)
  let altoDisponible = altoVentana - offsetTop - 250;

  // Retornamos mínimo 300px para que no desaparezca en pantallas ultra pequeñas
  return altoDisponible > 300 ? altoDisponible + "px" : "43vh";
}

/************************* E X P O R T A R **************************/

function ExportarTipoPlatillos(tipo) {
  // PETICION AL SERVICIO
  let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  let xhr = new XMLHttpRequest();

  xhr.open("GET", "/ExportarTipoPlatillo?Tipo=" + tipo, true);

  xhr.responseType = "blob";

  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", token);

  // Manejamos la respuesta del servidor
  xhr.onload = function () {
    const contentType = xhr.getResponseHeader("Content-Type");

    // Si el backend devolvió JSON (error)
    if (contentType && contentType.includes("application/json")) {
      const reader = new FileReader();

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
      // Se detecta si es excel
      if (
        contentType.includes("application/vnd.openxmlformats-officedocument") ||
        contentType.includes("application/pdf")
      ) {
        // Si es archivo → descargar
        const blob = xhr.response;
        const url = window.URL.createObjectURL(blob);

        const disposition = xhr.getResponseHeader("Content-Disposition");

        let filename = "tipo_platillos.xlsx";
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

  xhr.send();
}



/** * * * * * * * * AUTO DROPDOWN * * * * * * * * * **/

const dropdown = document.getElementById("dropdownInventario");
const trigger = dropdown.querySelector(".dropdown-trigger");
const menu = dropdown.querySelector(".dropdown-menu");
const links = dropdown.querySelectorAll(".dropdown-menu a");

// Abrir cuando el botón recibe el foco (Teclado)
trigger.addEventListener("focus", () => {
  dropdown.classList.add("is-active");
});

// Cerrar si el usuario presiona la tecla Escape
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    dropdown.classList.remove("is-active");
    trigger.blur(); // Quita el foco del botón
  }
});

// Cerrar si el foco sale del menú completo (Tab fuera del último link)
dropdown.addEventListener("focusout", (e) => {
  // Si el nuevo elemento con foco NO está dentro del dropdown, cerramos
  if (!dropdown.contains(e.relatedTarget)) {
    dropdown.classList.remove("is-active");
  }
});

// Función para cerrar
const closeMenu = () => {
  dropdown.classList.remove("is-active");
  trigger.setAttribute("aria-expanded", "false");
};

// Abrir al enfocar el botón
trigger.addEventListener("focus", () => {
  dropdown.classList.add("is-active");
  trigger.setAttribute("aria-expanded", "true");
});

// Manejo de teclas
dropdown.addEventListener("keydown", (e) => {
  const items = Array.from(links);
  const currentIndex = items.indexOf(document.activeElement);

  if (e.key === "ArrowDown") {
    e.preventDefault();
    // Si estamos en el botón, vamos al primer item. Si no, al siguiente.
    const nextIndex = (currentIndex + 1) % items.length;
    items[nextIndex].focus();
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    // Si estamos en el primero, vamos al último.
    const prevIndex = (currentIndex - 1 + items.length) % items.length;
    items[prevIndex].focus();
  } else if (e.key === "Escape") {
    closeMenu();
    trigger.focus();
  }
});

// Cerrar si el mouse sale o el foco se va a otro lado de la página
dropdown.addEventListener("mouseleave", closeMenu);
dropdown.addEventListener("focusout", (e) => {
  if (!dropdown.contains(e.relatedTarget)) {
    closeMenu();
  }
});