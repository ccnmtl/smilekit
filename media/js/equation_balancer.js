var results;

function setWeight(id, value){
  $('#'+id).val(value);
}

//function validate() {
  // validate all weight fields are numeric
//  var weights = $('input.weight', $('#weight-form'));
//  weights.each ( function(){
//    if( isNaN(this.val()) ) {
//      alert("Error: All weights must be numeric.  Please check your input and try again.");
//      return false;
//    }
//  });
//  return true;
//}

function calculate() {
  if(! validate()) { return false; }

  //var params = "numPlots=" + numPlots + "&shape=" + shape + "&size=" + size;
  //global_http_request = doXHR("calculate", {'method':'POST', 'sendContent':params,
  //                                       'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
  //                                      });
  //global_http_request.addCallback(showResults);
  //global_http_request.addErrback(showError);
}

function display_csv(file, response) {
  results = response['data'];
  var inner = "<table>";
  for(var i=0; i <= results.length; i++) {
    console.log(results[i]);
  }
  $.each(results, function(index, value) {
    inner += index;
    console.log(value);
  });
  inner += "</table>";
  $('#patient-data').html(inner);
}

function init_ajax_upload() {
  new AjaxUpload('upload_button',
                 {action: '/weights/load',
                  name: 'csvfile',
                  responseType: 'json',
                  onComplete: display_csv
  });
}

$(document).ready(init_ajax_upload);