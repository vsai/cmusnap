var currDevices = {}

$(document).ready(function() {
  update();
  setInterval(update, 1000);
});





// Makes an async call to the backend to get information of Raspberry Pis
function update() {
  $.ajax({
    url: "searchForRasPis"
  }).done(function(res) {
    if (objectsEqual(currDevices,res)) return;
    currDevices = res;
    updateTable();
  });
}
