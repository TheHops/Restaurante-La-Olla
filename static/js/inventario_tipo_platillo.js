function Impresion(id, nombre, estado) {
  $("#NameTipoPlatillo").val(nombre);
  $("#EstadoTipoPlatillo").val(estado === "1" ? 1 : 0);
  $("#IDTipoPlatillo").val(id);
}

document.getElementById("listaInventario").addEventListener(
  "change",
  function () {
    window.location = this.value;
  },
  false
);

function ActualizarTipoPlatillo() {
  const nombre = $("#NameTipoPlatillo").val();
  const estado = $("#EstadoTipoPlatillo").val();
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
    title: "¿Realmente desea eliminar este tipo de consumo?",
    icon: "warning",
    iconColor: "#ff964e",
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Eliminar",
    confirmButtonColor: "#ff6464",
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
        title: "¡Tipo de consumo eliminado correctamente!",
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
  const check = document.getElementById("checkVerTipoConsumosInactivos");
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