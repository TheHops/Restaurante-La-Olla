document.addEventListener("DOMContentLoaded", () => {
  const check = document.getElementById("checkVerPersonalInactivos");
  const key = "verEliminadosPersonal";

  // Restaurar estado guardado
  check.checked = localStorage.getItem(key) === "1";

  // Cargar tabla al inicio
  cargarPersonal(check.checked);

  check.addEventListener("change", () => {
    localStorage.setItem(key, check.checked ? "1" : "0");
    cargarPersonal(check.checked);
  });
});

function cargarPersonal(ver) {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/FiltrarPersonal?verEliminados=" + (ver ? "1" : "0"));
  xhr.send();

  xhr.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      $(".tablaInventario").DataTable().destroy();

      const tbody = document.querySelector("#cuerpoInventario");
      tbody.innerHTML = this.responseText;

      $(".tablaInventario").DataTable({
        scrollY: "50vh",
        scrollCollapse: true,
        paging: true,
        language: {
          url: "https://cdn.datatables.net/plug-ins/1.12.1/i18n/es-ES.json",
        },
      });
    }
  };
}

///////////////////////////////////////////////////////////////////

function ImpresionPersonal(
  usuario,
  correo,
  telefono,
  idCargo,
  idPersonal,
  estado,
  nombre,
  apellido
) {
  $("#NameUsuario").val(usuario);
  $("#CorreoUsuario").val(correo == "None" || correo == "" ? null : correo);
  $("#NumberUsuario").val(telefono == "None" || correo == "" ? null : telefono);
  $("#IdPersonal").val(idPersonal);
  $("#NombreUsuarioMod").val(nombre);
  $("#ApellidosUsuarioMod").val(apellido);
  $("#idCargoModificar").val(idCargo);
  $("#idEstadoModificar").val(estado === "1" ? 1 : 0);
}

function Agregar_Personal() {
  const data = {
    Nombre: $("#Fullname").val(),
    Apellido: $("#Apellidos").val(),
    User: $("#User").val(),
    Pass: $("#Pass").val(),
    Correo: $("#e-mail").val(),
    Telefono: $("#telefono").val(),
    Cargo: $("#idCargo").val(),
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
  };

  if (!ValidacionCamposVacios(1)) return;

  Swal.fire({
    title: "Procesando...",
    text: "Por favor espere",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  $.ajax({
    url: "/AgregarPersonal/",
    type: "POST",
    data: data,
    success: function (response) {
      console.log(response);

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
        title: "Error de servidor",
        text: "Hubo un error inesperado",
        icon: "error",
      });
    },
  });
}

function ModificarPersonal() {
  const data = {
    User: $("#NameUsuario").val(),
    Correo: $("#CorreoUsuario").val(),
    NewPass: $("#NewPassword").val(),
    Telefono: $("#NumberUsuario").val(),
    Cargo: $("#idCargoModificar").val(),
    IDPersonal: $("#IdPersonal").val(),
    Estado: $("#idEstadoModificar").val(),
    NameUsuario: $("#NombreUsuarioMod").val(),
    LastNameUsuario: $("#ApellidosUsuarioMod").val(),
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
  };

  if (!ValidacionCamposVacios(2)) return;

  Swal.fire({
    title: "Procesando...",
    text: "Por favor espere",
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading(),
  });

  $.ajax({
    url: "/ModificarPersonal/",
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

function ConfirmarBaja(idPersonal) {
  Swal.fire({
    title: "¿Realmente desea dar de baja a este usuario?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#ff6464",
    cancelButtonColor: "#6c757d",
    confirmButtonText: "Dar de baja",
    cancelButtonText: "Cancelar",
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: "/DarBajaPersonal/",
        type: "POST",
        data: {
          ID: idPersonal,
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function (response) {
          if (response.status === "ok") {
            Swal.fire({
              title: response.message,
              icon: "success",
              confirmButtonColor: "#ff6464",
            }).then((resultado) => {
              location.reload();
            });
          } else {
            Swal.fire({
              title: "Error",
              text: response.message,
              icon: "error",
              confirmButtonColor: "#343a40",
            });
          }
        },
        error: function (xhr) {
          Swal.fire({
            title: "Error",
            text: "Ocurrió un error en la solicitud.",
            icon: "error",
            confirmButtonColor: "#343a40",
          });
        },
      });
    }
  });
}

function ValidacionCamposVacios(banderaFormulario) {
  // validamos los paremetros que no deben estar vacios en el
  var bandera = banderaFormulario;
  if (bandera === 1) {
    // validacion en agregacion personal
    const fullname = $("#Fullname").val().trim();
    const lastName = $("#Apellidos").val().trim();
    const usuario = $("#User").val().trim();
    const pass = $("#Pass").val().trim();

    if (!fullname) {
      Swal.fire({
        title: "Nombre vacío",
        text: "Debe ingresar los nombres del personal.",
        icon: "warning",
      });
      $("#Fullname").focus();
      return false;
    }

    if (!lastName) {
      Swal.fire({
        title: "Apellido vacío",
        text: "Debe ingresar los apellidos del personal.",
        icon: "warning",
      });
      $("#Apellidos").focus();
      return false;
    }

    if (!usuario) {
      Swal.fire({
        title: "Usuario vacío",
        text: "Debe ingresar el nombre de usuario.",
        icon: "warning",
      });
      $("#User").focus();
      return false;
    }

    if (!pass) {
      Swal.fire({
        title: "Contraseña vacía",
        text: "Debe ingresar la contraseña.",
        icon: "warning",
      });
      $("#Pass").focus();
      return false;
    }
  } else if (bandera === 2) {
    // validacion en modificacion personal
    const usuario = $("#NameUsuario").val();
    const nombre = $("#NombreUsuarioMod").val();
    const apellido = $("#ApellidosUsuarioMod").val();
    const newPass = $("#NewPassword").val();
    const checkPass = $("#CheckPassword").val();

    // Validar campos obligatorios
    if (!usuario.trim()) {
      Swal.fire({
        title: "Campo Usuario Vacío",
        text: "Debe ingresar un usuario.",
        icon: "warning",
      });
      $("#NameUsuario").focus();
      return false;
    }

    if (!nombre.trim()) {
      Swal.fire({
        title: "Nombre Vacío",
        text: "Debe ingresar el nombre del usuario.",
        icon: "warning",
      });
      return false;
    }

    if (!apellido.trim()) {
      Swal.fire({
        title: "Apellido Vacío",
        text: "Debe ingresar el apellido del usuario.",
        icon: "warning",
      });
      return false;
    }

    // Si el usuario quiere cambiar contraseña, deben coincidir
    if (newPass || checkPass) {
      if (newPass !== checkPass) {
        Swal.fire({
          title: "Contraseñas no coinciden",
          text: "La confirmación no coincide con la nueva contraseña.",
          icon: "warning",
        });
        return false;
      }
    }
  }
  return true;
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

function PasoIDBaja(id) {
  $("#IdPersonalBaja").val(id);
}