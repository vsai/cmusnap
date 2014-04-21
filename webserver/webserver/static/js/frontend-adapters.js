// updates the table with IP address info of the RasPis.
function updateTable () {
  var devices = $("#devices");

  // Clear out whatever was there earlier
  devices.html("");

  var device_types = Object.keys(currDevices);
  for (i = 0; i < device_types.length; i++) {

    var device_name = device_types[i]

    // Make a new panel
    panel = $("<div class='panel panel-default' id='"+ device_name +"-panel'></div>");

    panel_hdr = $("<div class='panel-heading'><h3 class='panel-title'>"+ device_name +"</h3></div>");
    panel_body = $("<div class='panel-body'></div>");
    panel_table = $("<table class='table' id='"+ device_name +"-panelTable'>");

    // To this new panel, add all IPs found
    for (j = 0; j < currDevices[device_name].length; j++) {
      var row = $("<tr></tr>");

      var checkbox = $("<td><input type='checkbox'></input></td>");
      var ip = $("<td>"+ currDevices[device_name][j] +"</td>");

      row.append(checkbox);
      row.append(ip);

      panel_table.append(row);
    }

    panel_body.append(panel_table);
    panel.append(panel_hdr);
    panel.append(panel_body);
    devices.append(panel);
  } 
}