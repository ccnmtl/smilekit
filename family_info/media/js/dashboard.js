var LOCAL_STORAGE_KEY;

function add_keys() {
  $.extend({
     keys: function(obj){
       var a = [];
       $.each(obj, function(k){ a.push(k) });
       return a;
     }
  })
}

function update_cache_if_necessary () {
  cache.addEventListener('obsolete',    logEvent, false);
  cache.addEventListener('progress',    logEvent, false);
  cache.addEventListener('checking',    logEvent, false);
  cache.addEventListener('downloading', logEvent, false);
  cache.addEventListener('noupdate',    announce_ready_for_interview, false);
  cache.addEventListener('cached',      announce_ready_for_interview, false);
  cache.addEventListener('idle',        announce_ready_for_interview, false);
  cache.addEventListener('error', error_handler, false);
  cache.addEventListener('updateready', on_update_ready, false);     
  try {     
    cache.update();
  } catch(err) {
    // this is only a problem on ipad safari
    glog ("couldn't call cache update ....");
    show_buttons();
  }
}


function update_debug_localstorage() {
  if ($('#debug_localstorage')[0]) {
    document.getElementById('debug_localstorage').innerHTML = localStorage [LOCAL_STORAGE_KEY];
  }
}

function function_maker (id) {
  my_new_func = function () {
    local_storage_set ( LOCAL_STORAGE_KEY, 'current_family_id', id);
    //alert ("Setting current family id to " + id);
  }

  return my_new_func
}



function glog (str) {
  nw = str + "\n" + $("#debug_cache_status").html();
  $("#debug_cache_status").html(nw);
}


function head_to (family_id, url) {
  local_storage_set ( LOCAL_STORAGE_KEY, 'current_family_id', family_id);  
  window.location = url;
}


function set_up_family_links () {
  start_visit_links = "";

  list_of_questions = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_questions');
  
  if (list_of_questions == null) {
        alert ('list of questions is null; can\'t start interview.');
        return;
  }
  
  $.each(list_of_questions , function(key, value) { 
     family_study_id_number = value['family_study_id_number'];
     family_id = value['family_id'];
     url = value ['first_question_url']

     new_link = "<p>\
     <span id ='progress_info_for_family_" + family_id + "'> </span>\
     <input type='button' class ='go_to_family_button' onclick ='head_to(" + family_id + ", \"" + url + "\")'  value = 'Visit Family # " + family_study_id_number + "' /> </p>";
     start_visit_links += new_link;
  });
  $('#start_visit_links')[0].innerHTML = start_visit_links;

}


function build_end_interview_form () {
  form_contents = "";
  current_interview_questions = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_questions');
  $.each(current_interview_questions , function(key, value) {
        family_id = value['family_id'];
        their_answers = local_storage_get ( LOCAL_STORAGE_KEY, (family_id + '_answers'));
        if (their_answers != null) {
             tmp =  JSON.stringify (their_answers)
        } else {
            tmp = '{}';
        }
        form_contents +=  "<input type='hidden' \
              name = '"  + family_id + "' \
              class = '" + family_id + "' \
              value = '" + tmp + "' />";
    });
    $('#end_interview_inputs')[0].innerHTML = form_contents;
}


function show_interview_progress() {


  $.each(list_of_questions , function(key, value) { 
     family_id = value['family_id'];
     their_answers = local_storage_get ( LOCAL_STORAGE_KEY, family_id + '_answers');
      number = 0;
      if (their_answers != null) {
        number = $.keys(their_answers).length;
      }
     span_id =  '#progress_info_for_family_' + family_id;
     $(span_id)[0].innerHTML = "Questions answered so far: " +  number;
  
  });
}

function hide_buttons() {
  $('.go_to_family_button').hide();
  
}

function show_buttons() {
    $('.go_to_family_button').show();
    $('#downloading').hide();
  if (list_of_questions == null) {
        alert ('list of questions is null; can\'t start interview.');
        return;
    }
}

download_success_callback = show_buttons;

function init_family_info() {
  add_keys();
  LOCAL_STORAGE_KEY = 'la_llave_encantada';
  //glog('init family info:');
  
  // 2) SET UP LINKS TO FIRST PAGE OF EACH FAMILY'S INTERVIEW.
  set_up_family_links ();
  
  if (typeof (local_storage_get) == "undefined") {
    glog ('localstorageget not found.'); 
    return;
  } 
  hide_buttons();
  list_of_questions = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_questions');

  if (list_of_questions == null) {
    alert ('List of questions not found in local storage. Can\'t proceed with interview.');
    return;
  }

  if (typeof (cache) == "undefined") {
    // this might not actually matter.  
    glog ('Cache not found, so can\'t update it.'); 
    show_buttons();
  } 
  else {
    update_cache_if_necessary ();
  }
  //3) BUILD THE END INTERVIEW FORM
  build_end_interview_form ();
  
  // 4) SHOW INTERVIEW PROGRESS SO FAR:
  show_interview_progress();
}

///////////////////

if (typeof ($) == "undefined") {
  alert ('Jquery not found.');
} else {
  $(document).ready(init_family_info);
}


