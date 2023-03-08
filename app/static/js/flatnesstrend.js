const MAX_CHART_COUNT = 12;
const SCREEN_RATIO = 0.94;
$(document).ready(function () {
  var context = [];
  var compOptions = [];
  var compConfig = [];
  var viewIndex = 0;
  const lineChart = [];
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
      initTrendSettings();
    }
  }; //saveTrendConfig

  initTrendSettings = () => {
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

      if (item.show) visibleTrendLoop++;

      let layout = getNewLayout();
      layout.yaxis.title = item.signalName;
      // layout.xaxis.title = "time";
      let data = getNewData();
      data.line.color = colorSet[index];
      Plotly.newPlot("canvas" + (index + 1), [data], layout, getNewConfig());
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

    // resize checkbox_holder
    $("#checkbox_holder").width(window.innerWidth * SCREEN_RATIO);
  }; //initTrendSettings

  cleanupTrends = () => {
    lineChart.forEach((item) => {
      item.destroy();
    });
  }; //cleanupTrends

  getHistoryTrendData = () => {
    initTrendSettings();
  }; //getHistoryTrendData

  loadHistoryData = () => {
    $.ajax({
      type: "POST",
      url: "/history-trend",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        start: $("#startDatetime").val(),
        end: $("#endDatetime").val(),
      }),
      success: function (response) {
        //console.log(response);
        filteredData = JSON.parse(response);
        var update = {};
        var myPlot = "";
        filteredData.time = filteredData.time.map((item) => {
          return "2023-01-25 " + item;
        });
        compConfig.forEach((item, index) => {
          if (filteredData.hasOwnProperty(item.signalName)) {
            // lineChart[index].data.datasets[0].label = item.signalName;
            // lineChart[index].data.datasets[0].data =
            //   filteredData[item.signalName];
            // lineChart[index].data.datasets[0].backgroundColor = colorSet[index];
            // lineChart[index].data.datasets[0].borderColor = colorSet[index];
            // lineChart[index].data.labels = filteredData.time;
            // lineChart[index].update();
            // Plotly.extendTraces("canvas" + (index + 1), {
            //   x: [[parseInt(Math.random() * 10)]],
            //   y: [[parseInt(Math.random() * 100)]],
            // });
            myPlot = document.getElementById("canvas" + (index + 1));
            console.log("data", myPlot.data[0].x);
            //let layout = getNewLayout();
            //layout.yaxis.title = item.signalName;
            //layout.xaxis.title = "time";
            y = [filteredData[item.signalName]];
            x = [filteredData.time];
            update = { x: x, y: y };
            Plotly.update(myPlot, update, {}, [0]);
          }
        });
      },
      error: function (xhr) {
        console.error(xhr);
      },
    });
  }; //loadHistoryData
});

getNewData = () => {
  var config = {
    mode: "lines",
    name: "",
    x: [""],
    y: [""],
    hovertemplate:
      //"%{yaxis.title.text}: %{y:.0f}<br>" +
      //"%{xaxis.title.text}: %{x|%Y-%m-%d %H:%M:%S}<br>",
      "<b>%{yaxis.title.text}</b>: %{y:.0f}<br>" + "%{x|%Y-%m-%d %H:%M:%S}<br>",
    line: { color: "#17BECF", shape: "spline", smoothing: 0.9 },
  };
  return config;
}; //getNewData

getNewConfig = () => {
  var config = {
    responsive: true,
    displaylogo: false,
    modeBarButtonsToRemove: [
      "zoom2d",
      "pan2d",
      "select2d",
      "lasso2d",
      "zoomIn2d",
      "zoomOut2d",
      "autoScale2d",
      //"resetScale2d",
      "sendDataToCloud",
    ],
  };
  return config;
}; //getNewConfig

getNewLayout = () => {
  let layout = {
    title: "",
    width: window.innerWidth * SCREEN_RATIO,
    height: 300,
    margin: {
      l: 80,
      r: 20,
      b: 50,
      t: 20,
      pad: 0,
    },
    xaxis: {
      title: "",
      showgrid: true,
      showline: true,
      zeroline: false,
      showspikes: true,
      spikemode: "across",
    },
    yaxis: {
      title: "",
      font: {
        family: "Courier New, monospace",
        size: 5,
        color: "#7f7f7f",
      },
      showline: true,
      showgrid: true,
      zeroline: false,
      tickformat: ".0f",
    },
  };
  return layout;
}; //getNewLayout
