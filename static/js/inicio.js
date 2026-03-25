document.addEventListener("DOMContentLoaded", function () {
  $.ajax({
    url: "/GraficaOrdenes/",
    dataType: "json",
    success: function (data) {
      Chart.defaults.locale = "es";

      // --- 1. CONFIGURACIÓN GRÁFICO DE LÍNEAS (VENTAS) ---
      var ctx = document.getElementById("myChart").getContext("2d");
      var gradient = ctx.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, "rgba(255, 99, 132, 0.4)");
      gradient.addColorStop(1, "rgba(255, 255, 255, 0)");

      new Chart(ctx, {
        type: "line",
        data: {
          labels: data.labels_x,
          datasets: [
            {
              label: "Total (C$)",
              data: data.ingresos_v,
              fill: true,
              backgroundColor: gradient,
              borderColor: "#FF6384", // Color café de "La Olla"
              borderWidth: 3,
              tension: 0.4,
              pointRadius: 4,
              pointBackgroundColor: "#FF6384",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => "C$" + value.toLocaleString(),
              },
            },
          },
        },
      });

      // --- 2. CONFIGURACIÓN GRÁFICO DE DONA (MÉTODOS DE PAGO) ---
      var pieCtx = document.getElementById("pieChart").getContext("2d");
      new Chart(pieCtx, {
        type: "doughnut", // Cambiado a dona para coincidir con Figma
        data: {
          labels: data.metodos_labels, // Ahora usa los métodos de pago
          datasets: [
            {
              data: data.metodos_valores,
              backgroundColor: [
                "#FF6384", // Rosa/Rojo principal
                "#FEDA62", // Amarillo/Naranja de tu Figma
                "#ffa500", // Naranja
                "#4BC0C0", // Cyan
                "#66ff70", // verde
              ],
              borderWidth: 2,
              hoverOffset: 10,
            },
          ],
        },
        options: {
          responsive: true,
          cutout: "70%", // Esto hace que el "hoyo" sea más grande, muy estilo moderno
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                usePointStyle: true,
                padding: 20,
              },
            },
          },
        },
      });

      if (data.resumen) {
        $("#card-hoy-total").text("C$" + data.resumen.hoy_total.toLocaleString());
        $("#card-hoy-propinas").text("C$" + data.resumen.hoy_propinas.toLocaleString());
        $("#card-mes-total").text("C$" + data.resumen.mes_total.toLocaleString());
        $("#card-mes-propinas").text("C$" + data.resumen.mes_propinas.toLocaleString());
        $("#card-mes-gran-total").text("C$" + data.resumen.mes_gran_total.toLocaleString());
        $("#card-mes-cantidad-ordenes").text(data.resumen.mes_cantidad_ordenes);
      }

      // 2. Llenar Cards de Cajero
      if (data.cajero_stats) {
        $("#cajero-efectivo-total").text("C$" + data.cajero_stats.hoy_efectivo_total.toLocaleString());
        $("#cajero-efectivo-propina").text("C$" + data.cajero_stats.hoy_efectivo_propina.toLocaleString());
        $("#cajero-tarjeta-total").text("C$" + data.cajero_stats.hoy_tarjeta_total.toLocaleString());
        $("#cajero-tarjeta-propina").text("C$" + data.cajero_stats.hoy_tarjeta_propina.toLocaleString());
      }
    },
  });

  ConsultaDebeCambiarPass();
});

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
