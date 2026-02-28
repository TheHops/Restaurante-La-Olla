// Seleccionamos el checkbox por su id
const combinarCheckbox = document.getElementById("check_combinar_mesas");
const mesasDiv = document.getElementById("mesas");
const botonSiguiente = document.getElementById("btn_siguiente");

document.addEventListener("DOMContentLoaded", (event) => {
  // 1. Obtener una referencia al elemento
  const accionesBusquedaElement = document.getElementById("accionesBusqueda");
  const vPlatillosElement = document.getElementById("VPlatillos");

  // 2. Definir la función que se ejecutará al cambiar el tamaño de la ventana
  function obtenerAlturaAccionesBusqueda() {
    // Utilizar clientHeight para obtener la altura del elemento
    const altura = accionesBusquedaElement.clientHeight;

    // Mostrar el resultado en la consola (o realizar la acción deseada)
    console.log(`El alto actual de 'accionesBusqueda' es: ${altura}px`);

    vPlatillosElement.style.paddingTop = `${altura}px`;

    console.log(`El alto de 'accionesBusqueda' es: ${altura}px`);
    console.log(`Se aplicó padding-top: ${altura}px a 'VPlatillos'.`);
  }

  // 3. Agregar el listener al evento 'resize' de la ventana
  // Esto hace que la función se ejecute cada vez que el usuario redimensiona la ventana.
  window.addEventListener("resize", obtenerAlturaAccionesBusqueda);

  // Opcional: Ejecutar la función una vez al cargar la página para obtener la altura inicial
  obtenerAlturaAccionesBusqueda();

  ConsultaDebeCambiarPass();

  validarMostrarEmptyStateCrearOrden();

  notiPlatillos();
});

function ConsultaDebeCambiarPass() {
  console.log("INICIA CONSULA DEBE CAMBIAR PASS");

  $.ajax({
    url: "/DebeCambiarPass/",
    type: "GET",
    success: function (response) {
      console.log(response);
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

function validarMostrarEmptyStateCrearOrden() {
  const contenedor = document.getElementById("cuerpo_ordenes");
  const emptyState = document.getElementById("emptyStateCrearOrden");

  // Buscamos si existen elementos con la clase 'ordenPoFoC' dentro del contenedor
  const tieneOrdenes = contenedor.querySelectorAll(".orden").length > 0;

  if (tieneOrdenes) {
    // Si hay órdenes, ocultamos el empty state
    emptyState.style.display = "none";
  } else {
    // Si está vacío, mostramos el empty state
    emptyState.style.display = "flex"; // Usamos flex para centrar contenido si es necesario
  }
}

combinarCheckbox.addEventListener("change", function () {
  cambioTipoDeSeleccion(this);
});

function PonerInfoConsumible(imagenUrl, nombre, tipoConsumible, descripcion, precio) {
  // Imagen
  const img = document.getElementById("ImagenDetalleConsumible");
  if (imagenUrl && imagenUrl !== "") {
    img.src = `/media/${imagenUrl}`;
  } else {
    img.src = "/static/img/ProductoSinFoto.png";
  }

  console.log(imagenUrl);
  console.log(nombre);
  console.log(tipoConsumible);
  console.log(descripcion);
  console.log(precio);

  // Nombre del platillo
  document.getElementById("NombreDetalleConsumible").textContent = nombre;

  // Tipo de consumible
  document.getElementById("NombreDetalleTipoConsumible").textContent = tipoConsumible;

  // Descripción
  document.getElementById("DescripcionDetalleConsumible").textContent =
    descripcion && descripcion !== "" ? descripcion : "Sin descripción";

  // Precio
  document.getElementById("PrecioDetalleConsumible").textContent = precio;
}

function cambioTipoDeSeleccion(check) {
  // Seleccionamos todos los inputs dentro del div de mesas
  const inputs = mesasDiv.querySelectorAll("input");

  inputs.forEach((input) => {
    // Guardamos el valor actual de name
    const currentValue = input.value;

    if (check.checked) {
      // Activar "Combinar mesas": convertimos radio en checkbox
      input.type = "checkbox";
      input.name = "mesas_check"; // cambiamos el name para permitir múltiples
    } else {
      // Desactivar "Combinar mesas": convertimos checkbox de nuevo a radio
      input.type = "radio";
      input.name = "mesa"; // nombre original para radio único
      input.checked = false; // desmarcamos todos
      desactivarBoton();
    }
  });

  verificarSeleccionMesas();
}

mesasDiv.addEventListener("change", verificarSeleccionMesas);

function verificarSeleccionMesas() {
  const inputs = mesasDiv.querySelectorAll("input");
  const algunoSeleccionado = Array.from(inputs).some((input) => input.checked);

  botonSiguiente.disabled = !algunoSeleccionado;
}

function activarBoton() {
  botonSiguiente.disabled = false;
}

function desactivarBoton() {
  botonSiguiente.disabled = true;
}

var x = document.getElementById("pag1");
var y = document.getElementById("pag2");

function pagina2() {
  // Se eliminan las clases por si se habían añadido antes, todo es para tener un orden
  x.classList.remove("animate__animated", "animate__fadeInLeft");
  y.classList.remove("animate__animated", "animate__fadeOutRight");

  /**************************************************************/

  // Se establece la duración del objeto 'opciones'
  x.style.setProperty("--animate-duration", "1s");
  y.style.setProperty("--animate-duration", "1.5s");

  /**************************************************************/

  // Se asigna la clase de animación al objeto 'opciones'
  x.classList.add("animate__animated", "animate__fadeOutLeft");
  y.classList.add("animate__animated", "animate__fadeInRight");

  // y.style.transition = "0s"
  y.style.left = "0%";
}

function volver() {
  // Se eliminan las clases por si se habían añadido antes, todo es para tener un orden
  x.classList.remove("animate__animated", "animate__fadeOutLeft");
  y.classList.remove("animate__animated", "animate__fadeInRight");

  /**************************************************************/

  // Se establece la duración del objeto 'opciones'
  x.style.setProperty("--animate-duration", "1s");
  y.style.setProperty("--animate-duration", "1.5s");

  /**************************************************************/

  // Se asigna la clase de animación al objeto 'opciones'
  x.classList.add("animate__animated", "animate__fadeInLeft");
  y.classList.add("animate__animated", "animate__fadeOutRight");

  // y.style.transition = "1.5s"
  // y.style.left = "100%";
}

// Arreglo para manejar las ordenes listadas por medio del ID
var ordenP = [];
var indice = 0;
var cantOrdenes = 0;

function addCarrito(id, nombre, precio) {
  // console.log(id + " - " + nombre + " - " + precio);

  // Se reinicia el indice
  indice = 0;

  // Se crea la variable global para verificar si una orden ya existe o no
  let existeOrden = false;

  // Se obtiene el contenedor de las órdenes
  let contOrdenes = document.getElementById("cuerpo_ordenes");

  // Se obtiene la cantidad
  let cant = document.getElementById(id);

  // Se calcula el subtotal
  let subtotal = cant.value * parseInt(precio);

  // Se recorre el arreglo para verificar si existe el platillo dentro de las órdenes
  while (indice < ordenP.length) {
    if (ordenP[indice].id == id) {
      existeOrden = true;
      break;
    }

    indice++;
  }

  // Se verifica si ya existe o no
  if (existeOrden) {
    console.log("ENTRÓ A LA FUNCION SI EXISTE EL PLATILLO EN LA ORDEN");

    // Se obtiene la orden
    ordenExistente = document.getElementById("ordenP" + id);

    ordenP[indice].subtotal += subtotal;
    ordenP[indice].cantidad += parseInt(cant.value);

    ordenExistente.innerHTML =
      "<span>" +
      nombre +
      "</span><div class='detalleorden'><span>Subtotal: C$" +
      ordenP[indice].subtotal +
      "</span><span style='margin-left: auto;''>Cantidad: " +
      ordenP[indice].cantidad +
      "</span></div ><div class='botonQuitar' onclick='quitarOrden(" +
      ordenP[indice].id +
      ", " +
      ordenP[indice].subtotal +
      ")'><button class='btnQuitar'>Quitar</button></div>";
  } else {
    ordenP.push({
      id: id,
      subtotal: subtotal,
      cantidad: parseInt(cant.value),
    });

    // Se habilita el botón de agregar orden
    let btnAgregarOrden = document.getElementById("btnAgregarOrden");
    btnAgregarOrden.disabled = false;

    // Se crea el div
    var tempDiv = document.createElement("div");

    // Se le añade una clase
    tempDiv.classList.add("orden", "animate__animated", "animate__fadeIn");

    // Se asigna un id a la orden
    tempDiv.id = "ordenP" + id;

    tempDiv.innerHTML =
      "<span>" +
      nombre +
      "</span><div class='detalleorden'><span>Subtotal: C$" +
      subtotal +
      "</span><span style='margin-left: auto;''>Cantidad: " +
      cant.value +
      "</span></div ><div class='botonQuitar'><button class='btnQuitar' onclick='quitarOrden(" +
      id +
      ", " +
      subtotal +
      ")'>Quitar</button></div>";

    contOrdenes.appendChild(tempDiv);

    cantOrdenes += 1;

    /* Se verifica si hay más de un platillo */
    notiPlatillos();
  }

  // console.log(ordenP);

  calcularTotal(1, subtotal);

  validarMostrarEmptyStateCrearOrden();
}

function notiPlatillos() {
  let noti = document.getElementById("notiPlatillosOrden");

  const contenedor = document.getElementById("cuerpo_ordenes");
  const cantOrdenes = contenedor.querySelectorAll(".orden").length;

  let newWidth = window.innerWidth;

  if (newWidth < 730) {
    if (cantOrdenes > 0) {
      noti.style.display = "inline-block";
      noti.textContent = cantOrdenes;
    } else {
      noti.style.display = "none";
    }
  }
  else
  {
    noti.style.display = "none";
  }
}

var total = 0;

function calcularTotal(tipo, subtotal) {
  let LabelTotal = document.getElementById("preciototal");

  // console.log(LabelTotal);

  if (tipo == 1) {
    // Si es de tipo 1 entonces se está agregando
    total += subtotal;

    // console.log(total);

    // console.log(parseInt(LabelTotal.value))

    // Se va aumentando el valor del total sumandole el subtotal
    LabelTotal.innerHTML = total;
  }
}

/* SE LIMPIAN LAS ORDENES */

function limpiarOrdenes() {
  let cuerpo_ordenes = document.getElementById("cuerpo_ordenes");
  let LabelTotal = document.getElementById("preciototal");

  ordenP.forEach(function (elemento) {
    let ordenLimpiar = document.getElementById("ordenP" + elemento.id);

    cuerpo_ordenes.removeChild(ordenLimpiar);
  });

  // Se habilita el botón de agregar orden
  let btnAgregarOrden = document.getElementById("btnAgregarOrden");
  btnAgregarOrden.disabled = true;

  ordenP = [];
  total = 0;
  cantOrdenes = 0;

  LabelTotal.innerHTML = total;

  notiPlatillos();

  validarMostrarEmptyStateCrearOrden();
}

function quitarOrden(idOrden, subtotalOrden) {
  console.log("ENTRÓ A FUNCION QUITAR ORDEN");

  let cuerpo_ordenes = document.getElementById("cuerpo_ordenes");
  let ordenQuitar = document.getElementById("ordenP" + idOrden);
  let LabelTotal = document.getElementById("preciototal");

  // Se quita la orden en la vista
  cuerpo_ordenes.removeChild(ordenQuitar);

  // Se reduce el valor del total
  total -= subtotalOrden;
  LabelTotal.innerHTML = total;

  // Se identifica el elemento de referencia a esa orden dentro del arreglo
  indice = 0;

  while (indice < ordenP.length) {
    if (ordenP[indice].id == idOrden) {
      // Una vez encontrada la orden procederemos a cerrar el ciclo
      break;
    }

    indice++;
  }

  // Y la eliminamos del arreglo
  ordenP.splice(indice, 1);

  // Se disminuye la cantidad de ordenes contadas
  cantOrdenes -= 1;

  if (cantOrdenes == 0) {
    // Se habilita el botón de agregar orden
    let btnAgregarOrden = document.getElementById("btnAgregarOrden");
    btnAgregarOrden.disabled = true;
  }

  console.log(ordenP);
  console.log("Cantidad de ordenes: " + cantOrdenes);

  notiPlatillos();

  validarMostrarEmptyStateCrearOrden();
}

/* PLATILLOS FILTRADOS */
let temporizadorFiltrar = null;

function debouncedFiltrarPlatillos(cadena) {
  // Limpia cualquier temporizador anterior
  clearTimeout(temporizadorFiltrar);

  // Establece uno nuevo: espera 500ms después de que el usuario deje de escribir
  temporizadorFiltrar = setTimeout(() => {
    filtrarPlatillos(cadena);
  }, 500);
}

document
  .getElementById("accionesBusqueda")
  .addEventListener("change", function (event) {
    if (event.target.type === "checkbox" && event.target.checked) {
      const checkboxes = this.querySelectorAll('input[type="checkbox"]');

      // Desmarcamos todos los que NO sean el actual
      checkboxes.forEach((cb) => {
        if (cb !== event.target) {
          cb.checked = false;
        }
      });
    }

    const texto = document.getElementById("InputBuscarPlatillo").value || "";
    debouncedFiltrarPlatillos(texto);
  });

function obtenerTiposSeleccionados() {
  const checkboxes = document.querySelectorAll(
    '#accionesBusqueda input[type="checkbox"]:checked'
  );
  const tiposSeleccionados = Array.from(checkboxes).map(
    (checkbox) => checkbox.value
  );
  
  return tiposSeleccionados;
}

function filtrarPlatillos(cadena) {
  const tiposSeleccionados = obtenerTiposSeleccionados();

  // Une los IDs con comas para enviarlos en un solo parámetro URL.
  const tiposParam = tiposSeleccionados.join(",");

  let request = new XMLHttpRequest();

  const url = `/BuscarPlatillo?InputBuscarPlatillo=${encodeURIComponent(
    cadena
  )}&TiposSeleccionados=${encodeURIComponent(tiposParam)}`;

  // data.append('InputBuscarPlatillo', cadena);
  request.open("GET", url);
  request.send();
  request.onreadystatechange = function () {
    if (this.readyState == 4) {
      let contenedor = document.getElementById("VPlatillos");

      if (contenedor) {
        contenedor.innerHTML = this.responseText;
      }

      console.log(
        "Filtrado completado con texto: " + cadena + " y tipos: " + tiposParam
      );
    }
  };
}

function filtrarMesas(idAreaMesa) {
  let request = new XMLHttpRequest();
  // let data = new FormData();

  let boton = document.getElementById("btn_siguiente");
  boton.disabled = true;

  console.log(idAreaMesa);

  // data.append('InputBuscarPlatillo', idAreaMesa);
  request.open("GET", "/FiltrarMesas?listaAreasDeMesa=" + idAreaMesa);
  request.send();
  request.onreadystatechange = function () {
    if (this.readyState == 4) {
      let contenedor = document.getElementById("mesas");
      contenedor.innerHTML = this.responseText;

      cambioTipoDeSeleccion(combinarCheckbox);
    }
  };
}

/**************************************************************/
/**************************************************************/
/********************* C R E A R  O R D E N************************/
/**************************************************************/
/**************************************************************/

async function agregarOrden() {
  const { value: descripcion, isConfirmed } = await Swal.fire({
    title: "¿Realmente desea crear la orden?",
    input: "text",
    inputPlaceholder: "Agrega una descripción a tu orden (opcional)",
    inputAttributes: {
      maxlength: 150,
    },
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Crear orden",
    confirmButtonColor: "#ff6464",
    icon: "question",
    iconColor: "#ff964e",
    reverseButtons: true,
    didOpen: () => {
      const input = Swal.getInput();
      if (input) input.blur();
    },
  });

  if (isConfirmed) {
    try {
      // Muestra un modal de carga mientras se envían los datos
      Swal.fire({
        title: "Creando orden...",
        text: "Por favor espere",
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading(),
      });

      const respuesta = await enviarDatos(descripcion || "");

      // Supongamos que Django responde con algo como:
      // { "status": "ok", "message": "Orden creada exitosamente" }

      if (respuesta.status === "ok") {
        await Swal.fire({
          title: respuesta.message,
          icon: "success",
          confirmButtonColor: "#ff6464",
        });
        location.reload();
      } else {
        await Swal.fire({
          title: "Error",
          text: respuesta.message || "No se pudo crear la orden.",
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
}

// Funcion para mandar los datos al views
function enviarDatos(descripcion) {
  return new Promise((resolve, reject) => {
    let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/CrearOrden/", true);

    // Obtener las mesas seleccionadas
    let mesas = document.getElementsByName("mesa");
    if (mesas.length === 0) mesas = document.getElementsByName("mesas_check");

    let listaMesasSeleccionadas = [];
    for (let i = 0; i < mesas.length; i++) {
      if (mesas[i].checked) listaMesasSeleccionadas.push(mesas[i].value);
    }

    // Crear los datos del formulario
    let datos = new FormData();
    datos.append("OrdenPlatillos", JSON.stringify(ordenP));
    datos.append("csrfmiddlewaretoken", token);
    datos.append("mesas", JSON.stringify(listaMesasSeleccionadas));
    datos.append("descripcion", descripcion);
    datos.append("total", total);

    // Manejamos la respuesta del servidor
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          try {
            let respuesta = JSON.parse(xhr.responseText);
            resolve(respuesta); // se devuelve el resultado al .then()
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

function abrirCarrito() {
  /* Se obtiene el elemento con el id 'opciones' */
  var carrito = document.getElementById("Ordenes");
  var capa = document.getElementById("capaventas");

  /*Hacemos aparecer la capa y las opciones*/
  capa.style.display = "initial";
  carrito.style.display = "initial";

  // Se eliminan las clases por si se habían añadido antes, todo es para tener un orden
  capa.classList.remove("animate__animated", "animate__fadeOut");

  // Se establece la duración de la animación
  capa.style.setProperty("--animate-duration", "0.3s");

  // Se asigna la clase de animación a la capa
  capa.classList.add("animate__animated", "animate__fadeIn");

  /*******************************************************************************************/

  // Lo mismo para el objeto ;opciones;
  carrito.classList.remove("animate__animated", "animate__fadeIn");
  carrito.classList.remove("animate__animated", "animate__fadeOutRight");
  carrito.style.setProperty("--animate-duration", "0.5s");
  carrito.classList.add("animate__animated", "animate__fadeInRight");

  /* Se mueve el objeto 300px a la derecha */
  // opciones.style.transform = "translateX(0px)";
}

function cerrarCarrito() {
  /* Se obtiene el elemento con el id 'opciones' */
  var carrito = document.getElementById("Ordenes");
  var capa = document.getElementById("capaventas");

  // Se eliminan las clases por si se habían añadido antes, todo es para tener un orden
  carrito.classList.remove("animate__animated", "animate__fadeInRight");
  carrito.classList.remove("animate__animated", "animate__fadeIn");

  // Se establece la duración del objeto 'opciones'
  carrito.style.setProperty("--animate-duration", "0.5s");

  // Se asigna la clase de animación al objeto 'opciones'
  carrito.classList.add("animate__animated", "animate__fadeOutRight");

  /*******************************************************************************************/

  // Lo mismo para la capa
  capa.classList.remove("animate__animated", "animate__fadeIn");
  capa.style.setProperty("--animate-duration", "0.3s");
  capa.classList.add("animate__animated", "animate__fadeOut");

  /* Se mueve el objeto 300px a la derecha */
  // opciones.style.transform = "translateX(-305px)";

  /*Hacemos aparecer la capa*/
  setTimeout(() => {
    capa.style.display = "none";
  }, 500);
}

window.addEventListener("resize", function () {
  let newWidth = window.innerWidth;

  let carrito = document.getElementById("Ordenes");

  let noti = document.getElementById("notiPlatillosOrden");

  if (newWidth >= 730) {
    cerrarCarrito();
    Restablecer();

    noti.style.display = "none";
  } else if (newWidth < 730) {
    carrito.style.display = "none";
    notiPlatillos();
  }
});

function Restablecer() {
  carrito = document.getElementById("Ordenes");

  carrito.style.display = "initial";

  carrito.classList.remove("animate__animated", "animate__fadeInRight");

  carrito.classList.remove("animate__animated", "animate__fadeOutRight");

  carrito.classList.add("animate__animated", "animate__fadeIn");
}
