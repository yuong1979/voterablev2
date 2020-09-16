

function showFlashMessage(message) {
  var template = "<div class='container container-alert-flash'>" + 
  "<div class='col-sm-10 col-sm-offset-1'> " + 
  "<div class='alert alert-success alert-dismissible' role='alert'>" + 
  "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
  "<span aria-hidden='true'>&times;</span></button>" 
  + message + "</div></div></div>"
  $("body").append(template);
  $(".container-alert-flash").fadeIn(500);
  setTimeout(function(){ 
    $(".container-alert-flash").fadeOut(500);
  }, 5000);

}






//spinner
var overlay = document.getElementById("overlay");
window.addEventListener('load', function() {
overlay.style.display = 'none';
});

$('body').on('click', 'a[data-action=show-spinner]', function(){
$('#overlay').fadeIn(200);
});












// older scripts - to be deleted if no issues


    // $(".db-submit").click(function(e){
    // var $submitBtn = $(this);

    // e.preventDefault()

    // var msg = $(this).attr("msg");
    
    // $("#dc").fadeIn("300")
    // $("#dc").dialog({
    //   resizable: false,
    //   height: 200,
    //   width: 350,
    //   modal: true,
    //   show: { effect: 'fade' }, 
    //   hide: { effect: 'fade' },
    //   buttons:{
    //     1:{       
    //       id:"close",
    //       text:"Confirm",
    //       click: function(){
    //         console.log("confirm") 

    //           var $form = $submitBtn.parent('.db');

    //           if ($form && $form.length) {
    //             $form.submit();
    //           }

    //         $(this).dialog("close")
    //       },
    //       class: "buy-btn"
    //     },
    //     2:{       
    //       id:"close",
    //       text:"Cancel",
    //       click: function(){
    //         console.log("cancel")
    //         $(this).dialog("close")
    //       },
    //       class: "cancel-btn"
    //     }
    //   }
    // })
    // })






// $(document).ready(function () {

// console.log("hello man")

//      $('#navbar.navbar-collapse').on('show.bs.collapse', function () {
//          $("html, body").addClass('no-scroll');
//          $("#navbar-button .icon-bar").addClass('hidden');
//          $("#navbar-button span.close-btn").removeClass('hidden');
//          $("#navbar-button").blur();
//      });

//      $('#navbar.navbar-collapse').on('hide.bs.collapse', function () {
//          $("html, body").removeClass('no-scroll');
//          $("#navbar-button .icon-bar").removeClass('hidden');
//          $("#navbar-button span.close-btn").addClass('hidden');
//          $("#navbar-button").blur();
//      });


// });


// function showFlashMessage(message) {
//   var template = "<div class='container container-alert-flash'>" + 
//   "<div class='col-sm-10 col-sm-offset-1'> " + 
//   "<div class='alert alert-success alert-dismissible' role='alert'>" + 
//   "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
//   "<span aria-hidden='true'>&times;</span></button>" 
//   + message + "</div></div></div>"
//   $("body").append(template);
//   $(".container-alert-flash").fadeIn(500);
//   setTimeout(function(){ 
//     $(".container-alert-flash").fadeOut(500);
//   }, 5000);
// }
