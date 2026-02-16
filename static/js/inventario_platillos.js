document.addEventListener("DOMContentLoaded", () => {
  const check = document.getElementById("checkVerConsumiblesInactivos");
  const key = "verEliminadosPlatillos";

  // Restaurar estado guardado
  check.checked = localStorage.getItem(key) === "1";

  // Cargar tabla al inicio
  cargarPlatillos(check.checked);

  check.addEventListener("change", () => {
    localStorage.setItem(key, check.checked ? "1" : "0");
    cargarPlatillos(check.checked);
  });
});

// document.getElementById("listaInventario").addEventListener(
//   "change",
//   function () {
//     window.location = this.value;
//   },
//   false,
// );

function cargarPlatillos(ver) {
  document.getElementById("cuerpoInventario").style.opacity = "0";

  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/FiltrarPlatillos?verEliminados=" + (ver ? "1" : "0"));
  xhr.send();

  xhr.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      $(".tablaInventario").DataTable().destroy();

      const tbody = document.querySelector("#cuerpoInventario");
      tbody.innerHTML = this.responseText;

      $(".tablaInventario").DataTable({
        scrollY: "43vh",
        scrollCollapse: false,
        paging: true,
        language: {
          url: "/static/json/es-ES.json",
        },
      });

      setTimeout(() => {
        document.getElementById("cuerpoInventario").style.opacity = "100%";
      }, 500);
    }
  };
}

//////////////////////////////////////////////////////////////////////////

var btnAgregar = document.getElementById("agregar");

// Agrega el event listener al elemento
btnAgregar.addEventListener("click", function () {
  let campoArchivo = document.getElementById("iconoCargarImagen");
  let spanArchivo = document.getElementById("SpanLabel");

  campoArchivo.value = "";
  spanArchivo.textContent = "Cargar imagen";

  VerificarArchivo(campoArchivo);
});

function soloNumeros(event) {
  var charCode = event.which ? event.which : event.keyCode;

  // Permitir números del 0 al 9, el punto decimal y la tecla de retroceso
  if ((charCode >= 48 && charCode <= 57) || charCode === 46 || charCode === 8) {
    // Verificar que no se ingresen múltiples puntos decimales
    if (charCode === 46 && event.target.value.indexOf(".") !== -1) {
      event.preventDefault();
      return false;
    }
    return true;
  }

  event.preventDefault();
  return false;
}

/**********************************************************/

function Impresion(
  id,
  nombre,
  tipoPlatillo,
  idTipoPLatillo,
  precio,
  estado,
  descripcion,
) {
  $("#IDPlatillo").val(id);
  $("#NombrePlatillo").val(nombre);
  $("#TipoPlatillo").val(tipoPlatillo);
  $("#PrecioPlatillo").val(precio);
  $("#DescripcionPlatillo").val(descripcion);
  $("#TipoPlatillo").val(idTipoPLatillo);
  
  if (estado == "1")
    $("#switch-estado #activo").checked = true;
  else
    $("#switch-estado #inactivo").checked = true;
}

function ActualizarPlatillo() {
  const formData = new FormData();
  formData.append("id", $("#IDPlatillo").val());
  formData.append("Nombre", $("#NombrePlatillo").val());
  formData.append("tipoplatillo", $("#TipoPlatillo").val());
  formData.append("Precio", parseFloat($("#PrecioPlatillo").val()));
  formData.append("estado", $("#EstadoPlatillo").val());
  formData.append("Descripcion", $("#DescripcionPlatillo").val());
  formData.append("Imagen", $("#archivoModal_dos")[0].files[0]);
  formData.append(
    "csrfmiddlewaretoken",
    $("input[name=csrfmiddlewaretoken]").val(),
  );

  $.ajax({
    url: "/ActualizarPlatillos/",
    method: "POST",
    data: formData,
    processData: false,
    contentType: false,

    success: function (response) {
      if (response.status === "ok") {
        Swal.fire({
          icon: "success",
          title: response.message || "¡Consumible modificado exitosamente!",
          confirmButtonColor: "#ff6464",
        }).then(() => location.reload());
      } else {
        Swal.fire({
          icon: "error",
          title: "Error",
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

async function DarBaja_Platillo(idPlatillo) {
  // Confirmación
  const confirmacion = await Swal.fire({
    title: "¿Realmente desea desactivar este consumible?",
    icon: "question",
    iconColor: "#ff964e",
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Desactivar",
    confirmButtonColor: "#ff6464",
    reverseButtons: true,
  });

  if (!confirmacion.isConfirmed) return;

  try {
    // Cargando...
    Swal.fire({
      title: "Procesando...",
      text: "Por favor espere",
      allowOutsideClick: false,
      didOpen: () => Swal.showLoading(),
    });

    // Enviar AJAX
    const token = document.querySelector(
      "input[name='csrfmiddlewaretoken']",
    ).value;

    const response = await fetch("/DarBajaPlatillo/", {
      method: "POST",
      headers: {
        "X-CSRFToken": token,
      },
      body: new URLSearchParams({
        id: idPlatillo,
      }),
    });

    const data = await response.json();

    if (data.status === "ok") {
      await Swal.fire({
        title: data.message || "¡Consumible desactivado exitosamente!",
        icon: "success",
        confirmButtonColor: "#ff6464",
      });
      location.reload();
    } else {
      await Swal.fire({
        title: "Error",
        text: data.message || "No se pudo desactivar el consumible.",
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

function AgregarPlatillo() {
  const formData = new FormData();
  formData.append("Nombre", $("#NombrePlatilloAgregar").val());
  formData.append("tipoplatillo", $("#TipoPlatilloAgregar").val());
  formData.append("Precio", $("#PrecioPlatilloAgregar").val());
  formData.append("estado", $("#EstadoPlatilloAgregar").val());
  formData.append("Descripcion", $("#DescripcionPlatilloAgregar").val());
  formData.append("Imagen", $("#iconoCargarImagen")[0].files[0]);
  formData.append(
    "csrfmiddlewaretoken",
    $("input[name=csrfmiddlewaretoken]").val(),
  );

  $.ajax({
    url: "/AgregarPlatillo/",
    method: "POST",
    data: formData,
    processData: false,
    contentType: false,

    success: function (response) {
      if (response.status === "ok") {
        Swal.fire({
          icon: "success",
          title: response.message || "¡Consumible agregado exitosamente!",
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

function VerificarArchivo(campoArchivo) {
  let iconocargar = document.getElementById("iconoCargarImagen");
  let labelArchivo = document.getElementById("LabelArchivo");
  let spanlabel = document.getElementById("SpanLabel");

  if (!iconocargar || !spanlabel) {
    console.warn("No se encontraron los elementos necesarios.");
    return false;
  }

  if (campoArchivo.files.length > 0) {
    iconocargar.style.display = "initial";

    console.log(campoArchivo.files[0].name);
    console.log(campoArchivo.files[0]);

    spanlabel.textContent = campoArchivo.files[0].name;
    spanlabel.title = campoArchivo.files[0].name;
    return true;
  } else {
    iconocargar.style.display = "none";
    return false;
  }
}

function VerificarArchivo_dos(campoArchivo) {
  let iconocargar = document.getElementById("iconoCargarImagen_dos");
  let labelArchivo = document.getElementById("LabelArchivo_dos");
  let spanlabel = document.getElementById("SpanLabel_dos");
  if (campoArchivo.files.length > 0) {
    iconocargar.style.display = "initial";

    console.log(campoArchivo.files[0].name);
    console.log(campoArchivo.files[0]);

    spanlabel.textContent = campoArchivo.files[0].name;
    spanlabel.title = campoArchivo.files[0].name;
    return true;
  } else {
    iconocargar.style.display = "none";

    return false;
  }
}

function ExportarPlatillos(tipo) {
  // PREPARACION DE DATOS
  console.log("Exportación de tipo: " + (tipo == "1" ? "excel" : "pdf"));

  // PETICION AL SERVICIO
  let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  let xhr = new XMLHttpRequest();

  xhr.open("GET", "/ExportarPlatillo?Tipo=" + tipo, true);

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

    if (xhr.status === 200){
      // Se detecta si es excel
      if (
        contentType.includes("application/vnd.openxmlformats-officedocument") ||
        contentType.includes("application/pdf")
      ) {
        // Si es archivo → descargar
        const blob = xhr.response;
        const url = window.URL.createObjectURL(blob);

        const disposition = xhr.getResponseHeader("Content-Disposition");

        let filename = "platillos.xlsx";
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


