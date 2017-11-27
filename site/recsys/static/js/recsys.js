var app = {
  title: "",
  abstract: "",
  authors: [],

  init: function () {
    app.table = $('#rec-table').DataTable({
        serverSide: true,
        deferLoading: 0,

        paging: false,
        searching: false,
        info: false,
        columns: [
            {title: "Title"},
            {title: "Author"},
            {title: "Year"},
            {title: "Score"},
        ],
        ajax: {
          url: '/rec-sys/recommendations/?doi=10.1.1.30.6583',
          dataSrc: function ( json ) {
            console.log(json);
            return json.cited_paper_url.map(function (d) {
              return [d.title, d.author.join(', '), d.year, '-'];
            })
          },
        },
        processing: true,

    });
  }
};


(function() {

  window.addEventListener('load', function() {
    rivets.bind(document.getElementById('app-view'), {app: app});
    app.init();

    var filterForm = document.getElementById('filter-form');
    filterForm.addEventListener('submit', function(event) {
      event.preventDefault();
      event.stopPropagation();

      var ajaxURL = '/rec-sys/scores/?doi=' + $('#doi-input').val();
      console.log("Setting table url to ", ajaxURL);
      app.table.ajax.url(ajaxURL);

      app.table.ajax.reload();
    });

    var form = document.getElementById('doi-form');
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      event.stopPropagation();

      var ajaxURL = '/rec-sys/recommendations/?doi=' + $('#doi-input').val();
      console.log("Setting table url to ", ajaxURL);
      app.table.ajax.url(ajaxURL);

      app.table.ajax.reload();
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
