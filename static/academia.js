document.addEventListener("DOMContentLoaded", function () {
  // Add event listeners
  //hide the display of all elements with the class name "request-status"
  var request_element = document.getElementsByClassName("request-status");

  for (var i = 0; i < request_element.length; i++) {
    request_element[i].style.display = "none";
  }
});

function show_details(event, id) {
  //Hide every other status and show status for the clicked request
  var request_element = document.getElementsByClassName("request-status");

  for (var i = 0; i < request_element.length; i++) {
    request_element[i].style.display = "none";
  }

  document.querySelector(`#status-${id}`).style.display = "block";
}
