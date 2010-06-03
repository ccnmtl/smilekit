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
  scores = response['scores'];
  console.log(scores);
  for(var i=0; i <= results.length; i++) {
    console.log(results[i]);
  }
  var inner = "";
  $.each(results, function(index, value) {
    inner += "<tr>";
    inner += "<td>" + index + "</td>";
    inner += "<td>" + value + "</td>";
    inner += "</tr>";
  });
  $('#multipleview-inner').html(inner);
}

function init_ajax_upload() {
  new AjaxUpload('upload_button',
                 {action: '/weights/load',
                  name: 'csvfile',
                  responseType: 'json',
                  onSubmit: function() {
                    var data = {};
                    $("input.weight").each(function () {
                      data[this.id] = $(this).val();
                    });
                    $("input.moduleweight").each(function () {
                      data[this.id] = $(this).val();
                    });
                    this.setData(data);
                  },
                  onComplete: display_csv
  });
}

function multipleView() {
  $("#right").show();
  $("#tableview").toggleClass("view-multiple");
  $("#tableview").toggleClass("view-single");
}

function singleView() {
  $("#right").hide();
  $("#tableview").toggleClass("view-multiple");
  $("#tableview").toggleClass("view-single");
}

function init_toggle() {
  $("#toggle_button").toggle(singleView, multipleView);
}

$(document).ready(init_ajax_upload);
$(document).ready(init_toggle);