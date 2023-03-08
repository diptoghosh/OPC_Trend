$(document).ready(function () {
  // const
  const MAX_CHART_COUNT = 12;
  var context = [];
  var filteredData;
  var compOptions = [];
  var compConfig = [];
  var viewIndex = 0;
  var lineChart = [];
  const colorSet = [
    "#BCA228",
    "#15F5E0",
    "#E649E6",
    "#E64949",
    "#4E49E6",
    "#33FF55",
    "#FF3933",
    "#DDFF33",
    "#33FF90",
    "#FF33B2",
    "#33D7FF",
    "#FF7433",
  ];

  for (let i = 1; i <= MAX_CHART_COUNT; i++) {
    context[i - 1] = $("#canvas" + i)[0];
  }

  for (let i = 1; i <= MAX_CHART_COUNT; i++) {
    $("#checkboxView" + i).change(() => {
      if ($("#checkboxView" + i).prop("checked")) $("#canvas" + i).show();
      else {
        $("#canvas" + i).hide();
      }
      if (compConfig.length >= i) {
        compConfig[i - 1].show = $("#checkboxView" + i).prop("checked");
      } else {
        compConfig.push({ signalName: "Dummy", min: 0, max: 0, show: true });
      }
      localStorage.setItem("SignalConfig", JSON.stringify(compConfig));
      cleanupTrends();
      initTrendSettings();
      updateTrend();
    });

    context[i - 1] != null
      ? context[i - 1].addEventListener("dblclick", function () {
          // Some dazzling stuff happens be here
          viewIndex = i;
          $("#viewIndexSelected").text("for : View" + viewIndex);
          let modalComponents = $("#modal_components")[0];
          for (let comp = 0; comp < modalComponents.options.length; comp++) {
            if (
              modalComponents.options[comp].text ===
              compConfig[i - 1].signalName
            ) {
              modalComponents.value = compConfig[i - 1].signalName;
              $("#modal_min").val(compConfig[i - 1].min);
              $("#modal_max").val(compConfig[i - 1].max);
            } else if (compConfig[i - 1].signalName === "Dummy") {
              modalComponents.value = compConfig[i - 1].signalName;
              $("#modal_min").val(compConfig[i - 1].min);
              $("#modal_max").val(compConfig[i - 1].max);
            }
          }
          $("#configModal").modal();
        })
      : null;
  }

  autoScaleAll = () => {
    if (filteredData) {
      cleanupTrends();
      initTrendSettings((autoscale = true));
      updateTrend((autoscale = true));
    }
  }; //autoScaleAll

  loadModalData = () => {
    if (viewIndex > 0) {
      $("#modal_show").prop("checked", compConfig[viewIndex - 1].show);
    }
  }; //loadModalData

  saveTrendConfig = () => {
    if (localStorage.getItem("SignalConfig") != null) {
      compConfig[viewIndex - 1].signalName = $("#modal_components").val();
      compConfig[viewIndex - 1].min = parseFloat($("#modal_min").val());
      compConfig[viewIndex - 1].max = parseFloat($("#modal_max").val());
      compConfig[viewIndex - 1].show = $("#modal_show").prop("checked");
      localStorage.setItem("SignalConfig", JSON.stringify(compConfig));
      cleanupTrends();
      initTrendSettings();
      updateTrend();
    }
  }; //saveTrendConfig

  initTrendSettings = (autoscale = false) => {
    if (localStorage.getItem("SignalConfig") != null) {
      compConfig = JSON.parse(localStorage.getItem("SignalConfig"));
    } else {
      $.ajax({
        type: "GET",
        url: "/signal-config",
      }).done(function (data) {
        localStorage.setItem("SignalConfig", data);
        compConfig = JSON.parse(data);
      });
    }
    var visibleTrendTotal = 0;
    var visibleTrendLoop = 0;
    compConfig.forEach((item) => {
      if (item.show) visibleTrendTotal++;
    });
    console.log("visibleTrendTotal: " + visibleTrendTotal);

    compConfig.forEach((item, index) => {
      viewNum = index + 1;

      $("label[for='checkboxView" + viewNum + "']").text(item.signalName);
      $("#checkboxView" + viewNum).prop("checked", item.show);
      $("#cbBox" + viewNum + " rect").css("fill", colorSet[index]);

      if (item.show) $("#canvas" + viewNum).show();
      else $("#canvas" + viewNum).hide();

      let config = getNewConfig();
      config.options.scales.yAxes[0].scaleLabel.labelString = item.signalName;
      if (!autoscale) {
        config.options.scales.yAxes[0].ticks.min = parseFloat(
          compConfig[index].min
        );
        config.options.scales.yAxes[0].ticks.max = parseFloat(
          compConfig[index].max
        );
        // config.options.scales.yAxes[0].ticks.stepSize =
        //   (compConfig[index].max - compConfig[index].min) / 2;
        // config.options.scales.yAxes[0].ticks.fixedStepSize =
        //   (compConfig[index].max - compConfig[index].min) / 2;
      }

      if (item.show) visibleTrendLoop++;
      // if (visibleTrendTotal === visibleTrendLoop) {
      //   config.options.scales.xAxes[0].scaleLabel.display = true;
      //   config.options.scales.xAxes[0].ticks.display = true;
      // }
      lineChart[index] = new Chart(context[index], config);
    });

    if (compConfig.length < MAX_CHART_COUNT) {
      for (let i = compConfig.length + 1; i <= MAX_CHART_COUNT; i++) {
        $("label[for='checkboxView" + i + "']").text("Dummy");
        $("#cbBox" + i + " rect").css("fill", colorSet[i - 1]);
        $("#checkboxView" + i).prop("checked", false);
        $("#canvas" + i).hide();
      }
    }

    if (localStorage.getItem("SignalOptions") != null) {
      let options = JSON.parse(localStorage.getItem("SignalOptions"));
      let optionList = document.getElementById("modal_components").options;
      options.forEach((option) => optionList.add(new Option(option)));
    } else {
      $.ajax({
        type: "GET",
        url: "/signal-options",
      }).done(function (data) {
        //console.log(data);
        //console.log(JSON.parse(data));
        localStorage.setItem("SignalOptions", data);
        let optionList = document.getElementById("modal_components").options;
        JSON.parse(data).forEach((option) =>
          optionList.add(new Option(option))
        );
      });
    }
  }; //initTrendSettings

  cleanupTrends = () => {
    lineChart.forEach((item) => {
      item.destroy();
    });
    lineChart = [];
  }; //cleanupTrends

  getCoilTrendData = () => {
    initTrendSettings();
  }; //getCoilTrendData

  loadCoilOptions = () => {
    $.ajax({
      url: "/coil-options",
      type: "get",
      success: function (response) {
        parsedData = JSON.parse(response);
        let optionList = document.getElementById("coilSelected").options;
        parsedData.forEach((option) => optionList.add(new Option(option)));
      },
      error: function (xhr) {
        console.error(xhr);
      },
    });
  }; //loadCoilOptions

  loadTrendData = () => {
    let coilId = $("#coilSelected").val();
    console.log("Coil Id Query: " + coilId);
    $.ajax({
      url: "/coilwise-trend" + "/" + coilId,
      type: "get",
      success: function (response) {
        //console.log(response);
        filteredData = JSON.parse(response);
        compConfig.forEach((item, index) => {
          if (filteredData.hasOwnProperty(item.signalName)) {
            lineChart[index].data.datasets[0].label = item.signalName;
            lineChart[index].data.datasets[0].data =
              filteredData[item.signalName];
            lineChart[index].data.datasets[0].backgroundColor = colorSet[index];
            lineChart[index].data.datasets[0].borderColor = colorSet[index];
            lineChart[index].data.labels = filteredData.time;
            lineChart[index].update();
          }
        });
      },
      error: function (xhr) {
        console.error(xhr);
      },
    });
  }; //loadTrendData

  updateTrend = (autoscale = false) => {
    if (filteredData.hasOwnProperty("time")) {
      compConfig.forEach((item, index) => {
        if (filteredData.hasOwnProperty(item.signalName)) {
          lineChart[index].data.datasets[0].label = item.signalName;
          lineChart[index].data.datasets[0].data =
            filteredData[item.signalName];
          lineChart[index].data.datasets[0].backgroundColor = colorSet[index];
          lineChart[index].data.datasets[0].borderColor = colorSet[index];
          lineChart[index].data.labels = filteredData.time;
          lineChart[index].update();
        }
      });
      console.log("Update Finished");
    }
  }; //updateTrend
});

getNewConfig = () => {
  const config = {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "",
          backgroundColor: "",
          borderColor: "",
          pointHoverRadius: 5,
          data: [],
          fill: false,
          display: true,
        },
      ],
      labels: [],
    },
    options: {
      legend: {
        display: false,
      },
      responsive: false,
      maintainAspectRatio: true,
      title: {
        display: false,
        text: "",
      },
      tooltips: {
        mode: "index",
        intersect: false,
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
      scales: {
        xAxes: [
          {
            gridLines: {
              // You can change the color, the dash effect, the main axe color, etc.
              borderDash: [10, 5],
              color: "#348632",
            },
            crosshair: {
              enabled: true,
              snapToDataPoint: true,
            },
            shared: true,
            display: true,
            ticks: {
              display: true,
            },
            scaleLabel: {
              display: true,
              labelString: "Time",
            },
          },
        ],
        yAxes: [
          {
            display: true,
            ticks: {
              tickBorderDash: [1],
            },
            scaleBreaks: {
              autoCalculate: true,
            },
            scaleLabel: {
              display: true,
              labelString: "",
            },
          },
        ],
      },
      elements: {
        line: {
          tension: 0.5,
        },
        point: {
          borderWidth: 0,
          radius: 1,
          backgroundColor: "rgba(0,0,0,0)",
        },
      },
    },
  };
  return config;
}; //getNewConfig
