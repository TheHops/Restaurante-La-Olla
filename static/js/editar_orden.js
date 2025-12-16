function rellenarParaEditarOrden(idOrden) {
  let request = new XMLHttpRequest();

  const url = `/InicioEditar?IdOrden=${idOrden}`;

  // data.append('InputBuscarPlatillo', cadena);
  request.open("GET", url);
  request.send();
  request.onreadystatechange = function () {
    if (this.readyState == 4) {
      let contenedor = document.getElementById("contenidoDetalleOrden");

      if (contenedor) {
        contenedor.innerHTML = this.responseText;
      }
    }
  };
}
