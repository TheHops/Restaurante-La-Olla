document.addEventListener("DOMContentLoaded", () => {
  const pass1 = document.getElementById("NuevaPassEditarPerfil");
  const pass2 = document.getElementById("VerificarPassEditarPerfil");
  const btn = document.getElementById("btnCambiarPassword");

  const reqLength = document.getElementById("req-length");
  const reqNumber = document.getElementById("req-number");
  const reqSpecial = document.getElementById("req-special");

  function validar() {
    const value = pass1.value;
    let requisitosOk = true;

    // Reset visual si está vacío
    if (value.length === 0 && pass2.value.length === 0) {
      limpiar(pass1);
      limpiar(pass2);
      btn.disabled = true;
      return;
    }

    // 🔹 Requisitos
    toggleReq(reqLength, value.length >= 6);
    toggleReq(reqNumber, /\d/.test(value));
    toggleReq(reqSpecial, /[!@#$%^&*(),.?":{}|<>_\-+=~`[\]\\\/]/.test(value));

    requisitosOk =
      value.length >= 8 &&
      /\d/.test(value) &&
      /[!@#$%^&*(),.?":{}|<>_\-+=~`[\]\\\/]/.test(value);

    // 🔹 Bordes del primer input
    requisitosOk ? marcarValido(pass1) : marcarInvalido(pass1);

    // 🔹 Coincidencia
    if (pass2.value.length > 0) {
      if (value === pass2.value && requisitosOk) {
        marcarValido(pass2);
      } else {
        marcarInvalido(pass2);
      }
    } else {
      limpiar(pass2);
    }

    // 🔹 Botón
    btn.disabled = !(requisitosOk && value === pass2.value);
  }

  function toggleReq(el, ok) {
    el.classList.remove("neutral", "valid", "invalid");
    el.classList.add(ok ? "valid" : "invalid");
  }

  function marcarValido(input) {
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
  }

  function marcarInvalido(input) {
    input.classList.remove("is-valid");
    input.classList.add("is-invalid");
  }

  function limpiar(input) {
    input.classList.remove("is-valid", "is-invalid");
  }

  pass1.addEventListener("input", validar);
  pass2.addEventListener("input", validar);
});

function passwordValida() {
  return document.querySelectorAll("#requisitosPass .valid").length === 3;
}

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

document
.getElementById("formEditarPerfil")
.addEventListener("submit", function (e) {
  e.preventDefault();

  let form = this;

  Swal.fire({
    title: "¿Los cambios están correctos?",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#ff6464",
    cancelButtonColor: "#6c757d",
    iconColor: "#ff964e",
    confirmButtonText: "Confirmar",
    cancelButtonText: "Cancelar",
    reverseButtons: true,
  }).then((result) => {
    if (result.isConfirmed) {
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
              confirmButtonColor: "#ff6464",
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
    }
  });
});

function cambiarPass()
{
  Swal.fire({
    title: "Procesando...",
    text: "Por favor espere",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  const data = {
    NewPass: $("#NuevaPassEditarPerfil").val(),
    VerifyPass: $("#VerificarPassEditarPerfil").val(),
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
  };

  $.ajax({
    url: "/CambiarPass/",
    type: "POST",
    data: data,
    success: function (response) {
      if (response.status === "ok") {
        Swal.fire({
          confirmButtonColor: "#ff6464",
          title: response.message,
          icon: "success",
        }).then(() => location.reload());
        return;
      }

      // cuando es error
      Swal.fire({
        confirmButtonColor: "#ff6464",
        title: "Error",
        text: response.message,
        icon: "error",
      });
    },
    error: function () {
      Swal.fire({
        confirmButtonColor: "#ff6464",
        title: "Error",
        text: "Error interno del servidor.",
        icon: "error",
      });
    },
  });
}