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