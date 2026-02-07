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
          labels: data.dias_semana,
          datasets: [
            {
              label: "Ingresos (C$)",
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
                "#B86D3E", // Café
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

      document.getElementById("card-hoy-total").innerText =
        "C$" + data.resumen.hoy_total.toLocaleString();
      document.getElementById("card-hoy-propinas").innerText =
        "C$" + data.resumen.hoy_propinas.toLocaleString();
      document.getElementById("card-mes-total").innerText =
        "C$" + data.resumen.mes_total.toLocaleString();
      document.getElementById("card-mes-propinas").innerText =
        "C$" + data.resumen.mes_propinas.toLocaleString();
    },
  });

  ConsultaDebeCambiarPass();
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
