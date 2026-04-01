document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("listaEstadoOrdenes");
  const labelProceso = document.getElementById("textoSeleccionadoProceso");

  const contenedor = document.getElementById("listaOrdenesPoFoC");
  contenedor.style.opacity = "0";

  setTimeout(() => {
    MP(1);

    obtenerValorOrden().then((valorGuardado) => {
      if (valorGuardado) {
        select.value = valorGuardado;
        labelProceso.innerText = GetNombreEstadoOrden(valorGuardado);
        filtrarOrdenes(valorGuardado);
      } else {
        filtrarOrdenes(select.value);
      }

      // Guardar cambios
      // select.addEventListener("change", function () {
      //   localStorage.setItem("estadoOrdenSeleccionado", this.value);
      // });

      iniciarPolling();
    });
  }, 300);

  ConsultaDebeCambiarPass();
});

function GetNombreEstadoOrden (estado)
{
  if (estado == "0")
    return "Pago registrado"
  else if (estado == "1")
    return "Pendientes"
  else if (estado == "2")
    return "Anuladas"
  else if (estado == "3")
    return "Preparadas"
  else if (estado == "4")
    return "En preparación"
  else if (estado == "5")
    return "Todas"
  else if (estado == "6")
    return "Ambas"
  else if (estado == "7")
    return "Las tres"
}

function ConsultaDebeCambiarPass() {

  $.ajax({
    url: "/DebeCambiarPass/",
    type: "GET",
    success: function (response) {
      if (response.status === "ok" && response.DebeCambiarPass) {
        Swal.fire({
          icon: "warning",
          title:
            "¡Protege tu cuenta! Cambia tu contraseña temporal por una propia",
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 5000,
          timerProgressBar: false,
        });
        return;
      }
    },
  });
}

/////////////////////////////////////////////////////////////////////

async function FacturarOrden() {
  const { value: isConfirmed } = await Swal.fire({
    target: document.getElementById("FacturarOrden"),
    title: "¿Los datos están correctos?",
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Confirmar",
    confirmButtonColor: "#ff6464",
    icon: "question",
    iconColor: "#ff964e",
    reverseButtons: true,
  });

  if (isConfirmed) {
    let idOrdenF = document.getElementById("idOrdenFactura");
    let CambioOrden = document.getElementById("CambioOrden");
    let MontoOrden = document.getElementById("MontoOrden");
    let PropinaOrden = document.getElementById("txtValorPorcentajePropina");
    let DescuentoOrden = document.getElementById("txtValorPorcentajeDescuento");
    let PorcentajePropinaOrden = document.getElementById(
      "txtPorcentajePropina",
    );
    let PorcentajeDescuentoOrden = document.getElementById(
      "txtPorcentajeDescuento",
    );
    let Total = document.getElementById("totalOrdenFactura");
    let MetodoDePago = document.getElementById("SelectMetodoPago");
    let Banco = document.getElementById("SelectBanco");
    let numRef = document.getElementById("numRefOrden");

    // Se validan los valores de propina y descuento según su check
    let propinaCheck = document.getElementById("checkPropina");
    let descuentoCheck = document.getElementById("checkDescuento");

    if (!propinaCheck.checked) {
      PropinaOrden.value = 0;
      PorcentajePropinaOrden.value = 0;
    }

    if (!descuentoCheck.checked) {
      DescuentoOrden.value = 0;
      PorcentajeDescuentoOrden.value = 0;
    }

    let Monto = MontoOrden.value || 0;
    let Cambio = CambioOrden.value || 0;
    let Propina = PropinaOrden.value || 0;
    let Descuento = DescuentoOrden.value || 0;
    let PorcentajePropina = PorcentajePropinaOrden.value || 0;
    let PorcentajeDescuento = PorcentajeDescuentoOrden.value || 0;

    if (MetodoDePago.value == "2" || MetodoDePago.value == "3") Cambio = 0;

    let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/FacturarOrden/", true);

    let datos = new FormData();
    datos.append("csrfmiddlewaretoken", token);
    datos.append("idOrden", idOrdenF.value);
    datos.append("monto", Monto);
    datos.append("cambio", Cambio);
    datos.append("propinaOrden", Propina);
    datos.append("descuentoOrden", Descuento);
    datos.append("porcentajePropinaOrden", PorcentajePropina);
    datos.append("porcentajeDescuentoOrden", PorcentajeDescuento);
    datos.append("totalOrden", Total.value);
    datos.append("metodoPago", MetodoDePago.value);
    datos.append("banco", Banco.value);
    datos.append("numRef", numRef.value);

    xhr.onreadystatechange = function () {
      if (this.readyState === 4) {
        let response = JSON.parse(this.responseText);

        if (this.status === 200 && response.status === "ok") {
          Swal.fire({
            confirmButtonColor: "#ff6464",
            title: response.message,
            icon: "success",
          }).then(() => location.reload());
        } else {
          Swal.fire({
            confirmButtonColor: "#ff6464",
            title: "Error",
            text: response.message || "Ocurrió un error al facturar.",
            icon: "error",
          });
        }
      }
    };

    xhr.send(datos);
  }
}

function MP(valor) {
  ReiniciarCampos();

  let CambioOrden = document.getElementById("cambio");
  let MontoOrden = document.getElementById("monto");
  let NumRefOrden = document.getElementById("numRef");
  let infoMetodoMixto = document.getElementById("infoMetodoPagoMixto");
  let h4 = document.querySelector("#monto h4");
  let h4Cambio = document.querySelector("#cambio h4");
  let bancoh4 = document.querySelector("#banco h4");
  let contMonto = document.querySelector("#monto");

  let BtnRegistrar = document.getElementById("btnFacturar");
  let Banco = document.getElementById("banco");

  let inputCambio = document.getElementById("CambioOrden");

  if (valor == 1) {
    // EFECTIVO
    CambioOrden.style.display = "initial";
    MontoOrden.style.display = "initial";
    NumRefOrden.style.display = "none";
    Banco.style.display = "none";
    infoMetodoMixto.style.display = "none";

    inputCambio.disabled = true;
    inputCambio.placeholder = "";
    inputCambio.value = null;

    // contMonto.classList.remove("mb-2");
    h4.innerHTML = 'Monto (C$)<span class="asterisco">*</span>';
    h4Cambio.innerHTML = 'Cambio<span class="asterisco">*</span>';

    BtnRegistrar.disabled = true;
  } else if (valor == 2) {
    // TARJETA
    CambioOrden.style.display = "none";
    MontoOrden.style.display = "none";
    NumRefOrden.style.display = "none";
    Banco.style.display = "initial";
    infoMetodoMixto.style.display = "none";

    bancoh4.innerHTML = "Banco";

    BtnRegistrar.disabled = false;
  } else if (valor == 3) {
    // TRANSFERENCIA
    CambioOrden.style.display = "none";
    MontoOrden.style.display = "none";
    NumRefOrden.style.display = "initial";
    Banco.style.display = "initial";
    infoMetodoMixto.style.display = "none";

    bancoh4.innerHTML = "Banco";

    BtnRegistrar.disabled = false;
  } else {
    // EFECTIVO Y TARJETA
    CambioOrden.style.display = "initial";
    MontoOrden.style.display = "initial";
    NumRefOrden.style.display = "none";
    Banco.style.display = "initial";
    infoMetodoMixto.style.display = "initial";

    inputCambio.disabled = false;
    inputCambio.placeholder = "Ej: 50";

    contMonto.classList.add("mb-2");
    h4.innerHTML = "Monto en efectivo (C$)<span class='asterisco'>*</span>";
    h4Cambio.innerHTML = "Cambio en efectivo<span class='asterisco'>*</span>";
    bancoh4.innerHTML = "Banco de la tarjeta";

    BtnRegistrar.disabled = true;
  }

  CalcularTotal();
}

///////////////////////////// EXTRAS /////////////////////////////////////

document
  .getElementById("txtPorcentajePropina")
  .addEventListener("input", function () {
    CalcularPropina(); // Reutilización directa
  });

function CalcularPropina() {
  // Validación del campo porcentaje
  let txtPorcentajePropina = document.getElementById("txtPorcentajePropina");
  validarCampoNumero(txtPorcentajePropina, 0, 10);

  // Obtención del descuento
  let DescuentoCalculado = document.getElementById(
    "txtValorPorcentajeDescuento",
  ).value;
  let descuentoCheck = document.getElementById("checkDescuento");

  let valorDescuento =
    DescuentoCalculado == "" ? 0 : parseFloat(DescuentoCalculado);

  // Si el descuento no está activo, no se aplica
  if (!descuentoCheck.checked) valorDescuento = 0;

  // Total base de la orden
  let total = parseFloat($("#totalOrdenFactura").val().replace(",", ".")) || 0;

  // Primero se aplica el descuento (regla de negocio)
  total += valorDescuento; // DESCUENTO APLICADO AQUÍ

  // Porcentaje de propina
  let porcentaje = parseFloat(txtPorcentajePropina.value) || 0;

  // Cálculo de la propina sobre el total ya descontado
  let resultado = redondear((total * porcentaje) / 100); // PROPINA CALCULADA DESPUÉS DEL DESCUENTO

  // Se asigna el valor calculado
  $("#txtValorPorcentajePropina").val(resultado);

  return resultado; // Se retorna para reutilizarlo
}

let debounceDescuentos = null;

document
  .getElementById("txtPorcentajeDescuento")
  .addEventListener("input", function () {
    clearTimeout(debounceDescuentos);

    let total =
      parseFloat($("#totalOrdenFactura").val().replace(",", ".")) || 0;

    debounceDescuentos = setTimeout(() => {
      validarCampoNumero(this, 10, 30);

      calculosDescuento(this, total);

      CalcularTotal();
    }, 1000);

    calculosDescuento(this, total);
  });

function calculosDescuento(input, total) {
  let porcentaje = parseFloat(input.value) || 0;
  let resultado = (total * porcentaje) / 100;

  resultado *= -1;

  $("#txtValorPorcentajeDescuento").val(resultado);
}

function validarCampoNumero(input, minimo, maximo) {
  let dato = parseFloat(input.value);

  if (isNaN(dato)) {
    input.value = "";
    return;
  }

  if (dato < minimo) dato = minimo;
  if (dato > maximo) dato = maximo;

  input.value = dato;
}

////////////////////////// RELLENAR ////////////////////////////////////

function rellenarParaFacturar(id, total) {
  // El total declarado de forma global se le asigna un valor del total según la orden
  TotalGlobal = parseInt(total);

  let idOrdenF = document.getElementById("idOrdenFactura");
  let totalOrdenF = document.getElementById("totalOrdenFactura");

  idOrdenF.value = id;
  totalOrdenF.value = total;

  // Se vacían los campos
  ReiniciarCampos();

  let propina = document.getElementById("checkPropina");
  propina.checked = true;
  toggleContenedor("inputPorcentajePropina", true);

  // Se coloca el total para mostrarlo y que el usuario ingrese un buen monto
  let Monto = document.getElementById("totalOrdenMonto");
  Monto.innerHTML = "Total a pagar: C$" + total;

  CalcularTotal();
}

////////////////////////////////////////////////////////////////////

document.getElementById("MontoOrden").addEventListener("input", CalcularTotal);
document
  .getElementById("txtPorcentajeDescuento")
  .addEventListener("input", CalcularTotal);
document
  .getElementById("txtPorcentajePropina")
  .addEventListener("input", CalcularTotal);
document.getElementById("checkPropina").addEventListener("change", function () {
  let propinaCheck = document.getElementById("checkPropina");
  let descuentoCheck = document.getElementById("checkDescuento");

  $("#infoCalculoPropina").toggle(
    propinaCheck.checked && descuentoCheck.checked,
  );

  CalcularTotal();
});
document
  .getElementById("checkDescuento")
  .addEventListener("change", function () {
    let propinaCheck = document.getElementById("checkPropina");
    let descuentoCheck = document.getElementById("checkDescuento");

    $("#infoCalculoPropina").toggle(
      propinaCheck.checked && descuentoCheck.checked,
    );

    CalcularTotal();
  });

function redondear(valor, decimales = 2) {
  return Number(Math.round(valor + "e" + decimales) + "e-" + decimales);
}

function CalcularTotal() {
  let MetodoPago = document.getElementById("SelectMetodoPago");

  let txtTotalOrden = document.getElementById("totalOrdenMonto");

  // Se obtiene el valor de lo que se ingresa cada vez que se escribe algo
  let MontoIngresado = document.getElementById("MontoOrden").value;
  let DescuentoCalculado = document.getElementById(
    "txtValorPorcentajeDescuento",
  ).value;

  let valorPropina = CalcularPropina(); // Se guarda la propina calculada

  MontoIngresado = MontoIngresado == "" ? 0 : MontoIngresado;
  let valorDescuento = DescuentoCalculado == "" ? 0 : DescuentoCalculado;

  let propinaCheck = document.getElementById("checkPropina");
  let descuentoCheck = document.getElementById("checkDescuento");

  if (!propinaCheck.checked) valorPropina = 0;

  if (!descuentoCheck.checked) valorDescuento = 0;

  let MensajeMonto = document.getElementById("MensajeMonto");
  let CambioOrden = document.getElementById("CambioOrden");
  let btnFacturar = document.getElementById("btnFacturar");

  try {
    let totalGlobalNumero = parseFloat(TotalGlobal);
    let valorDescuentoNumero = parseFloat(valorDescuento);
    let valorPropinaNumero = parseFloat(valorPropina);

    // Se realiza el cálculo del monto
    let MontoNumero = parseFloat(MontoIngresado);

    if (Number.isNaN(MontoNumero)) {
      throw new Error("El valor no se puede convertir a un número");
    }

    let totalPagar = redondear(
      totalGlobalNumero + valorDescuentoNumero + valorPropinaNumero,
    );

    txtTotalOrden.textContent = `Total a pagar: C$${totalPagar}`;

    // Se verifica si el monto está bien ingresado
    if (MontoNumero < totalPagar && MetodoPago.value == "1") {
      MensajeMonto.style.display = "initial";

      CambioOrden.value = "";

      btnFacturar.disabled = true;
    } else if (MetodoPago.value == "4") {
      MensajeMonto.style.display = "none";

      btnFacturar.disabled = false;
    } else {
      // Este calculo aplica solo para efectivo
      let Cambio = redondear(MontoNumero - totalPagar);

      MensajeMonto.style.display = "none";

      CambioOrden.value = Cambio;

      btnFacturar.disabled = false;
    }
  } catch (error) {
    if (MetodoPago.value == "1") MensajeMonto.style.display = "initial";

    CambioOrden.value = "";

    btnFacturar.disabled = true;

    console.error(error);
  }
}

/////////////////////////////////////////////////////////////////////

// Se guarda el total de forma global
var TotalGlobal;

function ReiniciarCampos() {
  let CambioOrden = document.getElementById("CambioOrden");
  let MontoOrden = document.getElementById("MontoOrden");
  let MensajeMonto = document.getElementById("MensajeMonto");
  let btnFacturar = document.getElementById("btnFacturar");

  $("#inputPorcentajePropina").toggle(false);
  $("#inputPorcentajeDescuento").toggle(false);

  let descuentoCheck = document.getElementById("checkDescuento");
  let propinaCheck = document.getElementById("checkPropina");

  descuentoCheck.checked = false;
  propinaCheck.checked = false;

  $("#infoCalculoPropina").toggle(false);

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
  Mesero: ["1", "4", "3", "7"],
  Armador: ["1", "4", "6"],
  Cajero: ["0", "2", "3"],
};

const valoresPorDefecto = {
  Administrador: "5",
  Mesero: "7",
  Armador: "6",
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
        <div class="lblMotivoOrdenAnular" style="text-align: left; font-weight: bold;">Motivo de la anulación (opcional)</div>
        <input id="motivo" class="swal2-input" placeholder="Ej: No quiso pagar" maxlength="150" style="
        width: 100%;
        margin-top: 6px;
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
    didOpen: () => {
      const input = document.getElementById("motivo");
      if (input) input.blur();
    },
    preConfirm: () => document.getElementById("motivo").value.trim(),
    reverseButtons: true,
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

function CambioEstadoOrdenes(cadena) {
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
    "/FiltrarOrdenes?SelectFiltrarOrdenes=" + encodeURIComponent(cadena),
  );
  request.send();

  request.onreadystatechange = function () {
    if (this.readyState === 4) {
      if (this.status === 200) {
        contenedor.innerHTML = this.responseText;

        restaurarDespliegues();

        iniciarTimers();

        validarMostrarEmptyState();

        contenedor.style.opacity = "100%";
      } else {
        console.error("Error al cargar órdenes:", this.status);
      }
    }
  };
}

function validarMostrarEmptyState (){
  const contenedor = document.getElementById("listaOrdenesPoFoC");
  const emptyState = document.getElementById("emptyStateOrdenes");

  // Buscamos si existen elementos con la clase 'ordenPoFoC' dentro del contenedor
  const tieneOrdenes = contenedor.querySelectorAll(".ordenPoFoC").length > 0;

  if (tieneOrdenes) {
    // Si hay órdenes, ocultamos el empty state
    emptyState.style.display = "none";
  } else {
    // Si está vacío, mostramos el empty state
    emptyState.style.display = "flex"; // Usamos flex para centrar contenido si es necesario
  }
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
  toggleContenedor("inputPorcentajePropina", this.checked);
});

function toggleContenedor (id, checked){
  $("#" + id).toggle(checked);
}

$("#checkDescuento").on("change", function () {
  $("#inputPorcentajeDescuento").toggle(this.checked);
});

/* DROPDOWN */

const dropdownProceso = document.getElementById("dropdownEstadoOrdenesProceso");
const inputEstado = document.getElementById("listaEstadoOrdenes");
const labelProceso = document.getElementById("textoSeleccionadoProceso");
const optionsProceso = dropdownProceso.querySelectorAll(".dropdown-menu li");

optionsProceso.forEach((option) => {
  option.addEventListener("click", () => {
    const val = option.getAttribute("data-value");
    const txt = option.innerText;

    // 1. Actualizamos visualmente
    inputEstado.value = val;
    labelProceso.innerText = txt;

    // 2. Cerramos el menú
    dropdownProceso.classList.remove("is-active");

    // 3. EJECUTAMOS TU FUNCIÓN ORIGINAL
    // Esto reemplaza al onchange="CambioEstadoOrdenes(this.value)"
    if (typeof CambioEstadoOrdenes === "function") {
      localStorage.setItem("estadoOrdenSeleccionado", val);
      CambioEstadoOrdenes(val);
    }
  });

  option.setAttribute("tabindex", "0");
});

// Reutilizamos la lógica de apertura por hover/foco
dropdownProceso
  .querySelector(".dropdown-trigger")
  .addEventListener("focus", () => {
    dropdownProceso.classList.add("is-active");
  });

dropdownProceso.addEventListener("mouseleave", () => {
  dropdownProceso.classList.remove("is-active");
});