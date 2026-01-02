function soloNumeros(event) {
  var charCode = event.which ? event.which : event.keyCode;

  // Permitir números del 0 al 9 y la tecla de retroceso
  if ((charCode >= 48 && charCode <= 57) || charCode === 8) {
    var numero = event.target.value;

    // Verificar que no se ingresen múltiples puntos decimales
    if (charCode === 46 && numero.indexOf(".") !== -1) {
      event.preventDefault();
      return false;
    }

    if (numero.length > 7) {
      // Modificado a 7 ya que el índice comienza en 0
      event.preventDefault();
      return false;
    }

    return true;
  } else {
    event.preventDefault();
    return false;
  }
}

document.getElementById("formEditarPerfil").addEventListener("submit", function (e) {
  e.preventDefault();

  let form = this;

  fetch(form.action, {
    method: "POST",
    body: new FormData(form),
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.status === "ok") {
      Swal.fire({
        icon: "success",
        title: data.message,
        confirmButtonColor: "#ff6464",
      });
    } else {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: data.message,
        confirmButtonColor: "#ff6464"
      });
    }
  })
  .catch(() => {
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "No se pudo conectar con el servidor",
    });
  });
});