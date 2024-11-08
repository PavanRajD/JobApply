document.getElementById("jobForm").onsubmit = function (event) {
  event.preventDefault();

  // Collect form data
  const formData = new FormData(document.getElementById("jobForm"));
  const submitButton = document.getElementById("submitButton");
  const statusElement = document.getElementById("status");

  submitButton.disabled = true;

  // Send data via AJAX POST request
  fetch("/submit", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "Data submitted successfully!") {
        // Start SSE connection
        const source = new EventSource("/stream");
        source.onmessage = function (event) {
          statusElement.innerHTML += event.data + "<br>";
          if (event.data.includes("successfully")) {
            submitButton.disabled = false;
          }
        };

        source.onerror = function (event) {
          statusElement.innerHTML += "connection failed<br>";
          submitButton.disabled = false;
          source.close();
        };
      } else {
        statusElement.innerHTML +=
          "Form submission failed:" + data.message + "<br>";
        submitButton.disabled = false;
      }
    })
    .catch((error) => {
      statusElement.innerHTML += error + "<br>";
      submitButton.disabled = false;
    });
};
