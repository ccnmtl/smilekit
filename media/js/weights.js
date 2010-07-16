function create_model(event) {
  var name = $("#new-model").val();

  $("a.config-name:contains("+name+")").each(function() {
    if($(this).html() == name) {
      alert("Sorry, a model named \"" + name + "\" already exists.  Please choose a different name.");
      event.preventDefault();
      return false;
    }
  });
}

function init_create_model() {
  $('#form-create').submit(create_model);
}

$(document).ready(init_create_model);
//$(document).ready(function() {
//    $("form-create").submit(create_model)
// });

function delete_model(event) {
  event.preventDefault();
  var config_id = this.id.substr(7);
  var config_name = $("#config-"+config_id).html();
  if(! confirm("Do you really want to delete \"" + config_name + "\"?") ) {
    return false;
  }
  window.location = "/weights/delete/" + config_id;
}

function init_model_delete() {
  $('.delete').click(delete_model);
}

$(document).ready(init_model_delete);
    
function verify_import(event) {
  var filename = $("#csvfile").val();
  var config_id = filename.substr(0, filename.lastIndexOf('.')) || filename;
  
  $("a.config-name:contains("+config_id+")").each(function() {
    if( ( $(this).html() == config_id ) &&
        ( ! confirm("A model named \"" + config_id + "\" already exists.\nImporting will overwrite it. Are you sure?"))) {
      return false;
    }
  });
}
    
function init_verify_import() {
  $("#import-form").submit(verify_import);
}
    
$(document).ready(init_verify_import);