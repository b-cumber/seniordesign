function get_data(){
    $.ajax({
      dataType: "json",
      url: "/update",
      success: function(data){
          console.log(data);
          $("#altitude").text(data['Altitude']+"!!")
      }
    });
}
setInterval(get_data, 6000);