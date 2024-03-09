const swiper = new Swiper(".swiper", {
    loop: true,
    pagination: {
      el: ".swiper-pagination",
    },
  });
  
  function toggleMenu() {
    var menuElement = document.getElementById("header-right-menu");
    if (menuElement.style.display === "block") {
      menuElement.style.display = "none";
    } else {
      menuElement.style.display = "block";
    }
  }

console.log("working fine");
const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

$(".review-form").submit(function(e){
    e.preventDefault();

    let date = new Date();
    let time = date.getDate() + " " + monthNames[date.getUTCMonth()] + ", " + date.getFullYear()

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        datatype: "json",

        success: function(response){
            console.log("Comment saved")


            if (response.bool==true){
                $("#review-res").html("Review Added!")
                $(".review-hide-form").hide()

                let _html = '<div class="spr-review">'
                    _html += '<div class="spr-review-header">'
                    _html += '<span class="spr-review-header-byline">'
                    _html += '<strong> '+ response.context.user +' </strong>' 

                    _html += '<span> '+ time +' </span>'
                    _html += '</span>'

                    _html += '<div class="rating"></div>'

                    for(let i= 1; i <= response.context.rating; i++){
                        _html += '<i class="fa fa-star text-warning" aria-hidden="true "></i>'
                    }
                    _html += '</div>'

                    _html += '<div class="spr-review-content">'
                    _html += '<p class="spr-review-content-body">'+ response.context.review +'</p>'
                    _html += '</div>'
                    _html += '</div>'
                    $(".user-comment").prepend(_html)
            }
            


        }
    })
})



// add to cart functionality
$(".add-to-cart-btn").on("click", function(){
    let this_val = $(this)
    let index = this_val.attr("data-index")


    let quantity = $(".quantity-wanted-" + index).val()
    let product_title = $(".product-title-" + index).val()
    let product_id = $(".product-id-" + index).val()
    let product_price = $("#current-price-" + index).text()
    let product_pid = $(".product-pid-" + index).val()
    let product_image = $(".product-image-" + index).val()
    

    console.log("Qty:", quantity);
    console.log("Title:", product_title);
    console.log("ID:", product_id);
    console.log("PID:", product_pid);
    console.log("Image:", product_image);
    console.log("Price:", product_price);
    console.log("Index:", index);

    console.log("Current element:", this_val);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,

        },
        datatype: 'json',
        beforeSend: function(){
            console.log("Adding products to cart")
        },
        success: function(res){
            this_val.html("&check;")
            console.log("products added to cart")
            $(".cart-products-count").text(res.totalcartitems)
        }
    })


})

