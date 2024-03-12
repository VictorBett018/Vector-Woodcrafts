

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

                let _html = '<div style="padding-left: 20px;">'
                    _html += '<span  id="reviews" class="spr-review-header-byline">'
                    _html += '<strong> '+ response.context.user +' </strong> - ' 
                    _html += '<span> '+ time +' </span>'
                    _html += '</span>'
                    _html += '<br>'

                    for(let i= 1; i <= response.context.rating; i++){
                    _html += '<i style="color: orange;" class="ri-star-fill text-warning"></i>'
                    }
                    _html += '<br>'
                    _html += '<span > '+ response.context.review +'</span>'
                    _html += '</div>'
                    _html += '<br>'
                    $(".c-btn").prepend(_html)
            }
            


        }
    })
})


//product properties


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
    let product_color = $(".product-color-" + index).val()
    let product_woodtype = $(".product-woodtype-" + index).val()
    let product_dimension = $(".product-dimension-" + index).val()

    

    console.log("Qty:", quantity);
    console.log("Title:", product_title);
    console.log("ID:", product_id);
    console.log("PID:", product_pid);
    console.log("Image:", product_image);
    console.log("Price:", product_price);
    console.log("Finish", product_color);
    console.log("Finish", product_woodtype);
    console.log("Finish", product_dimension);
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
            'color':product_color,
            'woodtype':product_woodtype,
            'dimension':product_dimension,

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

//delete product
$(".delete-product").on("click", function(){
    let product_id = $(this).attr("data-product")
    let this_val = $(this)

    console.log("Product Id:", product_id);
    $.ajax({
      url: "/delete-from-cart",
      data: {
        "id": product_id
      },
      beforeSend: function(){
        this_val.hide()
      },
      success: function(response){
        
        this_val.show()
        $(".cart-products-count").text(response.totalcartitems)
        $("#cart-list").html(response.data)
        location.reload()
      }

    })

})

$(".update-product").on("click", function(){
  let product_id = $(this).attr("data-product")
  let this_val = $(this)
  let product_quantity = $(".product-qty-" + product_id).val()

  console.log("Product Id:", product_id);
  console.log("Product QTY:", product_quantity);

  $.ajax({
    url: "/update-cart",
    data: {
      "id": product_id,
      "qty": product_quantity
    },
    beforeSend: function(){
      this_val.hide()
    },
    success: function(response){
      
      this_val.show()
      $(".cart-products-count").text(response.totalcartitems)
      $("#cart-list").html(response.data)
      location.reload()
    }

  })

})

