"use scrict";

$(function() {
  var form = $("form[name=map]"),
    url = form.attr('action'),
    attribution = form.find('#attribution').html(),
    tileLayerUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    config = {maxZoom: 18, attribution: attribution};

  // Set a default view in case there are no Locations.
  var map = L.map('map').setView([0, 0], 2);

  // The markers layer enables us to create marker clusters.
  var markers = L.markerClusterGroup({showCoverageOnHover: false});

  // Create the Tile Layer and bind it to the map.
  L.tileLayer(tileLayerUrl, config).addTo(map);

  // Get the JSON payload of locations from the endpoint.
  $.get(url).done(function(data) {
    data.forEach(function(v, i){
      // Use the first location to determine where the
      // map viewport will be initially focused.
      if (i === 0) {
        map.setView([v.fields.latitude, v.fields.longitude], 5);
      }

      var title = v.fields.belong_to_name.name;
      // Instantiate a new marker.
      var marker = L.marker(
        [v.fields.latitude, v.fields.longitude],
        {title: title}
      );

      // Leverage jQuery to create an HTML element that we will use
      // inside the marker. This will create a link to the name detail
      // page. Then add the new marker to the markers layer, which will 
      // give us marker clusters.
      var a = $('<a/>', {'href': v.fields.belong_to_name.url,'text': title });
      marker.bindPopup(a.prop('outerHTML'));
      markers.addLayer(marker);
    });

    // Add the markers to the map.
    map.addLayer(markers);
  });
});
