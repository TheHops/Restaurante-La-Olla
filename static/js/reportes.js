document.getElementById("fechaDesde").addEventListener("change", function () {
  document.getElementById("labelDesde").textContent = this.value
    ? formatearFecha(this.value)
    : "- - - -";
});

document.getElementById("fechaHasta").addEventListener("change", function () {
  document.getElementById("labelHasta").textContent = this.value
    ? formatearFecha(this.value)
    : "- - - -";
});

function formatearFecha(valor) {
  const fecha = new Date(valor);

  return fecha.toLocaleString("es-NI", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
