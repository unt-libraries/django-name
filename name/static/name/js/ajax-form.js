$(function() {
    $("#names").autocomplete({
        source: function(request, response){
            // FIXME: Remove hardcoded URL
            $.getJSON("/name/search.json", {q_type: $('#q_type').val(), q: request.term}, response);
        },
        minLength: 2
    });
});
