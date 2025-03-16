                        let data = {
                                labels: [
                                  '',
                                ],
                                datasets: [{
                                  label: 'Projected Spread',
                                  data: ["{{ pmscore }}"],


                                  backgroundColor: [

                                  {% if finished%}
                                    {% if pmscore >= 0 and winner == 1 or pmscore < 0 and winner == 0 %}
                                      'rgb(65, 199, 8)',
                                    {%else%}
                                      'rgb(255, 0, 0)',

                                    {% endif %} 
                                  {% endif %}

                                  {%if not finished%}
                                  '#8d8f8f',
                                  {% endif %}


                                    

                                  ],
                                  hoverOffset: 10,

                                  borderWidth: 1,

                                
                                }]
                              };


                          let config{{game.pk }} = {
                              type: 'bar',
                              data: data{{game.pk }},
                              options: {
                                maintainAspectRatio: false,
                                  responsive: true,
                                  reverse: true,

                                  start: 0,
                                  end: 0,
                                  begin: 1,
                                  base: 0,
                                  middle: 0,
                                  indexAxis: 'y',
                                  plugins: {
                                      legend: {
                                        display: false
                                      }
                                    },
                                    layout: {
                                      padding: {
                                          // Any unspecified dimensions are assumed to be 0                     
                                          top: 5,
                                          bottom: 5,
                                          left: 5,
                                          right: 5,
                                      }
                                  },
                                  yAxes: [{
                                      type: 'time',
                                      ticks: {
                                          autoSkip: true,
                                          maxTicksLimit: 1
                                      }
                                }],
                                  scales: {
                                    x: {
                                      min: -10,
                                      max: 10,
                                      ticks: {
                                          autoSkip: true,
                                          maxTicksLimit: 4
                                      },
                                    


                                    },
                                    y: {
                                      min: 0,
                                      max: 1,
                                      
                                      weight: 1,

                                    }
                                  }
                                  }

                            };

                            const c = new Chart(document.getElementById('c'),config);

      document.addEventListener("DOMContentLoaded", function() {
          var ctx = document.getElementById('vegasOddsChart').getContext('2d');
          new Chart(ctx, {
              type: 'bar',
              data: {
                  labels: [{% for line in complexSpread %}'{{ line.name }}',{% endfor %}],
                  datasets: [{
                      label: 'Home Spread',
                      data: [{% for line in complexSpread %}{{ line.homeTeamSpread }},{% endfor %}],
                      backgroundColor: 'rgba(255, 99, 132, 0.2)',
                      borderColor: 'rgba(255, 99, 132, 1)',
                      borderWidth: 1,
                      yAxisID: 'y-axis-spread',
                  }, {
                      label: 'Visitor Spread',
                      data: [{% for line in complexSpread %}{{ line.awayTeamSpread }},{% endfor %}],
                      backgroundColor: 'rgba(54, 162, 235, 0.2)',
                      borderColor: 'rgba(54, 162, 235, 1)',
                      borderWidth: 1,
                      yAxisID: 'y-axis-spread',
                  }, {
                      label: 'Home Money Line',
                      data: [{% for line in complexSpread %}{{ line.homeTeamMLOdds }},{% endfor %}],
                      type: 'bar',
                      backgroundColor: 'rgba(75, 192, 192, 0.2)',
                      borderColor: 'rgba(75, 192, 192, 1)',
                      borderWidth: 1,
                      yAxisID: 'y-axis-ml',
                  }, {
                      label: 'Visitor Money Line',
                      data: [{% for line in complexSpread %}{{ line.awayTeamMLOdds }},{% endfor %}],
                      type: 'bar',
                      backgroundColor: 'rgba(153, 102, 255, 0.2)',
                      borderColor: 'rgba(153, 102, 255, 1)',
                      borderWidth: 1,
                      yAxisID: 'y-axis-ml',
                  }]
              },
              options: {
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                      'y-axis-spread': {
                          type: 'linear',
                          display: true,
                          position: 'left',
                          title: {
                              display: true,
                              text: 'Spread'
                          }
                      },
                      'y-axis-ml': {
                          type: 'linear',
                          display: true,
                          position: 'right',
                          title: {
                              display: true,
                              text: 'Money Line'
                          },
                          grid: {
                              drawOnChartArea: false,
                          },
                      }
                  }
              }
          });
      });

          var radarlabels = ['Projection ML Away'];
          var projectedML = convertPMScoreToML({{ pmscore }});
          var radardata = [projectedML];

          {% for line in complexSpread %}
          {% if line.awayTeamSpread != 0 %}
          radarlabels.push("{{ line.name }}");
          radardata.push(Math.abs({{ line.awayTeamMLOdds }}));
          {% endif %}
          {% endfor %}

          radardata = radardata.map(value => Math.round(Math.abs(value)));

          // Define a dynamic color palette for the dataset
          const colors = [
              'rgba(255, 159, 64, 0.2)' , // Orange
              'rgba(255, 99, 132, 0.2)', // Red
              'rgba(54, 162, 235, 0.2)', // Blue
              'rgba(255, 206, 86, 0.2)', // Yellow
              'rgba(75, 192, 192, 0.2)', // Green
              'rgba(153, 102, 255, 0.2)', // Purple
          ];
          const borderColors = [
              'rgb(255, 159, 64)',  // Orange
              'rgb(255, 99, 132)', // Red
              'rgb(54, 162, 235)', // Blue
              'rgb(255, 206, 86)', // Yellow
              'rgb(75, 192, 192)', // Green
              'rgb(153, 102, 255)', // Purple
          ];

          // Generate colors for each point
          let backgroundColors = [];
          let pointBorderColors = [];
          radardata.forEach((_, index) => {
              backgroundColors.push(colors[index % colors.length]);
              pointBorderColors.push(borderColors[index % borderColors.length]);
          });

          const radarconfig = {
              type: 'radar',
              data: {
                  labels: radarlabels,
                  datasets: [{
                      label: 'Moneyline Odds',
                      data: radardata,
                      fill: true,
                      backgroundColor: backgroundColors, // Apply unique colors to each point
                      borderColor: pointBorderColors,
                      pointBackgroundColor: pointBorderColors,
                      pointBorderColor: '#fff',
                      pointHoverBackgroundColor: '#fff',
                      pointHoverBorderColor: pointBorderColors,
                      borderWidth: 2
                  }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,

                  elements: {
                      line: {
                          tension: 0.3 // Smooths the lines
                      },
                      point: {
                          radius: 4 // Adjusts point size
                      }
                  },
                  scale: {
                      ticks: {
                          display: true,
                          beginAtZero: true,
                          suggestedMax: Math.max(...radardata) + 500, // Adjust for your data
                          stepSize: 500
                      },
                      pointLabels: {
                          fontSize: 16,
                          fontColor: 'rgb(54, 162, 235)'
                      }
                  }
              },
          };

         // Initialize the radar chart
    // Initialize the radar chart
    new Chart(document.getElementById('radarChart'), radarconfig);
    function convertPMScoreToML(pointSpread) {
      // Approximations based on general observations
      if (pointSpread >= 1 && pointSpread <= 2) {
          return -130; // Example for spreads 1 to 2 points
      } else if (pointSpread >= 2.5 && pointSpread <= 3.5) {
          return -160; // Example for spreads 2.5 to 3.5 points
      } else if (pointSpread >= 4 && pointSpread <= 5) {
          return -190; // Example for spreads 4 to 5 points
      } else if (pointSpread >= 5.5 && pointSpread <= 6.5) {
          return -220; // Example for spreads 5.5 to 6.5 points
      } else if (pointSpread >= 7 && pointSpread <= 8) {
          return -260; // Example for spreads 7 to 8 points
      } else if (pointSpread >= 8.5 && pointSpread <= 9.5) {
          return -300; // Example for spreads 8.5 to 9.5 points
      } else if (pointSpread >= 10) {
          return -350; // Example for spreads 10 points and above
      } else {
          return 100; // Flat return for underdogs or as a default (should ideally handle underdogs differently)
      }
  }

  window.addEventListener('resize', () => {
  resizeChart(radarChart, 2);
  resizeChart(totalPointsChart, 2);
});
function resizeChart(chart, aspectRatio = 2) {
  const container = chart.canvas.parentNode;
  const width = container.clientWidth;
  const height = width / aspectRatio;
  chart.canvas.style.width = width + 'px';
  chart.canvas.style.height = height + 'px';
  chart.resize();
}

  var totalPointsLabels = ['Projection Total Points'];
  var projectedTotalPoints = {{ phscore }}+{{pvscore}}; // Assuming pmscore can represent a total points projection
  var totalPointsData = [projectedTotalPoints];

  {% for line in complexSpread %}
  {% if line.awayTeamSpread != 0 %}
  totalPointsLabels.push("{{ line.name }}");
  totalPointsData.push({{ line.totalUnder }});
  {% endif %}
  {% endfor %}

  totalPointsData = totalPointsData.map(value => Math.round(Math.abs(value))); // Ensure all values are rounded and positive

  // Adapt colors for total points chart or reuse from the radar chart setup
  let totalPointsBackgroundColors = [];
  let totalPointsBorderColors = [];
  totalPointsData.forEach((_, index) => {
      totalPointsBackgroundColors.push(colors[index % colors.length]);
      totalPointsBorderColors.push(borderColors[index % borderColors.length]);
  });

  const totalPointsConfig = {
      type: 'radar', // Or 'bar' if you prefer a bar chart for total points
      data: {
          labels: totalPointsLabels,
          datasets: [{
              label: 'Total Points',
              data: totalPointsData,
              fill: true,
              backgroundColor: totalPointsBackgroundColors,
              borderColor: totalPointsBorderColors,
              pointBackgroundColor: totalPointsBorderColors,
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: totalPointsBorderColors,
              borderWidth: 2
          }]
      },
      options: {
        responsive: true,
          maintainAspectRatio: false,

          elements: {
              line: {
                  tension: 0.3
              },
              point: {
                  radius: 4
              }
          },
          scale: {
              ticks: {
                  display: true,
                  suggestedMax: Math.max(...totalPointsData) ,
                  stepSize: 1000
              },
              pointLabels: {
                  fontSize: 14,
                  fontColor: 'rgb(54, 162, 235)'
              }
          }
      },
  };

  new Chart(document.getElementById('totalPointsChart'), totalPointsConfig);

        function hh() {
          var x = document.getElementById("hh-table");
          var hh_btn = document.getElementById("hh-btn");
          if (x.style.display === "none") {
            hh_btn.value = "Hide Stats"
            x.style.display = "block";
          } else {
            hh_btn.value = "Show Stats"
            x.style.display = "none";
          }
        }
        function vh() {
          var x = document.getElementById("vh-table");
          var hh_btn = document.getElementById("vh-btn");
          if (x.style.display === "none") {
            hh_btn.value = "Hide Stats"
            x.style.display = "block";
          } else {
            hh_btn.value = "Show Stats"
            x.style.display = "none";
          }
        }

                  document.getElementById("retrain-strength").addEventListener("input", () => {
                  var sliderValue = document.getElementById("retrain-strength").value;
                  document.getElementById("retrain-display").innerHTML = sliderValue + '%';

                  // Update the button's href to include the slider value as a query parameter
                  var baseUrl = "{%url 'retrain-model' pk %}";
                  document.getElementById("retrain-button").href = baseUrl + '?strength=' + sliderValue;
              });

        var changes = "change=";
        var asdf =""
        editing = false

        document.body.addEventListener('click', function (event) {
          console.log('click')

        var press = jQuery.Event("keypress");
        press.ctrlKey = false;
        press.which = 13;
        $(".e").trigger(press);
        console.log(changes)

        })



        $(function(){
            $(".e").click(function(event){
                if(!editing){
                  editing=true;
                  if($(this).children("input").length > 0)
                      return false;
                  f = $(this).attr("id");
                  var tdObj = $(this);
                  asdf = tdObj
                  lastObj = tdObj
                  var preText = tdObj.html();
                  var inputObj = $("<input type='number' id='asdf'/>");
                  tdObj.html("");
                  inputObj.width(tdObj.width())
                      .height(tdObj.height())
                      .css({border:"0px",fontSize:"17px"})
                      .val(preText)
                      .appendTo(tdObj)
                      .trigger("focus")
                      .trigger("select");

                  inputObj.keyup(function(event){
                      if(13 == event.which) { // press ENTER-key
                          var text = $(this).val();
                          tdObj.html(text);
                          changes += f+":"+$(this).val()+"-";
                          editing=false;
                      }

                      else if(27 == event.which) {  // press ESC-key
                          tdObj.html(preText);
                          editing=false;

                      }

                    });



                  inputObj.click(function(){
                      return false;
                  });
            }

            });
        });

        function myFunction() {
            window.location.href = document.getElementById("model-slot").value +'/'+changes;

        }
