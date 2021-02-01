$(function () {
  console.log("Start");

  /* From django documentation */
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function post(url, formData) {
    return $.ajax({
      url: url,
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      data: formData,
      processData: false,
      contentType: false,
      type: "POST",
    });
  }

  function sendCmd(cmd) {
    const data = new FormData();
    data.append("cmd", cmd);
    return post("/api/1/state", data);
  }

  /* Load list of models */
  $.get("/api/1/models").then((result) => {
    result.forEach((model) => {
      $("#model-list").append(
        '<input type="radio" name="model" value="' +
          model.id +
          '">' +
          model.name +
          "</input><br/>"
      );
    });
  });

  /* Upload a new model */
  $("#raw-model").change((e) => {
    const formData = new FormData();

    const files = e.target.files;

    formData.append("raw", files[0]);
    formData.append("name", "A new super model");

    post("/api/1/models", formData).then((result) => {
      window.location.reload();
    });
  });

  $("#action-simplify").click(() => {});

  $("#action-print").click(() => {
    const modelId = $("input[name=model]:checked").val();

    const model = new FormData();
    model.append("model", modelId);

    post("/api/1/jobs", model);
  });

  $("#action-start").click(() => {
    sendCmd("start");
  });

  $("#action-stop").click(() => {
    sendCmd("stop");
  });

  function refresh() {
    $.get("/api/1/state").then((result) => {
      $("#status").text(JSON.stringify(result));
      $("#progress").text(result.progress);
      if (result.state == "Finished") {
        sendCmd("ack");
      }
    });
  }

  setInterval(refresh, 1000);
});
