$(function() {
  "use strict;"
  $("#names").autocomplete({
    source: function(request, response){
      var query = {
        q_type: $('#q_type').val(),
        q: request.term
      };

      $.getJSON($("#autocomplete").val(), query, response);
    },
    minLength: 2
  });
});
