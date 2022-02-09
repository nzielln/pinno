/** @format */

document.addEventListener("DOMContentLoaded", () => {
  console.log("CONNECTED!");
  const main = document.querySelector(".top-body");
  const images = [
    "../static/images/one_image.jpg",
    "../static/images/pizza.jpg",
    "../static/images/sub.jpg",
    "../static/images/salad.jpg",
    "../static/images/pasta.jpg"
  ];
  counter = -1;

  function changeImage() {
    counter++;

    if (counter >= 5) {
      counter = 0;
    }

    main.style.backgroundImage = "url(" + images[counter] + ")";
    main.style.backgroundSize = "100%";
    main.style.backgroundPosition = "center";
    main.style.height = "100%";
    main.style.backgroundRepeat = "no-repeat";
    main.style.backgroundAttachment = "fixed";

    console.log(counter);
  }
  changeImage();

  setInterval(changeImage, 3500);

  //change price on click, menu
  const largeBtn = document.querySelector(".large");
  const smallBtn = document.querySelector(".small");
  const price = document.querySelector(".price");
  if (largeBtn !== null && smallBtn !== null) {
    largeBtn.onclick(() => {
      if (smallBtn.id == "select") {
        smallBtn.removeAttribute("id");
      }
      largeBtn.setAttribute("id", "select");
      price.innerHTML = "{{ pizza.large }}";
    });

    smallBtn.onclick(() => {
      if (largeBtn.id == "select") {
        largeBtn.removeAttribute("id");
      }
      smallBtn.setAttribute("id", "select");
      price.innerHTML = "{{ pizza.small }}";
    });
  }

  /* function changeImage() {
        if (x = 0) {
            main.style.backgroundSize = "50%";
            main.style.backgroundPosition = "0% 50%";
            main.style.backgroundRepeat = "no-repeat";
            main.style.height = "100%";
            
            
            }
        main.style.backgroundImage = "url("+images[4]+")";
        main.style.backgroundSize = "50%";

        main.style.backgroundPosition = "0% 50%";
        main.style.height = "100%";
        main.style.backgroundRepeat = "no-repeat";
            
        x++;
        
        
        
         if (x >= images.length) {
        x = 0;
        }
        

        } */

  // switch(x) {
  //     case x = 0:
  //         main.style.backgroundImage = "url('../static/images/main_image.jpg')";
  //         main.style.backgroundPosition = "0% 50%";
  //         main.style.backgroundSize = "50%";
  //         main.style.height = "100%";
  //         main.style.backgroundRepeat = "no-repeat";
  //     break;
  //     case x = 1:
  //         main.style.backgroundImage = "url('../static/images/pizza.jpg')";
  //         main.style.backgroundPosition = "center";
  //         main.style.height = "100%";
  //         main.style.backgroundRepeat = "no-repeat";
  //         break;

  //     case x = 2:
  //         main.style.backgroundImage = "url('../static/images/sub.jpg')";
  //         main.style.backgroundPosition = "center";
  //         main.style.height = "100%";
  //         main.style.backgroundRepeat = "no-repeat";
  //         break;

  //     case x = 3:
  //         main.style.backgroundImage = "url('../static/images/salad.jpg')";
  //         main.style.backgroundPosition = "center";
  //         main.style.height = "100%";
  //         main.style.backgroundRepeat = "no-repeat";
  //         break;

  //     case x = 4:
  //         main.style.backgroundImage = "url('../static/images/pasta.jpg')";
  //         main.style.backgroundPosition = "center";
  //         main.style.height = "100%";
  //         main.style.backgroundRepeat = "no-repeat";
  // }

  // function changeImage() {
  //     x++;

  //     if(x >= 4) {
  //         x = 0;
  //     }
  // }
});
