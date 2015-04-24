function get_data(){
  $.ajax({
    dataType: "json",
    url: "/update",
    success: function(data){
        console.log(data);
        $("#altitude-val").text(data['Altitude'])
        gauges[0].write(data['Altitude']);
    }
  });
}

setInterval(get_data, 10000);
console.log(gauges);