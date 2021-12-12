// Navbar toggler initialisation
document.addEventListener('DOMContentLoaded', () => {
    let elems = document.querySelectorAll('.sidenav');
    let instances = M.Sidenav.init(elems);
});

// Initialize the select element 
$(document).ready(function(){
    $('select').formSelect();
  });

// Initialize date picker
  $(document).ready(function(){
    $('.datepicker').datepicker();
  });

//modal
$('.modal').modal();
