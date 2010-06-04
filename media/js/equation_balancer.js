var answers;
var scores;

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

function show_patient_data(patientNumber) {
  $("#patient-number").html(patientNumber);

  ans = answers[patientNumber];
  sc = scores[patientNumber];
  $("input.moduleweight").each(function() {
    var num = this.id.substring(13);
    $("#modulescore-"+num).val(sc["module-"+num]);
  });
  
  $("input.weight").each(function() {
    var qnum = this.id.substring(7);
    $("#answer-"+qnum).val(ans[qnum]); 
    $("#score-"+qnum).val(sc["question-"+qnum]); 
  });
}

function display_csv(file, response) {
  answers = response['data'];
  scores = response['scores'];
  var inner = "";
  var numPatients = 0;
  $.each(answers, function(index, value) {
    inner += "<tr class='patient-row' id='patient-" + index + "'>";
    inner += "<td>" + index + "</td>";
    inner += "<td>" + scores[index]["total"] + "</td>";
    inner += "</tr>";
    numPatients++;
  });
  $('#multipleview-inner').html(inner);
  $('#num-patients').html(numPatients);
  
  $('tr.patient-row').each(function() {
    $(this).click(function() {
      show_patient_data(this.id.substring(8));
      singleView();
    });
  });
}

function init_ajax_upload() {
  new AjaxUpload('upload_button',
                 {action: '/weights/load',
                  name: 'csvfile',
                  responseType: 'json',
                  onSubmit: function(file, extension) {
                    $("#filename").html(file);
                    var data = {};
                    $("input.weight").each(function () {
                      data[this.id] = $(this).val();
                    });
                    $("input.moduleweight").each(function () {
                      data[this.id] = $(this).val();
                    });
                    this.setData(data);
                    multipleView();
                  },
                  onComplete: display_csv
  });
}

function multipleView() {
  $("#right").show();
  $("#tableview").addClass("view-multiple");
  $("#tableview").removeClass("view-single");
}

function singleView() {
  $("#right").hide();
  $("#tableview").addClass("view-single");
  $("#tableview").removeClass("view-multiple");
}

function toggleViews() {
  if( $("#right").is(":visible") ) {
    singleView();
  }
  else {
    multipleView();
  }
}

function init_toggle() {
  $("#toggle_button").click(toggleViews);
}

$(document).ready(init_ajax_upload);
$(document).ready(init_toggle);