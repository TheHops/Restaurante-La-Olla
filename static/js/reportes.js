const fechaDesde = document.getElementById("fechaDesde");
const fechaHasta = document.getElementById("fechaHasta");
const errorFechas = document.getElementById("errorFechas");

function validarFechas() {
  if (!fechaDesde.value || !fechaHasta.value) {
    errorFechas.style.display = "none";
    return false;
  }

  const desde = new Date(fechaDesde.value);
  const hasta = new Date(fechaHasta.value);

  if (desde > hasta) {
    errorFechas.style.display = "block";
    fechaHasta.setCustomValidity("Fecha inválida");
    return false;
  }

  errorFechas.style.display = "none";
  fechaHasta.setCustomValidity("");
  return true;
}

fechaDesde.addEventListener("change", () => {
  if(validarFechas()) filtrarOrdenesFecha();
});
fechaHasta.addEventListener("change", () => {
  if (validarFechas()) filtrarOrdenesFecha();
});

function filtrarOrdenesFecha(){
  console.log("FECHA VALIDA");
}