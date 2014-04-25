var currDevices = {}

$(document).ready(function() {
  pollForUpdates();

  $('#device-form').submit(config_submit_handler);
  
});


function pollForUpdates() {
  update();
  console.log("NOT UPDATING");
  //setInterval(update, 1000);
}


// Makes an async call to the backend to get information of Raspberry Pis
function update() {
  $.ajax({
    url: "searchForRasPis"
  }).done(function(res) {
    //if (objectsEqual(currDevices,res)) return; //TODO COME BACK TO THIS
    currDevices = res;

    updateTable();
  });
}

function config_submit_handler(e) {
   e.preventDefault();
   
   $.ajax({
     type: 'POST',
     url: 'send-config',
     data: $(this).serialize(),
     success: function(data) {
      console.log("returned from backend! :)");
      console.log(data);
     }
   });

}
