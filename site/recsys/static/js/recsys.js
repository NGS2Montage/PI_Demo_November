(function() {

  window.addEventListener('load', function() {
    var form = document.getElementById('doi-form');
    form.addEventListener('submit', function(event) {
      // if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
      // }
      // form.classList.add('was-validated');

      var doiInput = document.getElementById('doi-input');
      console.log(doiInput.value);

      $.ajax({
          method: "GET",
          url: "/rec-sys/recommendations/",
          data: { doi: doiInput.value }
      })
        .done(function( msg ) {
          console.log(msg);
        });

    }, false);
  }, false);
})();

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
