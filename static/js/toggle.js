$(document).ready(function () {
  $(".modal").on("hide.bs.modal", function () {
    setTimeout(function () {
      $("#focusSink").focus();
    }, 0);
  });

  $(".modal").on("shown.bs.modal", function () {
    $(this).attr("data-uw-ignore", "true");
  });

  $(".modal").on("hidden.bs.modal", function () {
    $(this).removeAttr("data-uw-ignore");

    var $modal = $(this);

    // Mover foco a elemento seguro
    $("#focusSink").focus();

    // Limpiar todos los checkboxes y radios dentro del modal
    $modal
      .find('input[type="checkbox"], input[type="radio"]')
      .prop("checked", false);
  });
});

function confirmLogout() {
  Swal.fire({
    title: "¿Cerrar sesión?",
    text: "Tendrás que volver a ingresar tus credenciales",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#ff6464",
    confirmButtonText: "Confirmar",
    cancelButtonText: "Cancelar",
    // Esto hace que el modal se vea acorde al modo oscuro si lo usas
    background: "#fff",
    reverseButtons: true,
  }).then((result) => {
    if (result.isConfirmed) {
      // Aquí es donde Django hace su magia
      window.location.href = "/logout/";
    }
  });
}

/* ************************************************** */

function HacerBackup(tipo) {
  let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  let xhr = new XMLHttpRequest();

  // Apuntamos a la nueva ruta
  xhr.open("GET", "/Respaldo?Tipo=" + tipo, true);

  // Mantenemos blob para manejar archivos binarios y textos por igual
  xhr.responseType = "blob";

  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", token);

  Swal.fire({
    toast: true,
    position: "top-start",
    title: "Generando respaldo...",
    text: "Esto puede tomar unos segundos",
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();
    },
  });

  xhr.onload = function () {
    const contentType = xhr.getResponseHeader("Content-Type");
    const disposition = xhr.getResponseHeader("Content-Disposition");

    // 1. Verificamos si el servidor nos indica explícitamente que es un archivo adjunto
    if (
      xhr.status === 200 &&
      disposition &&
      disposition.includes("attachment")
    ) {
      const blob = xhr.response;
      const url = window.URL.createObjectURL(blob);

      // Extraemos el nombre real que viene del backend de Django
      let filename = "respaldo_la_olla";
      if (disposition.includes("filename=")) {
        filename = disposition.split("filename=")[1].replace(/"/g, "").trim();
      } else {
        // Fallback por si el backend no envía el nombre
        if (tipo === "1") filename += ".xlsx";
        if (tipo === "2") filename += ".pdf";
        if (tipo === "3") filename += ".sql";
        if (tipo === "4") filename += ".json";
      }

      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      Swal.fire({
        icon: "success",
        title: "¡Respaldo descargado!",
        toast: true,
        position: "top-start",
        showConfirmButton: false,
        timer: 4000,
      });
    }
    // 2. Si no es un archivo adjunto, pero es un JSON (posiblemente un error del backend controlado)
    else if (contentType && contentType.includes("application/json")) {
      const reader = new FileReader();

      reader.onload = function () {
        try {
          const respuesta = JSON.parse(reader.result);
          Swal.fire({
            title: respuesta.message || "Aviso del sistema",
            icon:
              respuesta.status === "error" || xhr.status !== 200
                ? "error"
                : "info",
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
      // Convertimos el blob devuelta a texto para leer el JSON de error
      reader.readAsText(xhr.response);
    }
    // 3. Cualquier otro error del servidor (Ej: 500 Internal Server Error)
    else {
      Swal.fire({
        title: "Error al generar",
        text: "Código de error: " + xhr.status,
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
    }
  };

  xhr.onerror = function () {
    Swal.fire({
      title: "Error de conexión",
      text: "No se pudo conectar con el servidor",
      icon: "error",
      confirmButtonColor: "#ff6464",
    });
  };

  xhr.send();
}