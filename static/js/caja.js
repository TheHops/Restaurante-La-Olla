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
        }).then(() => location.reload()); // Recargamos para actualizar la UI
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