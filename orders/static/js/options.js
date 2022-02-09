/** @format */
window.addEventListener("load", () => {});
document.addEventListener("DOMContentLoaded", () => {
  console.log("CONNECTED!");

  //jquery and ajax
  $.ajax({
    url: "/pizza/tops",
    type: "get",
    dataType: "json",
    success: function(data) {
      console.log(data);
      get_data = data;
    }
  });
  /* largeBtn.onclick(() => {
    if (smallBtn.id == "select") {
      smallBtn.removeAttribute("id");
    }
    largeBtn.setAttribute("id", "select");
    price.innerHTML = "{{ pizza.large }}";
  }); */

  /* smallBtn.onclick(() => {
    if (largeBtn.id == "select") {
      largeBtn.removeAttribute("id");
    }
    smallBtn.setAttribute("id", "select");
    price.innerHTML = "{{ pizza.small }}";
  }); */
});
