$(document).ready(function() {

var popCanvas = document.getElementById("popChart");
var barChart = new Chart(popCanvas, {
  type: 'bar',
  data: {
    labels: ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    datasets: [{
      label: 'Population',
      data: [500, 120, 95, 50, 300, 240, 170],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 206, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
        'rgb(255, 159, 64)',
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
      ]
    }]
  }
});


});

