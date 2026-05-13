$(document).ready(function () {
  // Escuchamos el evento de escritura en el input
  $("#EfectivoInicialCajaArqueo").on("input", function () {
    // Obtenemos el valor actual
    let valor = $(this).val();

    // Limpiamos el valor: permitimos solo números y un punto decimal
    // Esto evita que peguen letras
    valor = valor.replace(/[^0-9.]/g, "");
    $(this).val(valor);

    // Lógica de habilitación
    // Verificamos que no esté vacío y que sea un número válido
    if (valor !== "" && !isNaN(valor) && parseFloat(valor) >= 0) {
      $("#btnIniciarArqueo").prop("disabled", false);
      $("#btnIniciarArqueo").css("opacity", "1"); // Opcional: para feedback visual
    } else {
      $("#btnIniciarArqueo").prop("disabled", true);
      $("#btnIniciarArqueo").css("opacity", "0.6");
    }
  });
});

/************************************************************************/

function iniciarArqueo() {
  const montoInicial = $("#EfectivoInicialCajaArqueo").val();

  Swal.fire({
    title: "Iniciando Arqueo...",
    text: "Por favor espere",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  const data = {
    MontoInicial: montoInicial,
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
  };

  $.ajax({
    url: "/InicioArqueo/",
    type: "POST",
    data: data,
    success: function (response) {
      if (response.status === "ok") {
        Swal.fire({
          confirmButtonColor: "#ff6464", // El rojo de La Olla
          title: "¡Éxito!",
          text: response.message,
          icon: "success",
        })
        .then(() => location.reload()); // Recargamos para actualizar la UI
        return;
      }

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
        text: "Error interno del servidor al intentar iniciar el arqueo.",
        icon: "error",
      });
    },
  });
}

/*****************************************************************************/

function validarMontoFinal() {
  let valor = $("#EfectivoFinalCajaArqueo")
    .val()
    .replace(/[^0-9.]/g, "");
  $(this).val(valor);

  // Habilitar botón 'Cerrar' si hay un monto válido
  if (valor !== "" && !isNaN(valor) && parseFloat(valor) >= 0) {
    $("#btnCerrarArqueo").prop("disabled", false);
  } else {
    $("#btnCerrarArqueo").prop("disabled", true);
  }
}

function IniciarCierre (montoInicial, totalEfectivo) {
  // Habilitamos el input y cambiamos el estado visual
  $("#EfectivoFinalCajaArqueo").prop("disabled", false).focus();
  $("#btnIniciarCierre").prop("disabled", true); // Se auto-inhabilita para no repetir la acción

  // Calculamos el monto teórico (Efectivo inicial + Ventas efectivo de hoy)
  // Nota: Estos valores deben venir del contexto de Django
  let inicial = parseFloat(montoInicial) || 0;
  let ventas = parseFloat(totalEfectivo) || 0;
  let teorico = inicial + ventas;

  $("#EfectivoFinalCajaArqueo").val(teorico.toFixed(2));
  $("#txtMontoTeoricoArqueo").text("C$ " + teorico.toFixed(2));

  validarMontoFinal();
};

$(document).ready(function () {
  // 1. Validación en tiempo real del input de cierre
  $("#EfectivoFinalCajaArqueo").on("input", function () {
    validarMontoFinal();
  });

  // 2. Función para enviar el cierre al servidor
  $("#btnCerrarArqueo").on("click", function () {
    cerrarArqueo();
  });
});

function cerrarArqueo() {
  const montoFinalReal = $("#EfectivoFinalCajaArqueo").val();

  Swal.fire({
    title: "Procesando cierre...",
    text: "Calculando diferencias y generando registro",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  $.ajax({
    url: "/CierreArqueo/",
    type: "POST",
    data: {
      MontoFinalReal: montoFinalReal,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      if (response.status === "ok") {
        Swal.fire({
          confirmButtonColor: "#ff6464",
          title: "Arqueo Cerrado",
          text: response.message,
          icon: "success"
        })
        .then((result) => {
          if (result.isConfirmed) {
            location.reload();
          }
        });
      } else {
        Swal.fire({ icon: "error", title: "Error", text: response.message });
      }
    },
    error: function () {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "Error en el servidor.",
      });
    },
  });
}

/********************************************************* */

function MostrarInfo(title, body){
  Swal.fire({
    title: title,
    text: body,
    icon: "info",
    confirmButtonColor: "#888888",
    confirmButtonText: "Entendido",
  });
}
