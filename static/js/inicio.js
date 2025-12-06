$(document).ready(function () {
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

      var myChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
          ],
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
});
