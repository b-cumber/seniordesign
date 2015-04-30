var poly;
var map;
var msg;

function get_data() {
  $.ajax({
    dataType: "json",
    url: "/update",
    success: function(data){
        msg = $("#msgnum").val();
        if(data["msg"] == msg){
          console.log("No new data");
        }else{
          console.log(data);
          console.log(data["msg"], msg)
          $("#msgnum").val(data["msg"]);
          if(data["Altitude"]){
            $("#altitude-val").text(data['Altitude']);
            gauges[0].write(data['Altitude']);
          }
          if(data["Satellites"]){
            $("#sats-val").text(data['Satellites']);
          }
          if(data["Time"]){
            $("#time").text(data['Time']);
          }
          if(data["Latitude"] && data["Longitude"]){
            $("#lat-val").text(data['Latitude']);
            $("#long-val").text(data['Longitude']);
            addLatLng(data['Latitude'], data['Longitude']);
          }
        }
    }
  });
}

function initialize() {
  var mapOptions = {
    zoom:  15,
    // Center the Map over the Northwest
    center: new google.maps.LatLng(46.75320, -118.30832),
    mapTypeId:"hybrid" 
  };
  
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  
  var polyOptions = {
    strokeColor: '#000000',
    strokeOpacity: 1.0,
    strokeWeight: 3
  };
  poly = new google.maps.Polyline(polyOptions)
  poly.setMap(map);
}

function addLatLng(Lat, Lng) {
  var path = poly.getPath();
  
  coords = new google.maps.LatLng(Lat, Lng);
  path.push(coords);
  map.panTo(coords);
  var marker = new google.maps.Marker({
    position: coords,
    title: '#' + path.getLength(),
    map: map
  });
}

google.maps.event.addDomListenerOnce(window, 'load', initialize);
setInterval(get_data, 4000);
console.log(gauges);
