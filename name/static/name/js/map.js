"use scrict";

$(function() {
  var form = $("form[name=map]"),
      url = form.attr('action'),
      attribution = form.find('#attribution').html(),
      tileLayerUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      config = {maxZoom: 18, attribution: attribution};

  var map = L.map('map'),
      markers = L.markerClusterGroup({showCoverageOnHover: false});

  L.tileLayer(tileLayerUrl, config).addTo(map);

  $.get(url).done(function(data) {
    data.forEach(function(v, i){
      // Use the first location to determine where the
      // map viewport with be focused initially.
      if (i === 0) {
        map.setView([v.fields.latitude, v.fields.longitude], 5);
      }

      // Instantiate a new marker.
      var title = v.fields.belong_to_name.name;
      var marker = L.marker(
        new L.LatLng(v.fields.latitude, v.fields.longitude),
        { title: title}
      );

      // TODO: Figure out what this does.
      marker.bindPopup(title);
      markers.addLayer(marker);
    });

    // Add the markers to the map.
    map.addLayer(markers);
  });
});
