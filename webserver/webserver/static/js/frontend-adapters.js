// updates the table with IP address info of the RasPis.
function updateTable() {
  form = $("#form-section");
  form.html("");
  btn = $("#button-section");

  var device_types = Object.keys(currDevices);

  
  for (i = 0; i < device_types.length; i++) {

    var cat_name = device_types[i] //Ex. "RasPi"

    // Make a new panel
    panel = $("<div class='panel panel-default' id='"+ cat_name +"-panel'></div>");

    panel_hdr = $("<div class='panel-heading'><h3 class='panel-title'>"+ cat_name +"</h3></div>");
    panel_body = $("<div class='panel-body'></div>");
    panel_table = $("<table class='table' id='"+ cat_name +"-panelTable'>");

    var devices_in_cat = Object.keys(currDevices[cat_name]);


    // To this new panel, add all the devices found
    for (j = 0; j < devices_in_cat.length; j++) {
      var row = $("<tr></tr>");

      var dev_name = devices_in_cat[j];
      var checked = parseInt(currDevices[cat_name][dev_name]);

      var checkbox;
      if (checked) {
      checkbox = $("<td><input type='checkbox' name='dev_name' value='"+ dev_name +"' checked></input></td>");
      } else {
      checkbox = $("<td><input type='checkbox' name='dev_name' value='"+ dev_name +"'></input></td>"); 
      }
      var dev = $("<td><p class='lead'>"+ dev_name + "</p></td>");

      row.append(checkbox);
      row.append(dev);

      panel_table.append(row);
    }

    panel_body.append(panel_table);
    panel.append(panel_hdr);
    panel.append(panel_body);
    form.append(panel);
  }


    $("#config-btn").remove();
    btn.append($("<input type='submit' id='config-btn' class='btn btn-info' value='Configure'>")); 
}