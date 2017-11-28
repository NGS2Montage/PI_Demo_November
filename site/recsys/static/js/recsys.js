var app = {
  title: "",
  abstract: "",
  authors: [],

  init: function () {
    app.table = $('#rec-table').DataTable({
        // serverSide: true,
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
        order: [
          [3, 'desc']
        ],
        ajax: {
          url: '/rec-sys/recommendations/?doi=blank',
          dataSrc: function ( json ) {
            console.log(json);
            if (json.cited_paper_url.length == 0) {
              app.title = '';
              app.abstract = '';
              app.authors = '';
              return [[]];
            }

            app.title = json.title;
            app.abstract = json.abstract[json.doi];
            app.authors = json.author;

            $('#this-div').removeClass('invisible');

            return Object.keys(json.cited_paper_url).filter(function (doi) {
              var paper = json.cited_paper_url[doi];
              return paper.author && paper.year && paper.title;
            }).map(function (doi) {
              var paper = json.cited_paper_url[doi];
              var authors = paper.author;
              if (Array.isArray(authors)) {
                authors = authors.join(', ');
              }
              var score = '-';
              if ('score' in paper && paper.score) {
                score = parseFloat(Math.round(paper.score * 10000) / 10000).toFixed(4);
              }
              return [paper.title, authors, paper.year, score];
            });
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

$.fn.dataTable.ext.errMode = 'throw';







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
