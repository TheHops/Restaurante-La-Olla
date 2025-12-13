document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("listaEstadoOrdenes");
  
  const contenedor = document.getElementById("listaOrdenesPoFoC");
  contenedor.style.opacity = "0";

  setTimeout(() => {
    MP(1);
  
    obtenerValorOrden().then((valorGuardado) => {
      if (valorGuardado) {
        select.value = valorGuardado;
        filtrarOrdenes(valorGuardado);
      } else {
        filtrarOrdenes(select.value);
      }
  
      // Guardar cambios
      select.addEventListener("change", function () {
        localStorage.setItem("estadoOrdenSeleccionado", this.value);
      });
  
      iniciarPolling();
    });
  }, 300);

});

/////////////////////////////////////////////////////////////////////

function FacturarOrden() {
  let idOrdenF = document.getElementById("idOrdenFactura");
  let CambioOrden = document.getElementById("CambioOrden");
  let MontoOrden = document.getElementById("MontoOrden");
  let PropinaOrden = document.getElementById("txtValorPorcentajePropina");
  let DescuentoOrden = document.getElementById("txtValorPorcentajeDescuento");

  let Propina = PropinaOrden.value;

  if (PropinaOrden.value == "") {
    Propina = 0;
  }

  console.log(
    "ID: " +
      idOrdenF.value +
      " Cambio: " +
      CambioOrden.value +
      " Monto: " +
      MontoOrden.value +
      " Propina: " +
      Propina
  );

  let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  console.log(token);

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/FacturarOrden/", true);

  // xhr.setRequestHeader('Content-Type', 'application/json');
  // Abrir la conexión, y especificamos el método

  let datos = new FormData(); // Es un formulario de JS para leer el codigo

  datos.append("csrfmiddlewaretoken", token);
  datos.append("monto", MontoOrden.value);
  datos.append("cambio", CambioOrden.value);
  datos.append("idOrden", idOrdenF.value);
  datos.append("propinaOrden", Propina);

  xhr.onreadystatechange = function () {
    if (this.readyState == 4) {
      console.log("SI ENTRÓ A LA FUNCIÓN ONREADY (FACTURAR ORDEN)");
    }
  };
  // Se envían los datos
  xhr.send(datos);

  Swal.fire({
    confirmButtonColor: "#ff6464", //'#ff964e',
    title: "¡Orden #" + idOrdenF.value + " registrada correctamente!",
    icon: "success",
  }).then((resultado) => {
    if (resultado.isConfirmed) {
      location.reload();
    } else {
      location.reload();
    }
  });
}

function MP(valor) {
  ReiniciarCampos();

  let CambioOrden = document.getElementById("cambio");
  let MontoOrden = document.getElementById("monto");
  let NumRefOrden = document.getElementById("numRef");

  let BtnRegistrar = document.getElementById("btnFacturar");

  console.log(valor);

  if (valor == 1) {
    CambioOrden.style.display = "initial";
    MontoOrden.style.display = "initial";
    NumRefOrden.style.display = "none";
    
    BtnRegistrar.disabled = true;
  } else if (valor == 2) {
    CambioOrden.style.display = "none";
    MontoOrden.style.display = "none";
    NumRefOrden.style.display = "none";
    
    BtnRegistrar.disabled = false;
  } else {
    CambioOrden.style.display = "none";
    MontoOrden.style.display = "none";
    NumRefOrden.style.display = "initial";
    
    BtnRegistrar.disabled = true;
  }
}

document.getElementById("txtPorcentajePropina").addEventListener("input", function () {
  validarCampoNumero(this, 0, 10);
  
  let total = parseFloat($("#totalOrdenFactura").val().replace(",", ".")) || 0;
  let porcentaje = parseFloat(this.value) || 0;

  let resultado = (total * porcentaje) / 100;

  console.log("Resultado - total - porcentaje");
  console.log(resultado);
  console.log(total);
  console.log(porcentaje);

  $("#txtValorPorcentajePropina").val(resultado);
});

document.getElementById("txtPorcentajeDescuento")
  .addEventListener("input", function () {
    validarDescuentoDebounce.call(this);

    let total =
      parseFloat($("#totalOrdenFactura").val().replace(",", ".")) || 0;
    let porcentaje = parseFloat(this.value) || 0;

    let resultado = (total * porcentaje) / 100;

    resultado *= -1;

    $("#txtValorPorcentajeDescuento").val(resultado);
  });

function validarCampoNumero (input, minimo, maximo){
  let dato = parseFloat(input.value);

  if (isNaN(dato)) {
    input.value = "";
    return;
  }

  if (dato < minimo) dato = minimo;
  if (dato > maximo) dato = maximo;

  input.value = dato;
}

const validarDescuentoDebounce = debounce(function () {
  validarCampoNumero(this, 10, 30);
}, 500);

function debounce(fn, delay = 400) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), delay);
  };
}

function rellenarParaFacturar(id, total) {
  // El total declarado de forma global se le asigna un valor del total según la orden
  TotalGlobal = parseInt(total);
  console.log(TotalGlobal);

  let idOrdenF = document.getElementById("idOrdenFactura");
  let totalOrdenF = document.getElementById("totalOrdenFactura");

  idOrdenF.value = id;
  totalOrdenF.value = total;

  // Se vacían los campos
  ReiniciarCampos();

  // Se coloca el total para mostrarlo y que el usuario ingrese un buen monto
  let Monto = document.getElementById("totalOrdenMonto");
  Monto.innerHTML = "Total: C$" + total;
}

document.getElementById("MontoOrden").addEventListener("input", function () {
  // Se obtiene el valor de lo que se ingresa cada vez que se escribe algo
  let MontoIngresado = document.getElementById("MontoOrden").value;
  console.log(MontoIngresado);

  let MensajeMonto = document.getElementById("MensajeMonto");
  let CambioOrden = document.getElementById("CambioOrden");
  let btnFacturar = document.getElementById("btnFacturar");

  try {
    // Se realiza el cálculo del monto
    let Cambio = parseInt(MontoIngresado) - TotalGlobal;
    console.log("Cambio = " + Cambio);

    // Se verifica si el monto está bien ingresado
    if (MontoIngresado < TotalGlobal) {
      MensajeMonto.style.display = "initial";

      CambioOrden.value = "";

      btnFacturar.disabled = true;
    } else {
      MensajeMonto.style.display = "none";

      CambioOrden.value = Cambio;

      btnFacturar.disabled = false;
    }
  } catch (error) {
    MensajeMonto.style.display = "initial";

    CambioOrden.value = "";

    btnFacturar.disabled = true;
  }
});

/////////////////////////////////////////////////////////////////////

// Se guarda el total de forma global
var TotalGlobal;

function ReiniciarCampos() {
  let CambioOrden = document.getElementById("CambioOrden");
  let MontoOrden = document.getElementById("MontoOrden");
  let MensajeMonto = document.getElementById("MensajeMonto");
  let btnFacturar = document.getElementById("btnFacturar");

  CambioOrden.value = "";
  MontoOrden.value = "";
  MensajeMonto.style.display = "none";
  btnFacturar.disabled = true;
}

/////////////////////////////////////////////////////////////////////

let intervaloPolling = null;

function iniciarPolling() {
  // Evitar múltiples timers
  if (intervaloPolling !== null) {
    clearInterval(intervaloPolling);
  }

  // Cada 4 segundos se consulta nuevamente
  intervaloPolling = setInterval(async () => {
    let valorOrden = await obtenerValorOrden();
    filtrarOrdenes(valorOrden);
  }, 7000);
}

function pausarPolling() {
  if (intervaloPolling !== null) {
    clearInterval(intervaloPolling);
    intervaloPolling = null;
  }
}

function reanudarPolling() {
  iniciarPolling();
}

let timerIntervalId = null;

function iniciarTimers() {
  if (timerIntervalId) {
    clearInterval(timerIntervalId);
    timerIntervalId = null;
  }

  const timers = document.querySelectorAll(".timer");

  function formatearTiempo(diffMs, texto) {
    const horas = Math.floor(diffMs / 3600000);
    const minutos = Math.floor((diffMs % 3600000) / 60000);
    const segundos = Math.floor((diffMs % 60000) / 1000);

    if (horas > 0) texto += `${horas}h `;
    texto += `${minutos}m ${segundos}s`;

    return texto;
  }

  function actualizarTimers() {
    const ahora = new Date();

    timers.forEach((timer) => {
      const fecha = new Date(timer.dataset.fecha);
      const diff = ahora - fecha;

      let estado = timer.dataset.estado;

      let texto = "";

      if (estado == "1") texto = "Creada hace ";
      else if (estado == "4") texto = "Preparando hace ";
      else texto = "";

      // Formato del texto
      timer.textContent = formatearTiempo(diff, texto);

      // Quitar clases anteriores
      timer.classList.remove("naranja", "rojo");

      const minutos = Math.floor(diff / 60000);

      // Colores según tiempo
      if (minutos >= 20 && minutos < 40) {
        timer.classList.add("naranja");
      } else if (minutos >= 40) {
        timer.classList.add("rojo");
      }
    });
  }

  actualizarTimers();
  timerIntervalId = setInterval(actualizarTimers, 1000);
}

/////////////////////////////////////////////////////////////////////

const opcionesDisponibles = {
  Administrador: ["0", "1", "2", "3", "4", "5"],
  Mesero: ["1", "4", "6"],
  Cocinero: ["1", "4", "6"],
  Cajero: ["0", "2", "3"],
};

const valoresPorDefecto = {
  Administrador: "5",
  Mesero: "6",
  Cocinero: "6",
  Cajero: "3",
};

function validarFiltroPorCargo(cargo, valorFiltro) {
  const opciones = opcionesDisponibles[cargo];
  const valorDefault = valoresPorDefecto[cargo];

  if (opciones.includes(valorFiltro)) {
    return valorFiltro;
  }

  return valorDefault;
}

async function obtenerValorOrden() {
  let valorGuardado = localStorage.getItem("estadoOrdenSeleccionado");
  const cargo = await obtenerCargoUsuario();

  valorGuardado = validarFiltroPorCargo(cargo, valorGuardado);
  return valorGuardado;
}

/////////////////////////////////////////////////////////////////////

// --- Enviar solicitud al servidor (retorna una promesa) ---
function enviarCancelacion(idOrden, motivo) {
  return new Promise((resolve, reject) => {
    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/CancelarOrden/", true);

    const datos = new FormData();
    datos.append("csrfmiddlewaretoken", token);
    datos.append("idOrden", idOrden);
    datos.append("motivo", motivo);

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          try {
            const respuesta = JSON.parse(xhr.responseText);
            resolve(respuesta);
          } catch (e) {
            reject("Error al procesar la respuesta del servidor.");
          }
        } else {
          reject("Error de red o servidor: " + xhr.status);
        }
      }
    };

    xhr.onerror = function () {
      reject("Error al conectar con el servidor.");
    };

    xhr.send(datos);
  });
}

async function CancelarOrden(idOrden) {
  const { value: motivo } = await Swal.fire({
    title: "¿Realmente desea anular la orden?",
    html: `
        <input id="motivo" class="swal2-input" placeholder="Escribe el motivo de la anulación (opcional)" maxlength="70" style="
        width: 100%;
        margin-left: 0px;
        margin-right: 0px;
        ">
      `,
    focusConfirm: false,
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Anular",
    confirmButtonColor: "#ff6464",
    icon: "question",
    iconColor: "#ff964e",
    preConfirm: () => document.getElementById("motivo").value.trim(),
  });

  // Si el usuario cancela, salimos
  if (motivo === undefined) return;

  try {
    // Mostrar animación de carga
    Swal.fire({
      title: "Anulando orden...",
      text: "Por favor espere",
      allowOutsideClick: false,
      didOpen: () => Swal.showLoading(),
    });

    // Enviar al servidor
    const respuesta = await enviarCancelacion(idOrden, motivo || "");

    if (respuesta.status === "ok") {
      await Swal.fire({
        title: `¡Orden #${idOrden} anulada correctamente!`,
        icon: "success",
        confirmButtonColor: "#ff6464",
      });
      location.reload();
    } else {
      await Swal.fire({
        title: "Error",
        text: respuesta.message || "No se pudo anular la orden.",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
    }
  } catch (error) {
    await Swal.fire({
      title: "Error",
      text: error,
      icon: "error",
      confirmButtonColor: "#ff6464",
    });
  }
}

/////////////////////////////////////////////////////////////////////

function CambioEstadoOrdenes(cadena)
{
  const contenedor = document.getElementById("listaOrdenesPoFoC");

  contenedor.style.opacity = "0";
  
  setTimeout(() => {
    filtrarOrdenes(cadena);
  }, 300);
}

function filtrarOrdenes(cadena) {
  const contenedor = document.getElementById("listaOrdenesPoFoC");

  const request = new XMLHttpRequest();

  request.open(
    "GET",
    "/FiltrarOrdenes?SelectFiltrarOrdenes=" + encodeURIComponent(cadena)
  );
  request.send();

  request.onreadystatechange = function () {
    if (this.readyState === 4) {
      if (this.status === 200) {
        contenedor.innerHTML = this.responseText;
        
        restaurarDespliegues();
        
        iniciarTimers();

        contenedor.style.opacity = "100%";
      } else {
        console.error("Error al cargar órdenes:", this.status);
      }
    }
  };
}

/////////////////////////////////////////////////////////////////////

async function cambiarEstadoOrden(idOrden, url, textoCarga) {
  try {
    // Mostrar modal de carga
    Swal.fire({
      title: textoCarga,
      allowOutsideClick: false,
      didOpen: () => Swal.showLoading(),
    });

    // Enviar la petición al servidor
    const respuesta = await enviarCambioEstado(idOrden, url);

    // Cerrar modal de carga
    Swal.close();

    if (respuesta.status === "ok") {
      // Mostrar éxito y recargar automáticamente después de 3 segundos
      await Swal.fire({
        title: respuesta.message,
        icon: "success",
        confirmButtonColor: "#ff6464",
        timer: 2300,
      });

      var estadoSeleccionado =
        document.getElementById("listaEstadoOrdenes").value;
      filtrarOrdenes(estadoSeleccionado);
    } else {
      await Swal.fire({
        title: "Error",
        text: respuesta.message || "No se pudo actualizar la orden.",
        icon: "error",
        confirmButtonColor: "#ff6464",
      });
    }
  } catch (error) {
    console.log(error);

    await Swal.fire({
      title: "Error",
      text: error,
      icon: "error",
      confirmButtonColor: "#ff6464",
    });
  }
}

function enviarCambioEstado(idOrden, url) {
  return new Promise((resolve, reject) => {
    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    const datos = new FormData();
    datos.append("csrfmiddlewaretoken", token);
    datos.append("ID", idOrden);

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          try {
            console.log(xhr.responseText);
            const respuesta = JSON.parse(xhr.responseText);
            resolve(respuesta);
          } catch (e) {
            reject("Error al procesar la respuesta del servidor.");
          }
        } else {
          reject("Error de red o servidor: " + xhr.status);
        }
      }
    };

    xhr.onerror = function () {
      reject("Error al conectar con el servidor.");
    };

    xhr.send(datos);
  });
}

/////////////////////////////////////////////////////////////////////

function desplegarDetalles(idOrden) {
  let detallitos = document.getElementById("idDetalleOrden" + idOrden);
  let icono = document.getElementById("iconoOrden" + idOrden);

  icono.classList.toggle("desplegado");
  detallitos.classList.toggle("desplegado");

  guardarEstadoDespliegue(idOrden);
}

function guardarEstadoDespliegue(idOrden) {
  let estados = JSON.parse(localStorage.getItem("ordenesDesplegadas")) || [];

  const indice = estados.indexOf(idOrden);

  if (
    document
      .getElementById("idDetalleOrden" + idOrden)
      .classList.contains("desplegado")
  ) {
    if (indice === -1) estados.push(idOrden);
  } else {
    if (indice !== -1) estados.splice(indice, 1);
  }

  localStorage.setItem("ordenesDesplegadas", JSON.stringify(estados));
}

function restaurarDespliegues() {
  const estados = JSON.parse(localStorage.getItem("ordenesDesplegadas")) || [];

  estados.forEach((idOrden) => {
    const detalle = document.getElementById("idDetalleOrden" + idOrden);
    const icono = document.getElementById("iconoOrden" + idOrden);

    if (detalle && icono) {
      detalle.classList.add("desplegado");
      icono.classList.add("desplegado");
    }
  });
}

///////////////////////////////////////////////////////

$("#checkPropina").on("change", function () {
  $("#inputPorcentajePropina").toggle(this.checked);
});

$("#checkDescuento").on("change", function () {
  $("#inputPorcentajeDescuento").toggle(this.checked);
});