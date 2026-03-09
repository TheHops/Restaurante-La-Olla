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

function confirmLogout(url) {
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
      window.location.href = url;
    }
  });
}