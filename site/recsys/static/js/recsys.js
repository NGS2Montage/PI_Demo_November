var app = {
  title: "",
  abstract: "",
  authors: [],

  refill: function (msg) {
    app.title = msg.title;
    app.abstract = msg.abstract;
    app.authors = msg.author;

    // var recData = msg.cited_paper_data.map(function (cite) {
    //   return [cite.title, cite.Author, cite.Year];
    // });

    var recData = msg.cited_paper_url.map(function (cite) {
      return [cite, '', ''];
    });

    $('#rec-table').dataTable().fnClearTable();
    $('#rec-table').dataTable().fnAddData(recData);
  },

  init: function () {
    app.table = $('#rec-table').DataTable({
        // deferRender: true,
        // data: [],
        paging: false,
        searching: false,
        info: false,
        columns: [
            {title: "Title"},
            {title: "Author"},
            {title: "Year"},
        ],
        ajax: {
          url: '/rec-sys/recommendations/?doi=10.1.1.30.6583',
          dataSrc: function ( json ) {
            console.log("Hi there")
            console.log(json);
            return json.cited_paper_url.map(function (d) {
              return [d.title, d.author.join(', '), d.year];
            })
            // return json.data;
          },
        },
        processing: true,

        // columnDefs: [{
        //     "targets": [0],
        //     render: function (data, type, row) {
        //       return '<a rel="noopener noreferrer" target="_blank" href="' + data + '">' + data.substring(49) + '</a>'
        //     },
        // }],
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

      // app.table.data = function ( d ) {
      //   return $.extend( {}, d, {
      //     "doi": $('#doi-input').val()
      //   } );
      // };

      var ajaxURL = '/rec-sys/recommendations/?doi=' + $('#doi-input').val();
      console.log("Setting table url to ", ajaxURL);
      app.table.ajax.url(ajaxURL);

      app.table.ajax.reload();


      // var doiInput = document.getElementById('doi-input');
      // console.log(doiInput.value);


      // // table.ajax.url( 'newData.json' )

      // $.ajax({
      //     method: "GET",
      //     url: "/rec-sys/recommendations/",
      //     data: { doi: doiInput.value }
      // })
      //   .done(function( msg ) {
      //     console.log(msg);
      //     app.refill(msg);
      //   });

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
