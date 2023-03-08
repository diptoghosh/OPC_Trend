const MAX_CHART_COUNT = 20;
const SCREEN_WIDTH_RATIO = 0.95;
const SCREEN_HEIGHT_RATIO = 0.9;
const svgns = "http://www.w3.org/2000/svg";
var settingsIcon = {
  width: 500,
  height: 600,
  path: "M495.9 166.6c3.2 8.7 .5 18.4-6.4 24.6l-43.3 39.4c1.1 8.3 1.7 16.8 1.7 25.4s-.6 17.1-1.7 25.4l43.3 39.4c6.9 6.2 9.6 15.9 6.4 24.6c-4.4 11.9-9.7 23.3-15.8 34.3l-4.7 8.1c-6.6 11-14 21.4-22.1 31.2c-5.9 7.2-15.7 9.6-24.5 6.8l-55.7-17.7c-13.4 10.3-28.2 18.9-44 25.4l-12.5 57.1c-2 9.1-9 16.3-18.2 17.8c-13.8 2.3-28 3.5-42.5 3.5s-28.7-1.2-42.5-3.5c-9.2-1.5-16.2-8.7-18.2-17.8l-12.5-57.1c-15.8-6.5-30.6-15.1-44-25.4L83.1 425.9c-8.8 2.8-18.6 .3-24.5-6.8c-8.1-9.8-15.5-20.2-22.1-31.2l-4.7-8.1c-6.1-11-11.4-22.4-15.8-34.3c-3.2-8.7-.5-18.4 6.4-24.6l43.3-39.4C64.6 273.1 64 264.6 64 256s.6-17.1 1.7-25.4L22.4 191.2c-6.9-6.2-9.6-15.9-6.4-24.6c4.4-11.9 9.7-23.3 15.8-34.3l4.7-8.1c6.6-11 14-21.4 22.1-31.2c5.9-7.2 15.7-9.6 24.5-6.8l55.7 17.7c13.4-10.3 28.2-18.9 44-25.4l12.5-57.1c2-9.1 9-16.3 18.2-17.8C227.3 1.2 241.5 0 256 0s28.7 1.2 42.5 3.5c9.2 1.5 16.2 8.7 18.2 17.8l12.5 57.1c15.8 6.5 30.6 15.1 44 25.4l55.7-17.7c8.8-2.8 18.6-.3 24.5 6.8c8.1 9.8 15.5 20.2 22.1 31.2l4.7 8.1c6.1 11 11.4 22.4 15.8 34.3zM256 336c44.2 0 80-35.8 80-80s-35.8-80-80-80s-80 35.8-80 80s35.8 80 80 80z",
};
var hideIcon = {
  width: 500,
  height: 600,
  path: "M150.7 92.77C195 58.27 251.8 32 320 32C400.8 32 465.5 68.84 512.6 112.6C559.4 156 590.7 207.1 605.5 243.7C608.8 251.6 608.8 260.4 605.5 268.3C592.1 300.6 565.2 346.1 525.6 386.7L630.8 469.1C641.2 477.3 643.1 492.4 634.9 502.8C626.7 513.2 611.6 515.1 601.2 506.9L9.196 42.89C-1.236 34.71-3.065 19.63 5.112 9.196C13.29-1.236 28.37-3.065 38.81 5.112L150.7 92.77zM189.8 123.5L235.8 159.5C258.3 139.9 287.8 128 320 128C390.7 128 448 185.3 448 256C448 277.2 442.9 297.1 433.8 314.7L487.6 356.9C521.1 322.8 545.9 283.1 558.6 256C544.1 225.1 518.4 183.5 479.9 147.7C438.8 109.6 385.2 79.1 320 79.1C269.5 79.1 225.1 97.73 189.8 123.5L189.8 123.5zM394.9 284.2C398.2 275.4 400 265.9 400 255.1C400 211.8 364.2 175.1 320 175.1C319.3 175.1 318.7 176 317.1 176C319.3 181.1 320 186.5 320 191.1C320 202.2 317.6 211.8 313.4 220.3L394.9 284.2zM404.3 414.5L446.2 447.5C409.9 467.1 367.8 480 320 480C239.2 480 174.5 443.2 127.4 399.4C80.62 355.1 49.34 304 34.46 268.3C31.18 260.4 31.18 251.6 34.46 243.7C44 220.8 60.29 191.2 83.09 161.5L120.8 191.2C102.1 214.5 89.76 237.6 81.45 255.1C95.02 286 121.6 328.5 160.1 364.3C201.2 402.4 254.8 432 320 432C350.7 432 378.8 425.4 404.3 414.5H404.3zM192 255.1C192 253.1 192.1 250.3 192.3 247.5L248.4 291.7C258.9 312.8 278.5 328.6 302 333.1L358.2 378.2C346.1 381.1 333.3 384 319.1 384C249.3 384 191.1 326.7 191.1 255.1H192z",
};

for (let i = 1; i <= MAX_CHART_COUNT; i++) {
  if (i == 1) {
    jQuery("<div>", {
      id: "canvasConatiner" + i,
      class: "canvas-conatiner",
      //title: "",
    }).insertAfter("#topBtnGroup");
  } else {
    let prev = i - 1;
    jQuery("<div>", {
      id: "canvasConatiner" + i,
      class: ["row", "canvas-conatiner"],
      //title: "",
    }).insertAfter("#canvas" + prev);
  }

  jQuery("<div>", {
    id: "canvas" + i,
    class: "plotly-canvas",
    //title: "trend div",
  }).appendTo("#canvasConatiner" + i);

  if (i <= parseInt(MAX_CHART_COUNT / 2)) {
    jQuery("<div>", {
      id: "checkboxDiv" + i,
    }).appendTo("#checkboxHolderRow1");
  } else {
    jQuery("<div>", {
      id: "checkboxDiv" + i,
    }).appendTo("#checkboxHolderRow2");
  }

  jQuery("<input>", {
    id: "checkboxView" + i,
    type: "checkbox",
  }).appendTo("#checkboxDiv" + i);

  try {
    let html =
      '<svg id="cbSvgBox' +
      i +
      '" width="40" height="16" style="margin: 5px"></svg>';
    $("#checkboxDiv" + i).append(html);

    $("#cbSvgBox" + i).attr({
      width: 25,
      height: 25,
      viewBox: [0, 0, 40, 16].join(" "),
      preserveAspectRatio: "xMidYMid meet",
    });

    $("#cbSvgBox" + i).css("margin", "0px");
    var rect = document.createElementNS(svgns, "rect");
    rect.setAttribute("x", 5);
    rect.setAttribute("y", -10);
    rect.setAttribute("rx", 13);
    rect.setAttribute("ry", 13);
    rect.setAttribute("width", 25);
    rect.setAttribute("height", 25);
    rect.setAttribute("fill", "red");
    $("#cbSvgBox" + i)[0].appendChild(rect);
  } catch (error) {
    console.error(error);
  }

  jQuery("<label>", {
    id: "cbLabel" + i,
  }).appendTo("#checkboxDiv" + i);

  $("#cbLabel" + i).attr("for", "checkboxView" + i);
}

$(document).ready(function () {
  // const
  //const MAX_CHART_COUNT = 12;
  var eventSource;
  var context = [];
  var compOptions = [];
  var compConfig = [];
  var viewIndex = 0;
  var trendPaused = false;
  var duration = 0;
  const colorSet = [
    "#00580b",
    "#9127ef",
    "#74f62e",
    "#001fbb",
    "#00d000",
    "#a100c3",
    "#00bf00",
    "#cc1fd1",
    "#87db00",
    "#6953f5",
    "#02ce4b",
    "#e03cd8",
    "#d9ff5f",
    "#853acc",
    "#ffce27",
    "#5052d5",
    "#d0c74a",
    "#8b00a6",
    "#00cb84",
    "#ff004a",
    "#00efd7",
    "#f5004a",
    "#00e2e1",
    "#b90000",
    "#61fcff",
    "#ff2969",
    "#00caa4",
    "#3b006b",
    "#ffee85",
    "#003eab",
    "#ff7900",
    "#007eff",
    "#197700",
    "#0084ff",
    "#246b00",
    "#0042ae",
    "#ccaf49",
    "#001d73",
    "#cdc669",
    "#0077e8",
    "#ac3000",
    "#0094ff",
    "#9d0000",
    "#00ddff",
    "#6b0000",
    "#00daff",
    "#ff635d",
    "#00d9ff",
    "#af0048",
    "#00d3d2",
    "#7e0071",
    "#005700",
    "#ffa2ff",
    "#445900",
    "#0084f1",
    "#d48839",
    "#005db8",
    "#6f4500",
    "#00c1ff",
    "#781711",
    "#00d6ff",
    "#7c001e",
    "#61cefd",
    "#4e0000",
    "#e2fbd5",
    "#540058",
    "#007e51",
    "#82499f",
    "#00693a",
    "#ffc1ff",
    "#002700",
    "#7da7ff",
    "#6e5d13",
    "#003b8e",
    "#d7a477",
    "#00246c",
    "#ffb7b0",
    "#001600",
    "#c9c3ff",
    "#1e3500",
    "#004f98",
    "#ae3731",
    "#007dbf",
    "#88272b",
    "#006f6b",
    "#2c0035",
    "#e2d1cd",
    "#430000",
    "#1f4718",
    "#cd7386",
    "#002a0b",
    "#b37580",
    "#00230b",
    "#a07185",
    "#002b24",
    "#677757",
    "#002533",
    "#2e250f",
    "#002a31",
    "#002725",
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
        compConfig.push({ signalName: ["Dummy"], show: true });
      }
      localStorage.setItem("SignalConfig", JSON.stringify(compConfig));
      cleanupTrends();
      initTrendSettings();
    });
  }

  loadModalData = () => {
    if (viewIndex > 0) {
      $("#modal_show").prop("checked", compConfig[viewIndex - 1].show);
    }
  }; //loadModalData

  saveTrendConfig = () => {
    if (localStorage.getItem("SignalConfig") != null) {
      let signalName = [];
      let color = [];
      let rowCount = 0;
      $("#configTable tbody tr").each(function () {
        rowCount++;
        signalName.push($(this).find("td").eq(0).text());
        color.push($("#colorBtn" + rowCount).val());
      });
      compConfig[viewIndex - 1].signalName = signalName;
      compConfig[viewIndex - 1].signalColor = color;
      compConfig[viewIndex - 1].show = $("#modal_show").prop("checked");
      localStorage.setItem("SignalConfig", JSON.stringify(compConfig));
      initTrendSettings();
    }
  }; //saveTrendConfig

  AddToTrendConfig = () => {
    let tableRow = [];
    let rowCount = 0;
    $("#configTable tbody tr").each(function () {
      rowCount++;
      tableRow.push([
        $(this).find("td").eq(0).text(),
        "<color>" + $("#colorBtn" + rowCount).val() + "</color>",
        "<button></button>",
      ]);
    });
    tableRow.push([
      $("#modal_components").val(),
      "<color></color>",
      "<button></button>",
    ]);
    createTable(tableRow);
  }; //AddToTrendConfig

  removeFromConfig = (id) => {
    let index = parseInt(id.replace("removeBtn", "")) - 1;
    let tableRow = [];
    let rowCount = 0;
    $("#configTable tbody tr").each(function () {
      rowCount++;
      tableRow.push([
        $(this).find("td").eq(0).text(),
        "<color>" + $("#colorBtn" + rowCount).val() + "</color>",
        "<button></button>",
      ]);
    });
    tableRow.splice(index);
    createTable(tableRow);
  }; //removeFromConfig

  saveTrendDuration = (btnId) => {
    duration = parseInt($("#" + btnId).val());
    $(".btn-duration").removeClass("btn-success");
    $(".btn-duration").each((index, item) => {
      if ($(item).val() == duration) $(item).addClass("btn-success");
    });
    localStorage.setItem("Duration", duration);
    cleanupTrends();
    closeEvent();
    getRealtimeTrendData();
  }; //saveTrendDuration

  intiDbCall = () => {
    //const source = new EventSource("/query-database");
    $.ajax({
      type: "GET",
      url: "/query-database",
    });
  }; //intiDbCall

  initTrendSettings = () => {
    if (localStorage.getItem("Duration") != null) {
      duration = parseInt(localStorage.getItem("Duration"));
    } else {
      duration = parseInt($("#btnDur30").val());
      localStorage.setItem("Duration", duration);
    }

    $(".btn-duration").each((index, item) => {
      if ($(item).val() == duration) $(item).addClass("btn-success");
    });

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

      if (item.signalName.length > 1) {
        $("label[for='checkboxView" + viewNum + "']").text("Chart " + viewNum);
      } else {
        $("label[for='checkboxView" + viewNum + "']").text(item.signalName);
      }
      $("#checkboxView" + viewNum).prop("checked", item.show);
      if (item.signalColor === undefined) {
        if (item.signalName.length > 1) {
          $("#cbSvgBox" + viewNum + " rect").attr("fill", colorSet[index]);
        } else {
          $("#cbSvgBox" + viewNum + " rect").css("fill", colorSet[index]);
        }
      } else {
        if (item.signalColor.length > 1) {
          $("#cbSvgBox" + viewNum + " rect").attr("fill", item.signalColor[0]);
        } else {
          $("#cbSvgBox" + viewNum + " rect").attr("fill", item.signalColor[0]);
        }
      }

      if (item.show) $("#canvas" + viewNum).show();
      else $("#canvas" + viewNum).hide();

      if (item.show) visibleTrendLoop++;

      // lineChart[index] = new Chart(context[index], config);

      let layout = getNewLayout();
      // layout.xaxis.title = "time";
      let data = [];
      let title = [];
      item.signalName.forEach((signal, signalIdx) => {
        let tempConfig = getNewData();
        tempConfig.name = signal;
        data.push(tempConfig);
        title.push(signal);
      });
      for (let idx = 0; idx < data.length; idx++) {
        if (item.signalColor === undefined) {
          if (idx === 0) {
            data[idx].line.color = colorSet[index];
          } else {
            data[idx].line.color = colorSet[50 + index];
          }
        } else {
          if (idx === 0) {
            data[idx].line.color = item.signalColor[idx];
          } else {
            data[idx].line.color = item.signalColor[idx];
          }
        }
      }
      if (title.length > 1) {
        // layout.yaxis.title.text = title.join(", ");
        layout.yaxis.title.text = "Chart" + viewNum;
      } else if (title.length === 1) {
        layout.yaxis.title.text = title[0];
      } else {
        layout.yaxis.title.text = "Dummy";
      }
      Plotly.newPlot("canvas" + (index + 1), data, layout, getNewConfig());
    });
    // fit width vscrollbar
    fitTrendWidth();

    if (compConfig.length < MAX_CHART_COUNT) {
      for (let i = compConfig.length + 1; i <= MAX_CHART_COUNT; i++) {
        $("label[for='checkboxView" + i + "']").text("Dummy");
        $("#cbSvgBox" + i + " rect").css("fill", colorSet[i - 1]);
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
    $("#checkbox_holder").width(getTrendWidth());
  }; //initTrendSettings

  cleanupTrends = () => {
    // if required to cleanup data
  }; //cleanupTrends

  createEvent = () => {
    let clientid = +new Date();
    eventSource = new EventSource(
      "/trend-data?duration=" + duration + "&clientid=" + clientid
    );
    console.log("Creatting EventSource: " + eventSource.url);
    eventSource.onopen = (event) => {};
    eventSource.onerror = (err) => {
      //console.log("time out: ", new Date());
    };
    eventSource.onmessage = (event) => {
      //console.log(new Date());
      if (!trendPaused) {
        let index;
        let parsedData = JSON.parse(event.data);
        let filteredData = {};
        var plotData = [];
        var myPlot = "";
        let dtStart = new Date(new Date().getTime() - duration * 1000);
        for (let prop in parsedData) {
          filteredData[prop] = [];
        }
        if (parsedData.hasOwnProperty("time")) {
          for (index = parsedData.time.length - 1; index >= 0; index--) {
            if (new Date(parsedData.time[index]) < dtStart) {
              break;
            }
            for (let prop in parsedData) {
              if (prop == "time")
                filteredData[prop].push(parsedData[prop][index].slice(11));
              else filteredData[prop].push(parsedData[prop][index]);
            }
          }
          for (let prop in filteredData) {
            filteredData[prop] = filteredData[prop].reverse();
          }
        }

        filteredData.time = filteredData.time.map((item) => {
          return "2023-01-27 " + item;
        });
        compConfig.forEach((item, index) => {
          let idx = 0;
          myPlot = document.getElementById("canvas" + (index + 1));
          for (idx = 0; idx < item.signalName.length; idx++) {
            var x = [],
              y = [];
            if (filteredData.hasOwnProperty(item.signalName[idx])) {
              y = [filteredData[item.signalName[idx]]];
              x = [filteredData.time];
              if (idx === 0) {
                let min = Math.min(...filteredData[item.signalName[idx]]),
                  max = Math.max(...filteredData[item.signalName[idx]]);
                if (max - min < 1) {
                  myPlot.layout.yaxis.tickformat = ".3f";
                } else if (max - min < 5) {
                  myPlot.layout.yaxis.tickformat = ".2f";
                } else if (max - min < 10) {
                  myPlot.layout.yaxis.tickformat = ".1f";
                } else {
                  myPlot.layout.yaxis.tickformat = ".0f";
                }
              }
              myPlot.layout.fileindex = idx;
              Plotly.restyle("canvas" + (index + 1), { x: x, y: y }, [idx]);
            }
          }
        });
      }
    };
  }; //createEvent

  closeEvent = () => {
    if (eventSource) {
      console.log(eventSource);
      console.log("Closing EventSource: " + eventSource.url);
      eventSource.close();
      eventSource = null;
      console.log(eventSource);
    }
  }; //closeEvent

  getRealtimeTrendData = () => {
    intiDbCall();
    initTrendSettings();
    createEvent();
  }; //getRealtimeTrendData

  pauseTrendToggle = () => {
    trendPaused = !trendPaused;
    if (trendPaused) {
      $("#btnPause").removeClass("btn-primary");
      $("#btnPause").addClass("btn-danger");
      //$("#btnPause").text("Resume");
    } else {
      $("#btnPause").removeClass("btn-danger");
      $("#btnPause").addClass("btn-primary");
      //$("#btnPause").text("Pause");
    }
    $("#svgPause").toggle();
    $("#svgPlay").toggle();
  }; //pauseTrendToggle

  fitAllTrends = () => {
    let windowHeight = window.innerHeight;
    var visibleTrendTotal = 0;
    var graph = null;
    compConfig.forEach((item, index) => {
      if (item.show) visibleTrendTotal++;
    });
    let footer = $("#checkbox_holder").is(":visible")
      ? $("#checkbox_holder").height()
      : 0;
    let trendNavbar = $("#trendNavbar").height();
    let topBtnGroup = $("#topBtnGroup").height();
    let totalTrendHeight = windowHeight - trendNavbar - topBtnGroup - footer;
    let layout_height =
      (totalTrendHeight * SCREEN_HEIGHT_RATIO * (footer == 0 ? 1.02 : 1)) /
      visibleTrendTotal;
    compConfig.forEach((item, index) => {
      graph = document.getElementById("canvas" + (index + 1));
      graph.layout.height = layout_height;
      graph.layout.width = window.innerWidth * SCREEN_WIDTH_RATIO;
      Plotly.redraw(graph);
    });
  };

  fitTrendWidth = () => {
    compConfig.forEach((item, index) => {
      graph = document.getElementById("canvas" + (index + 1));
      graph.layout.width = getTrendWidth();
      Plotly.redraw(graph);
    });
  };

  getTrendWidth = () => {
    let width = window.innerWidth * SCREEN_WIDTH_RATIO;
    let scrollWidth = window.innerWidth - $("body").width();
    width = width - scrollWidth;
    console.log("scrollWidth:", scrollWidth);
    console.log("trend width:", width);
    return width;
  };

  getNewData = () => {
    var config = {
      type: "scatter",
      //mode: "lines+markers",
      mode: "lines",
      name: "trace",
      x: [""],
      y: [""],
      //hovertemplate:
      //"%{yaxis.title.text}: %{y:.0f}<br>" +
      //"%{xaxis.title.text}: %{x|%Y-%m-%d %H:%M:%S}<br>",
      //"<b>%{yaxis.title.text}</b>: %{y:.0f}<br>" +
      //"%{x|%Y-%m-%d %H:%M:%S.%f}<br>",
      // hoverinfo: "name+x+text",
      line: { color: "#17BECF", shape: "spline", smoothing: 0.9 },
    };
    return config;
  }; //getNewData

  getNewConfig = () => {
    var config = {
      responsive: true,
      displaylogo: false,
      modeBarButtonsToAdd: [
        {
          name: "Signal Configure",
          icon: settingsIcon,
          click: function (gd) {
            console.log(gd.id);
            viewIndex = parseInt(gd.id.replace("canvas", ""));
            $("#viewIndexSelected").text("for : View" + viewIndex);
            let modalComponents = $("#modal_components")[0];
            let signalName = [],
              signalColor = [],
              tableRow = [];
            chartData = gd.data;
            compConfig[viewIndex - 1].signalName.forEach((signal) => {
              signalName.push(signal);
            });
            chartData.forEach((item) => {
              signalColor.push(item.line.color);
            });
            for (let idx = 0; idx < signalName.length; idx++) {
              tableRow.push([
                signalName[idx],
                "<color>" + signalColor[idx] + "</color>",
                "<button></button>",
              ]);
            }
            createTable(tableRow);
            $("#configModal").modal({ backdrop: "static", keyboard: false });
          },
        },
        {
          name: "Show/Hide Legend",
          icon: hideIcon,
          click: function (gd) {
            $("#" + gd.id + " .legend").toggle();
          },
        },
      ],
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
      width: window.innerWidth * SCREEN_WIDTH_RATIO,
      height: 300,
      hovermode: "x",
      legend: {
        x: 0,
        y: 1,
        traceorder: "normal",
        font: {
          family: "sans-serif",
          size: 12,
          color: "#000",
        },
        bgcolor: "#E2E2E2",
        bordercolor: "#FFFFFF",
        borderwidth: 2,
      },
      margin: {
        l: 80,
        r: 20,
        b: 50,
        t: 20,
        pad: 0,
      },
      xaxis: {
        title: "",
        tickfont: {
          family: "Courier New, monospace",
          size: 12,
          color: "#7f7f7f",
        },
        //tickformat: "%H:%M:%S.%L",
        showgrid: true,
        showline: true,
        zeroline: false,
        // showspikes: true,
        // spikemode: "across",
      },
      yaxis: {
        title: {
          text: "",
          font: {
            family: "Arial Black",
            size: 12,
            color: "#7f7f7f",
          },
        },
        tickfont: {
          family: "Courier New, monospace",
          size: 12,
          color: "#7f7f7f",
        },
        showline: true,
        showgrid: true,
        zeroline: false,
        tickformat: ".2f",
      },
      showlegend: true,
    };
    return layout;
  }; //getNewLayout

  createTable = (tableData) => {
    $("#configTable").html("");
    var table = $("#configTable")[0];
    var tableBody = document.createElement("tbody");
    var rowCount = 0;
    tableData.forEach(function (rowData) {
      rowCount++;
      var row = document.createElement("tr");
      rowData.forEach(function (cellData) {
        var cell = document.createElement("td");
        if (cellData.startsWith("<button>")) {
          let btn = document.createElement("BUTTON");
          btn.setAttribute("id", "removeBtn" + rowCount);
          btn.setAttribute("class", "removeBtn");
          btn.appendChild(
            document.createTextNode(
              cellData.replace("<button>", "").replace("</button>", "")
            )
          );
          cell.appendChild(btn);
        } else if (cellData.startsWith("<color>")) {
          let color = cellData.replace("<color>", "").replace("</color>", "");
          let colorBtn = document.createElement("INPUT");
          colorBtn.setAttribute("type", "color");
          colorBtn.setAttribute("value", color);
          //colorBtn.setAttribute("style", "background-color: " + color + ";");
          colorBtn.setAttribute("id", "colorBtn" + rowCount);
          colorBtn.setAttribute("class", "colorBtn");
          cell.appendChild(colorBtn);
        } else {
          cell.appendChild(document.createTextNode(cellData));
        }

        row.appendChild(cell);
      });

      tableBody.appendChild(row);
    });
    table.appendChild(tableBody);

    for (let idx = 1; idx <= rowCount; idx++) {
      $("#removeBtn" + idx).click(function () {
        console.log($(this).attr("id"));
        removeFromConfig($(this).attr("id"));
      });
    }
  };
});
