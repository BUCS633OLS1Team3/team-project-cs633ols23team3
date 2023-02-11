document.addEventListener("DOMContentLoaded", function () {
  // Add event listeners
  document.querySelector("#status").style.display = "none";
});

function show_details(event, id) {
  console.log("clicked this item");
  // Show request status bar at the top
  document.querySelector("#status").style.display = "block";

  document.querySelector("#status").innerHTML = `<div class="col-md-12">
  <div class="bg-white p-2 border rounded px-3">
    <div
      class="d-flex flex-row justify-content-between align-items-center order"
    >
      <div class="d-flex flex-column order-details">
        <span style="font-weight: bold">Request ID: TRR</span
        ><span class="date">requested on </span>
      </div>
    </div>
    <br />

    <div
      class="d-flex flex-row justify-content-between align-items-center align-content-center"
    >
      <span class="dot"></span>
      <hr class="flex-fill track-line" />
      <span class="dot"></span>
      <hr class="flex-fill track-line" />
      <span class="dot"></span>
      <hr class="flex-fill track-line" />
      <span class="dot"></span>
      <hr class="flex-fill track-line" />
      <span
        class="d-flex justify-content-center align-items-center big-dot dot"
        ><i class="fa fa-check text-white"></i
      ></span>
    </div>
    <div
      class="d-flex flex-row justify-content-between align-items-center"
    >
      <div class="d-flex flex-column align-items-start">
        <span>15 Mar</span><span>Submitted</span>
      </div>
      <div class="d-flex flex-column justify-content-center">
        <span>15 Mar</span><span>Approved</span>
      </div>
      <div
        class="d-flex flex-column justify-content-center align-items-center"
      >
        <span>15 Mar</span><span>Processed</span>
      </div>
      <div class="d-flex flex-column align-items-center">
        <span>15 Mar</span><span>Completed</span>
      </div>
      <div class="d-flex flex-column align-items-end">
        <span>15 Mar</span><span>Closed</span>
      </div>
    </div>
  </div>
</div>`;
}
