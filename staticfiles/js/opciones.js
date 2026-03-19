function abrir() {
  /* Se obtiene el elemento con el id 'opciones' */
  var opciones = document.getElementById("opciones");
  var capa = document.getElementById("capa");

  /*Hacemos aparecer la capa y las opciones*/
  capa.style.display = "initial";
  opciones.style.display = "flex";
  opciones.style.flexDirection = "column";
  opciones.style.alignItems = "center";

  // Se eliminan las clases por si se habían añadido antes, todo es para tener un orden
  capa.classList.remove("animate__animated", "animate__fadeOut");

  // Se establece la duración de la animación
  capa.style.setProperty("--animate-duration", "0.3s");

  // Se asigna la clase de animación a la capa
  capa.classList.add("animate__animated", "animate__fadeIn");

  /*******************************************************************************************/

  // Lo mismo para el objeto ;opciones;
  opciones.classList.remove("animate__animated", "animate__fadeOutLeft");
  opciones.style.setProperty("--animate-duration", "0.5s");
  opciones.classList.add("animate__animated", "animate__fadeInLeft");

  /* Se mueve el objeto 300px a la derecha */
  // opciones.style.transform = "translateX(0px)";
}

function cerrar() {
  /* Se obtiene el elemento con el id 'opciones' */
  var opciones = document.getElementById("opciones");
  var capa = document.getElementById("capa");

  // Se eliminan las clases por si se habían añadido antes, todo es para tener un orden
  opciones.classList.remove("animate__animated", "animate__fadeInLeft");

  // Se establece la duración del objeto 'opciones'
  opciones.style.setProperty("--animate-duration", "0.5s");

  // Se asigna la clase de animación al objeto 'opciones'
  opciones.classList.add("animate__animated", "animate__fadeOutLeft");

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

function abrirCapa() {
  var capa = document.getElementById("capa");

  /*Hacemos aparecer la capa y las opciones*/
  capa.style.display = "initial";

  // Se eliminan las clases por si se habían añadido antes, todo es para tener un orden
  capa.classList.remove("animate__animated", "animate__fadeOut");

  // Se establece la duración de la animación
  capa.style.setProperty("--animate-duration", "0.3s");

  // Se asigna la clase de animación a la capa
  capa.classList.add("animate__animated", "animate__fadeIn");
}

function cerrarCapa() {
  var capa = document.getElementById("capa");

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

/*-----------------------------------------------------------------------------*/

function calcularAltoTabla() {
  // 1. Obtenemos el alto total de la ventana (viewport)
  let altoVentana = window.innerHeight;

  // 2. Obtenemos la distancia desde el tope de la página hasta tu tabla
  // Si la tabla no existe aún, usamos un valor por defecto
  let tablaElemento = document.querySelector(".tablaInventario");
  let offsetTop = tablaElemento
    ? tablaElemento.getBoundingClientRect().top
    : 200;

  // 3. Calculamos: Alto total - lo que ya ocupan los headers/filtros - margen de seguridad (ej. 100px)
  let altoDisponible = altoVentana - offsetTop - 250;

  // Retornamos mínimo 300px para que no desaparezca en pantallas ultra pequeñas
  return altoDisponible > 300 ? altoDisponible + "px" : "43vh";
}

let table = $(".tablaInventario").DataTable({
  scrollY: calcularAltoTabla(), // <--- Aquí llamamos a la función
  scrollCollapse: true,
  paging: true,
  language: {
    url: "/static/json/es-ES.json",
  },
});