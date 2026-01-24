document.addEventListener("DOMContentLoaded", function () {
  $.ajax({
    url: "/GraficaOrdenes/",
    dataType: "json",
    success: function (data) {
      console.log(data);
      Chart.defaults.locale = "es";
      var ctx = document.getElementById("myChart").getContext("2d");
      var gradient = ctx.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, "rgba(184,109,62,1)");
      gradient.addColorStop(1, "rgba(254,218,162, 0.3)");

      console.log(data);

      var myChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.dias_semana,
          datasets: [
            {
              label: "Facturas por día de la semana",
              data: data.num_facturas,
              fill: true,
              backgroundColor: gradient,
              borderColor: "#fff",
              pointBackgroundColor: "“#fff",
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function (value) {
                  if (Number.isInteger(value)) {
                    return value;
                  }
                  return "";
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