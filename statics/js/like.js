$(document).ready(function() {
  $('.like-btn, .unlike-btn').on('click', function(event) {
    event.preventDefault(); 
    var form = $(this).closest('form');
    $.ajax({
      url: form.attr('action'),
      method: form.attr('method'),
      data: form.serialize(),
      success: function(response) {
        console.log(response);
        window.location.reload();
      },
      error: function(xhr, status, error) {
        console.error(error); 
      }
    });
  });
});



