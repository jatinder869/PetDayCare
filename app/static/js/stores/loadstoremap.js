function initMap() {
  // The location of Uluru
  var locations=[
    ]

  $(".store-coord").each(function () {
    let lat=parseFloat($(this).children("lat").html())
        let lng=parseFloat($(this).children("lang").html())
    locations.push({lat:lat,lng:lng})

  });

  var avgLat=0
  var avgLng=0
  locations.map((loc)=>{
    avgLat+=loc.lat;
    avgLng+=loc.lng;
  });
  avgLat/=locations.length;
  avgLng/=locations.length;
  const uluru = { lat: avgLat, lng: avgLng}; //saskatoon coords


  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById("store-map"), {
    zoom: 11,
    center: uluru,
  });
    const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  // The marker, positioned at Uluru
  const markers = locations.map((location, i) => {
    return new google.maps.Marker({
      position: location,
      label: labels[i % labels.length],
    });
  });

  new MarkerClusterer(map, markers, {
    imagePath:
      "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
  });
}