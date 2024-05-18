let nav = document.querySelectorAll(".mys_box .nav li");
let nav_box = document.querySelectorAll(".nav_box");

nav.forEach((item, idx) => {
    item.addEventListener("click", () => {
        console.log("click");
        nav.forEach((item) => item.classList.remove("active"));
        item.classList.add("active");

        nav_box.forEach((item) => {
            item.classList.remove("active");
        });
        nav_box[idx].classList.add("active");
    });
});

function redirect_pagination () {
const savedType = localStorage.getItem('paginationType');
        console.log(savedType)
        if(savedType) {
            if(savedType == "own-posts"){
                console.log(1)
                nav[1].click();
            } else if (savedType == "liked-posts") {
                console.log(2)
                nav[2].click();
            } else if (savedType == "commented-posts") {
                console.log(3)
                nav[3].click();
            }
            localStorage.clear();
            }


}

redirect_pagination();

const items = document.querySelector(".box1").querySelectorAll(".item");
for (i = 0; i < items.length - 1; i++) {
  items[i].addEventListener(
    "click",
    (function (index) {
      return function () {
        nav[index + 1].click();
      };
    })(i)
  );
}


const paginationLinks = document.querySelectorAll('.paginationLink');
for(i = 0; i < paginationLinks.length; i++) {
    paginationLinks[i].addEventListener("click", function(e){
        e.preventDefault();
        const type = this.dataset.type;
        localStorage.setItem('paginationType', type);
        window.location.href = this.href;


    })
}

