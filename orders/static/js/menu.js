/** @format */
window.addEventListener("load", () => {});
document.addEventListener("DOMContentLoaded", () => {
  console.log("CONNECTED!");
  //change price on click, menu
  const lbtn = document.querySelector(".lbtn");
  const sbtn = document.querySelector(".sbtn");
  const price = document.querySelector(".price");
  const sz_btn = document.querySelector("#select");

  const smallPrice = document.querySelectorAll(".sml");
  const largePrice = document.querySelectorAll(".lrg");

  if (lbtn !== null && sbtn !== null) {
    for (let i = 0; i < largePrice.length; i++) {
      largePrice[i].style.opacity = "0";
    }
    lbtn.addEventListener("click", () => {
      if (sbtn.id == "select") {
        sbtn.removeAttribute("id");
      }
      lbtn.setAttribute("id", "select");
      for (let i = 0; i < largePrice.length; i++) {
        largePrice[i].style.opacity = "1";
      }
    });

    sbtn.addEventListener("click", () => {
      if (lbtn.id == "select") {
        lbtn.removeAttribute("id");
      }
      sbtn.setAttribute("id", "select");
      for (let i = 0; i < largePrice.length; i++) {
        largePrice[i].style.opacity = "0";
      }
    });
  }

  // get cookies
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie("csrftoken");

  //ajax calls
  let session_xhr = new XMLHttpRequest();
  let post_xhr = new XMLHttpRequest();

  // send pizza info

  const food_card = document.querySelectorAll(".foodcard");
  let pz_xhr = new XMLHttpRequest();

  for (let i = 0; i < food_card.length; i++) {
    const food_name = food_card[i].children[1].children[0];
    const food_price = food_card[i].children[1].children[2];

    //const fd_price = fd_card[i].children[1].children[1].children[0].children[0];
    let price;
    let sub_size_data;

    if (sz_btn !== null && sbtn !== null && lbtn !== null) {
      if (sz_btn.innerHTML != "Large") {
        sizing = 0;
      }

      sbtn.onclick = () => {
        sizing = 0;
      };

      lbtn.onclick = () => {
        sizing = 1;
      };

      food_card[i].onclick = () => {
        if (sizing == 0) {
          price = food_price.children[0].children[0].innerHTML;
          sub_size_data = sbtn.innerHTML;
        } else if (sizing == 1) {
          price = food_price.children[1].children[0].innerHTML;
          sub_size_data = lbtn.innerHTML;
        }
        food_data = {
          name: food_name.innerHTML,
          price: price,
          size: sub_size_data,
          pk: food_name.getAttribute("data-pk")
        };

        console.log(food_data);

        let data = JSON.stringify(food_data);
        pz_xhr.open("POST", "/pz_data", true);
        pz_xhr.setRequestHeader(
          "Content-type",
          "application/json; charset=utf-8"
        );
        pz_xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        pz_xhr.send(data);
        pz_xhr.onload = () => {
          console.log(data);
        };

        console.log(food_data);
      };
    }
  }

  //get session data
  session_xhr.open("GET", "/sessions");
  session_xhr.responseType = "json";

  session_xhr.send();

  session_xhr.onload = () => {
    let session_json = session_xhr.response;

    addToOptions(session_json);
  };

  //send data to django
  const addToOptions = resp_data => {
    const optionsArray = [];
    const listOpt = document.querySelectorAll(".option");
    const item = document.querySelector(".main");

    for (let i = 0; i < listOpt.length; i++) {
      const addText = listOpt[i].children[0];
      const addBtn = listOpt[i].children[1];
      const toppingsNum = document.querySelector(".top-num").innerHTML;

      addBtn.onclick = () => {
        if (toppingsNum > optionsArray.length) {
          addBtn.style.color = "red";

          if (optionsArray.includes(addText.innerHTML)) {
          } else {
            optionsArray.push(addText.innerHTML);
          }

          raw_data = {
            name: resp_data["name"],
            pk: resp_data["pk"],
            size: resp_data["size"],
            price: resp_data["price"],
            options: optionsArray
          };
          console.log(raw_data);
        } else if (toppingsNum == "0") {
          raw_data = {
            name: resp_data["name"],
            pk: resp_data["pk"],
            size: resp_data["size"],
            price: resp_data["price"],
            options: optionsArray
          };
          console.log(raw_data);
        }
        if (toppingsNum == optionsArray.length) {
          let data = JSON.stringify(raw_data);
          post_xhr.open("POST", "/post_sessions", true);
          post_xhr.setRequestHeader(
            "Content-type",
            "application/json; charset=utf-8"
          );
          post_xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
          post_xhr.send(data);

          post_xhr.onload = () => {
            console.log(data);
          };
          console.log(optionsArray);
        }
      };
    }
  };

  //send pasta information
  //pasta variables
  let fd_xhr = new XMLHttpRequest();
  const fd_card = document.querySelectorAll(".fd-card");
  for (let i = 0; i < fd_card.length; i++) {
    let fd_name = fd_card[i].children[1].children[0];
    const fd_price = fd_card[i].children[1].children[1];

    //const fd_price = fd_card[i].children[1].children[1].children[0].children[0];
    let price;
    let sub_size_data;

    if (sz_btn !== null && sbtn !== null && lbtn !== null) {
      if (sz_btn.innerHTML == "Small") {
        sizing = 0;
      }

      sbtn.onclick = () => {
        sizing = 0;
      };

      lbtn.onclick = () => {
        sizing = 1;
      };

      fd_card[i].onclick = () => {
        if (sizing == 0) {
          price = fd_price.children[0].children[0].innerHTML;
          sub_size_data = sbtn.innerHTML;
        } else if (sizing == 1) {
          price = fd_price.children[1].children[0].innerHTML;
          sub_size_data = lbtn.innerHTML;
        }
        fd_data = {
          name: fd_name.innerHTML,
          price: price,
          size: sub_size_data,
          pk: fd_name.getAttribute("data-pk")
        };

        let data = JSON.stringify(fd_data);
        fd_xhr.open("POST", "/fd_data", true);
        fd_xhr.setRequestHeader(
          "Content-type",
          "application/json; charset=utf-8"
        );
        fd_xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        fd_xhr.send(data);
        fd_xhr.onload = () => {
          console.log(data);
        };
      };
    } else {
      fd_card[i].onclick = () => {
        price = fd_price.children[0].innerHTML;
        console.log(price);

        fd_data = {
          name: fd_name.innerHTML,
          price: price,
          pk: fd_name.getAttribute("data-pk")
        };

        let data = JSON.stringify(fd_data);
        fd_xhr.open("POST", "/fd_data", true);
        fd_xhr.setRequestHeader(
          "Content-type",
          "application/json; charset=utf-8"
        );
        fd_xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        fd_xhr.send(data);
        fd_xhr.onload = () => {
          console.log(data);
        };
      };
    }
  }

  let status_xhr = new XMLHttpRequest();
  const orders = document.querySelectorAll("#orders");

  if (orders !== null) {
    for (let i = 0; i < orders.length; i++) {
      const status = orders[i].children[0].children[1];
      const order_pk = console.log(status);
      orders[i].onclick = () => {
        status.style.backgroundColor = "green";
        status.style.width = "150px";
        status.textContent = "Complete";

        data = {
          status: status.textContent,
          pk: orders[i].getAttribute("data-pk")
        };
        console.log(data);
        let status_data = JSON.stringify(data);
        status_xhr.open("POST", "/status", true);
        status_xhr.setRequestHeader(
          "Content-type",
          "application/json; charset=utf-8"
        );
        status_xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        status_xhr.send(status_data);
        status_xhr.onload = () => {
          console.log(status_data);
        };
      };
    }
  }
});
