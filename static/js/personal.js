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

function resetFormAgregarPersonal() {
  const form = document.getElementById("formAgregarPersonal");

  // Reset básico del formulario
  form.reset();

  // Limpieza manual extra (passwords + inputs)
  const inputs = form.querySelectorAll("input");

  inputs.forEach((input) => {
    input.value = "";
    input.setAttribute("value", "");
  });
}

function cargarPersonal(ver) {
  document.getElementById("cuerpoInventario").style.opacity = "0";

  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/FiltrarPersonal?verEliminados=" + (ver ? "1" : "0"));
  xhr.send();

  xhr.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      $(".tablaInventario").DataTable().destroy();

      const tbody = document.querySelector("#cuerpoInventario");
      tbody.innerHTML = this.responseText;

      $(".tablaInventario").DataTable({
        scrollY: "43vh",
        scrollCollapse: true,
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

///////////////////////////////////////////////////////////////////

function ImpresionPersonal(
  usuario,
  correo,
  telefono,
  idCargo,
  idPersonal,
  estado,
  nombre,
  apellido,
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

function ConfirmarRestablecer(idPersonal) {
  Swal.fire({
    title: "¿Realmente desea restablecer la contraseña de este usuario?",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#ff6464",
    cancelButtonColor: "#6c757d",
    iconColor: "#ff964e",
    confirmButtonText: "Restablecer",
    cancelButtonText: "Cancelar",
    reverseButtons: true,
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: "Procesando...",
        text: "Por favor espere",
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading(),
      });

      $.ajax({
        url: "/RestablecerPass/",
        type: "POST",
        data: {
          ID: idPersonal,
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function (response) {
          Swal.close();

          if (response.status === "ok") {
            // Insertar la contraseña nueva en el modal
            $("#nuevaPassTemporal").val(response.new_pass);

            console.log(response.new_pass);

            $("#IdPersonalRestablecerPass").val(idPersonal);

            // Crear instancia y mostrar modal
            const modal = new bootstrap.Modal(
              document.getElementById("modalPassRestablecida"),
            );

            modal.show();
          } else {
            Swal.fire({
              title: "Error",
              text: response.message,
              icon: "error",
              confirmButtonColor: "#343a40",
            });
          }
        },
        error: function () {
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

function ConfirmarBaja(idPersonal) {
  Swal.fire({
    title: "¿Realmente desea dar de baja a este usuario?",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#ff6464",
    cancelButtonColor: "#6c757d",
    iconColor: "#ff964e",
    confirmButtonText: "Dar de baja",
    cancelButtonText: "Cancelar",
    reverseButtons: true,
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
        text: "Debe ingresar los nombres del personal",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
      $("#Fullname").focus();
      return false;
    }

    if (!lastName) {
      Swal.fire({
        title: "Apellido vacío",
        text: "Debe ingresar los apellidos del personal",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
      $("#Apellidos").focus();
      return false;
    }

    if (!usuario) {
      Swal.fire({
        title: "Nombre de usuario vacío",
        text: "Debe ingresar el nombre de usuario",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
      $("#User").focus();
      return false;
    }

    if (!pass) {
      Swal.fire({
        title: "Contraseña vacía",
        text: "Debe ingresar la contraseña temporal del usuario",
        icon: "error",
        confirmButtonColor: "#ff6464",
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
        title: "Nombre de usuario vacío",
        text: "Debe ingresar el nombre de usuario",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
      $("#NameUsuario").focus();
      return false;
    }

    if (!nombre.trim()) {
      Swal.fire({
        title: "Nombre vacío",
        text: "Debe ingresar el nombre del usuario",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
      return false;
    }

    if (!apellido.trim()) {
      Swal.fire({
        title: "Apellido vacío",
        text: "Debe ingresar el apellido del usuario",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
      return false;
    }

    // Si el usuario quiere cambiar contraseña, deben coincidir
    if (newPass || checkPass) {
      if (newPass !== checkPass) {
        Swal.fire({
          title: "Contraseñas no coinciden",
          text: "La confirmación no coincide con la nueva contraseña",
          icon: "error",
          confirmButtonColor: "#ff6464",
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

document.getElementById("btnCopiarPass").addEventListener("click", function () {
  const input = document.getElementById("nuevaPassTemporal");
  const img = document.getElementById("iconoCopiarPass");

  const imgCheck = this.dataset.imgCheck;
  const imgCopy = this.dataset.imgCopy;

  input.select();
  input.setSelectionRange(0, 99999); // Para móviles

  navigator.clipboard
    .writeText(input.value)
    .then(() => {
      img.src = imgCheck;

      Swal.fire({
        icon: "success",
        title: "¡Contraseña copiada!",
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: false,
      });

      setTimeout(() => {
        img.src = imgCopy;
      }, 2000);
    })
    .catch(() => {
      console.error("Ocurrió un error al intentar copiar la contraseña");
    });
});

function EnviarCorreo() {
  let idPersonal = $("#IdPersonalRestablecerPass").val();
  let passTemporal = $("#nuevaPassTemporal").val();

  Swal.fire({
    toast: true,
    position: "top-end",
    title: "Procesando...",
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();
    },
  });

  $.ajax({
    url: "/EnviarCorreo/",
    type: "POST",
    data: {
      idPersonal: idPersonal,
      tituloCorreo: "Nueva contraseña temporal",
      mensajeCorreo: "Su contraseña temporal es: " + passTemporal,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      Swal.close();

      if (response.status === "ok") {
        Swal.fire({
          icon: "success",
          title: response.message,
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 4000,
          timerProgressBar: false,
        });
      } else {
        Swal.fire({
          icon: "error",
          title: response.message,
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 4000,
          timerProgressBar: false,
        });
      }
    },
  });
}

/******************************************************************************/
/*********************************EXPORTAR*************************************/
/******************************************************************************/

function ExportarPersonal(tipo) {
  // PREPARACION DE DATOS
  console.log("Exportación de tipo: " + (tipo == "1" ? "excel" : "pdf"));

  // PETICION AL SERVICIO
  let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  let xhr = new XMLHttpRequest();

  xhr.open("GET", "/ExportarPersonal?Tipo=" + tipo, true);

  xhr.responseType = "blob";

  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", token);

  // Manejamos la respuesta del servidor
  xhr.onload = function () {
    if (xhr.status === 200) {
      const contentType = xhr.getResponseHeader("Content-Type");

      // Si el backend devolvió JSON (error)
      if (contentType && contentType.includes("application/json")) {
        const reader = new FileReader();
        reader.onload = function () {
          const respuesta = JSON.parse(reader.result);
          Swal.fire({
            title: respuesta.message,
            icon: respuesta.status === "error" ? "error" : "success",
            confirmButtonColor: "#ff6464",
          });
        };
        reader.readAsText(xhr.response);
        return;
      }

      // Si es archivo → descargar
      const blob = xhr.response;
      const url = window.URL.createObjectURL(blob);

      const disposition = xhr.getResponseHeader("Content-Disposition");

      let filename = "personal.xlsx";
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