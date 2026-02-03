// EMPIEZA EL FLUJO DE CAMBIO DE PASS DESDE LOGIN
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

// FUNCION QUE NOS REGRESA AL LOGIN
function volverALogin() {
  window.location.href = "/";
}

// SE VALIDA EL CORREO INGRESADO A NIVEL DE FRONT
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

// SE VERIFICA SI EL CORREO EXISTE, SI HAY ALGÚN USUARIO CON ESE CORREO Y SI EL USUARIO ES ADMIN
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

// SE VALIDÓ EL CORREO Y SE ENVIÓ UNA OTP QUE SE GENERÓ Y SE DEBE INGRESAR, SE MUESTRA UN TIMER DE 2 MINUTOS
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

// REENVIAR OTP
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

// VALIDACION DE OTP (FRONT)
function validarOTPForgotPass() {
  const inputOTP = document.getElementById("OTPForgotPass");
  const btnVerificar = document.getElementById("btn_verificar_otp_forgot_pass");

  // Eliminar cualquier cosa que no sea número
  inputOTP.value = inputOTP.value.replace(/\D/g, "");

  // Limitar a 6 dígitos
  if (inputOTP.value.length > 6) {
    inputOTP.value = inputOTP.value.slice(0, 6);
  }

  // Validar exactamente 6 dígitos
  if (inputOTP.value.length === 6) {
    btnVerificar.disabled = false;
    btnVerificar.classList.add("activo");
  } else {
    btnVerificar.disabled = true;
    btnVerificar.classList.remove("activo");
  }
}

// VALIDACION DE OTP (BACKEND)
function verificarOTPForgotPass() {
  const otp = document.getElementById("OTPForgotPass").value.trim();
  const idUsuario = document.getElementById("IdUsuarioOTP").value;
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  // Validación rápida en frontend
  if (!/^\d{6}$/.test(otp)) {
    alert("El OTP debe contener exactamente 6 dígitos");
    return;
  }

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/ValidarOTPForgotPass/", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      // 🔹 Caso OK (HTML renderizado)
      if (xhr.status === 200) {
        document.innerHTML = xhr.responseText;
      }

      // Errores (JSON)
      else {
        try {
          let response = JSON.parse(xhr.responseText);
          alert(response.message);
        } catch (e) {
          alert("Error inesperado al validar el OTP");
        }
      }
    }
  };

  xhr.send(
    "otp=" +
      encodeURIComponent(otp) +
      "&id_usuario=" +
      encodeURIComponent(idUsuario),
  );
}