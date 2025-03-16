const labels = ['Fanduel', 'DraftKings', 'BetMGM', 'Caesars'];
const data = {
  labels: labels,
  datasets: [
    {
      label: 'Trend',
      data: [65, -59, 80, -81],
      borderColor: "#fc861e",
      backgroundColor: 'rgba(252, 134, 30, 0.5)',
      borderWidth: 2,
      borderRadius: Number.MAX_VALUE,
      borderSkipped: false,
      barPercentage: 0.5,
      categoryPercentage: 0.5,
    },
    {
      label: 'Trend',
      data: [28, 48, 40, 19],
      backgroundColor: 'rgba(54, 162, 235, 0.5)',
      borderColor: 'rgb(54, 162, 235)',
      borderWidth: 2,
      borderRadius: 5,
      borderSkipped: false,
      barPercentage: 0.5,
      categoryPercentage: 0.5,
    }
  ]
};

const config = {
  type: 'bar',
  data: data,
  options: {
    indexAxis: 'y',
    scales: {
      x: {
        beginAtZero: true,
      }
    },
    plugins: {
      legend: {
        display: false,
      }
    }
  },
};

var myChart = new Chart(document.getElementById('myChart'), config);
