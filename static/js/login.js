function InicioForgotPassword() {
  var contenedor = document.getElementById("derecha");

  contenedor.classList.add("hide");

  let request = new XMLHttpRequest();

  const url = `/ForgotPassword`;

  // data.append('InputBuscarPlatillo', cadena);
  request.open("GET", url);
  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status === 200) {
      console.log("INICIO FORGOT AFTER GET");

      setTimeout(() => {
        if (contenedor) {
          contenedor.innerHTML = this.responseText;
          contenedor.classList.remove("hide");
        }
      }, 500);
    }
  };

  request.send();
}

///////////////////////////////////////////////////////////////////

function volverALogin() {
  window.location.href = "/";
}

function validarCorreoForgotPass() {
  const inputCorreo = document.getElementById("CorreoForgotPass");
  const btnVerificar = document.getElementById(
    "btn_verificar_correo_forgot_pass",
  );

  const correo = inputCorreo.value.trim();

  console.log("Se está validando");

  // Expresión regular básica para correo
  const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (regexCorreo.test(correo)) {
    btnVerificar.disabled = false;
  } else {
    btnVerificar.disabled = true;
  }
}

function validarOTPForgotPass() {
  const inputOTP = document.getElementById("OTPForgotPass");

  console.log("VERIFICA OTP");

  if (inputOTP.value.length > 6) {
    inputOTP.value = inputOTP.value.slice(0, 6); // cortar a 6 dígitos
  }
}

function verificarCorreo() {
  let correo = document.getElementById("CorreoForgotPass").value.trim();
  var contenedor = document.getElementById("derecha");

  contenedor.classList.add("hide");

  Swal.fire({
    title: "Procesando...",
    text: "Por favor espere",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  console.log("ENTRA A VERIFICAR CORREO");

  if (correo === "") {
    Swal.fire({
      icon: "warning",
      title: "Correo requerido",
      text: "Debes ingresar un correo electrónico.",
      confirmButtonColor: "#ff6464",
      iconColor: "#ff964e",
      confirmButtonText: "Ok",
      reverseButtons: true,
    });
    return;
  }

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/ValidateEmailForgotPass/", true);
  xhr.setRequestHeader(
    "X-CSRFToken",
    document.getElementsByName("csrfmiddlewaretoken")[0].value,
  );

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        setTimeout(() => {
          Swal.close();
        }, 800);

        setTimeout(() => {
          if (contenedor) {
            contenedor.innerHTML = this.responseText;
            contenedor.classList.remove("hide");

            iniciarTimer();
          }
        }, 1000);
      } else {
        contenedor.classList.remove("hide");

        let response = JSON.parse(xhr.responseText);

        Swal.fire({
          icon: "error",
          title: "Error",
          text: response.message,
          confirmButtonColor: "#ff6464",
        }).then(() => {
          window.location.href = "/";
        });
      }
    }
  };

  let data = new FormData();
  data.append("txtCorreoForgotPass", correo);

  xhr.send(data);
}

function iniciarTimer() {
  let segundos = parseInt(document.getElementById("SegundosRestantes").value);

  const timerSpan = document.getElementById("timerOTP");
  const inputOTP = document.getElementById("OTPForgotPass");
  const OTPtext = document.getElementById("otp-timer");
  const btnVerificar = document.getElementById("btn_verificar_otp_forgot_pass");
  const btnReenviar = document.getElementById("btnReenviarOTP");

  btnReenviar.disabled = true;

  function actualizarTimer() {
    let minutos = Math.floor(segundos / 60);
    let seg = segundos % 60;

    timerSpan.textContent = `${minutos}:${seg.toString().padStart(2, "0")}`;

    if (segundos <= 0) {
      clearInterval(intervalo);
      OTPtext.innerHTML = "El código ha <span id='timerOTP'>EXPIRADO</span>";
      // timerSpan.textContent = "EXPIRADO";
      btnReenviar.disabled = false;

      inputOTP.disabled = true;
      btnVerificar.disabled = true;

      Swal.fire({
        icon: "warning",
        title: "OTP expirado",
        text: "El código ha expirado. Debes solicitar uno nuevo.",
        confirmButtonColor: "#ff6464",
      });
    }

    segundos--;
  }

  actualizarTimer();
  const intervalo = setInterval(actualizarTimer, 1000);
}

function reenviarOTP() {
  const idUsuario = document.getElementById("IdUsuarioOTP").value;
  const btnReenviar = document.getElementById("btnReenviarOTP");

  Swal.fire({
    title: "Reenviando código...",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/ReenviarOTPForgotPass/", true);
  xhr.setRequestHeader(
    "X-CSRFToken",
    document.getElementsByName("csrfmiddlewaretoken")[0].value,
  );

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      Swal.close();
      let res = JSON.parse(xhr.responseText);

      if (!res.ok) {
        Swal.fire("Error", res.message, "error");
        return;
      }

      segundos = res.segundos;
      iniciarTimer();

      Swal.fire({
        icon: "success",
        title: "OTP reenviado",
        text: "Revisa tu correo",
        confirmButtonColor: "#ff6464",
      });
    }
  };

  let data = new FormData();
  data.append("idUsuario", idUsuario);
  xhr.send(data);
}