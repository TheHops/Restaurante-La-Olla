function Impresion(id, nombre, estado) {
  $("#NameTipoPlatillo").val(nombre);
  // $("#EstadoTipoPlatillo").val(estado === "1" ? 1 : 0);
  $("#IDTipoPlatillo").val(id);

  if (estado == "1" || estado == 1) {
    $("#activo").prop("checked", true);
  } else {
    $("#inactivo").prop("checked", true);
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
  const key = "verEliminadosTipoPlatillos";

  // Restaurar estado guardado
  check.checked = localStorage.getItem(key) === "1";

  // Cargar tabla al inicio
  cargarTipoPlatillos(check.checked);

  check.addEventListener("change", () => {
    localStorage.setItem(key, check.checked ? "1" : "0");
    cargarTipoPlatillos(check.checked);
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

      $(".tablaInventario").DataTable({
        scrollY: "43vh",
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

/************************* E X P O R T A R **************************/

function ExportarTipoPlatillos(tipo) {
  // PREPARACION DE DATOS
  console.log("Exportación de tipo: " + (tipo == "1" ? "excel" : "pdf"));

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

    console.log(contentType);

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