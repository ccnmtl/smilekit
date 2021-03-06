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


/* AJAX file upload */
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
  new AjaxUpload('upload-button',
                 {action: '/weights/load',
                  name: 'csvfile',
                  responseType: 'json',
                  onSubmit: function(file, extension) {
                    $("#recalc-button").removeAttr('disabled');
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

$(document).ready(init_ajax_upload);

/* recalculate */
function update_scores(data) {
  scores = jQuery.parseJSON(data);

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

  // update the patient information too
  var currentPatient =  $("#patient-number").html();
  show_patient_data(currentPatient);
}

function recalculate() {
  var data = {};
  // get current weights from form
  $("input.weight").each(function () {
    data[this.id] = $(this).val();
  });
  $("input.moduleweight").each(function () {
    data[this.id] = $(this).val();
  });

  // we have the answers already
  $.each(answers, function(index, value) {
    //data['patient-' + index] = value;
    $.each(value, function(index2, value2) {
      data['patient-' + index + '-' + index2] = value2;
    });
  });
  //data[answers] = answers.serialize();
  jQuery.post("/weights/recalculate", data, update_scores);
}

function init_recalculate() {
  $('#recalc-button').click(recalculate);
}

$(document).ready(init_recalculate);

/* AJAX (background) save */
function save_model() {
  $('#model-submit').attr('disabled', 'disabled');
  $('#status').html("Saving...");
  var data = $('#model-form').serialize();
  data += "&ajax=1";
  jQuery.post("save", data, updateStatus);
  return false;
}

function updateStatus() {
  $('#status').html("Saved.");
  $('#model-submit').attr('disabled', '');
}

function init_ajax_save() {
  $('#model-submit').click(save_model);
}

$(document).ready(init_ajax_save);


/* module toggle arrows */
function toggleModule(elem) {
  $(elem.target).toggleClass("toggle-closed");
  $(elem.target).toggleClass("toggle-open");
  var modulenumber = elem.target.id.substr(14);
  $(".module-child-" + modulenumber).toggle();
}

function initToggleModule() {
  $(".module-toggle").click(toggleModule);
}

$(document).ready(initToggleModule);

/* toggle from single patient to multiple patient view */
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

function initToggleViews() {
  $("#toggle-button").click(toggleViews);
}

$(document).ready(initToggleViews);

/* make "back" button go */
$(document).ready(function() { $("#back-button").click(function() { window.location="/weights/"; }); });
