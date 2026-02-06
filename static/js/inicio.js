document.addEventListener("DOMContentLoaded", function () {
  $.ajax({
    url: "/GraficaOrdenes/",
    dataType: "json",
    success: function (data) {
      console.log(data);
      Chart.defaults.locale = "es";
      var ctx = document.getElementById("myChart").getContext("2d");

      // Crear el gradiente para el área debajo de la línea
      var gradient = ctx.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, "rgba(255, 99, 132, 0.5)"); // Color principal (rojo/naranja de tu Figma)
      gradient.addColorStop(1, "rgba(255, 255, 255, 0)");

      var myChart = new Chart(ctx, {
        type: "line", // CAMBIADO de 'bar' a 'line'
        data: {
          labels: data.dias_semana,
          datasets: [
            {
              label: "Ingresos Diarios (C$)",
              data: data.ingresos_v, // Usamos el nuevo array de montos
              fill: true,
              backgroundColor: gradient,
              borderColor: "#FF6384", // El color de la línea
              borderWidth: 3,
              tension: 0.4, // Esto hace que la línea sea curva como en Figma
              pointRadius: 5,
              pointBackgroundColor: "#FF6384",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }, // Ocultar leyenda para limpiar el diseño
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                // Formatear como moneda
                callback: function (value) {
                  return "C$" + value.toLocaleString();
                },
              },
            },
          },
        },
      });

      // Gráfico de pastel para los 5 platillos más vendidos
      var pieCtx = document.getElementById("pieChart").getContext("2d");
      var pieChart = new Chart(pieCtx, {
        type: "pie",
        data: {
          labels: data.platillos_nombres,
          datasets: [
            {
              data: data.num_ventas_platillos,
              backgroundColor: [
                "#FF6384",
                "#36A2EB",
                "#FFCE56",
                "#4BC0C0",
                "#9966FF",
              ],
              hoverBackgroundColor: [
                "#FF6384",
                "#36A2EB",
                "#FFCE56",
                "#4BC0C0",
                "#9966FF",
              ],
            },
          ],
        },
        options: {
          responsive: true,
        },
      });
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
          title: "¡Protege tu cuenta! Cambia tu contraseña temporal por una propia",
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