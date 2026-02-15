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

/** * * * * * * * * AUTO DROPDOWN * * * * * * * * * **/

const dropdown = document.getElementById("dropdownInventario");
const trigger = dropdown.querySelector(".dropdown-trigger");
const menu = dropdown.querySelector(".dropdown-menu");
const links = dropdown.querySelectorAll(".dropdown-menu a");

// Abrir cuando el botón recibe el foco (Teclado)
trigger.addEventListener("focus", () => {
  dropdown.classList.add("is-active");
});

// Cerrar si el usuario presiona la tecla Escape
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    dropdown.classList.remove("is-active");
    trigger.blur(); // Quita el foco del botón
  }
});

// Cerrar si el foco sale del menú completo (Tab fuera del último link)
dropdown.addEventListener("focusout", (e) => {
  // Si el nuevo elemento con foco NO está dentro del dropdown, cerramos
  if (!dropdown.contains(e.relatedTarget)) {
    dropdown.classList.remove("is-active");
  }
});

// Función para cerrar
const closeMenu = () => {
  dropdown.classList.remove("is-active");
  trigger.setAttribute("aria-expanded", "false");
};

// Abrir al enfocar el botón
trigger.addEventListener("focus", () => {
  dropdown.classList.add("is-active");
  trigger.setAttribute("aria-expanded", "true");
});

// Manejo de teclas
dropdown.addEventListener("keydown", (e) => {
  const items = Array.from(links);
  const currentIndex = items.indexOf(document.activeElement);

  if (e.key === "ArrowDown") {
    e.preventDefault();
    // Si estamos en el botón, vamos al primer item. Si no, al siguiente.
    const nextIndex = (currentIndex + 1) % items.length;
    items[nextIndex].focus();
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    // Si estamos en el primero, vamos al último.
    const prevIndex = (currentIndex - 1 + items.length) % items.length;
    items[prevIndex].focus();
  } else if (e.key === "Escape") {
    closeMenu();
    trigger.focus();
  }
});

// Cerrar si el mouse sale o el foco se va a otro lado de la página
dropdown.addEventListener("mouseleave", closeMenu);
dropdown.addEventListener("focusout", (e) => {
  if (!dropdown.contains(e.relatedTarget)) {
    closeMenu();
  }
});