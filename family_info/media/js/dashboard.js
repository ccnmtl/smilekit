function add_keys() {
  $.extend({
     keys: function(obj){
       var a = [];
       $.each(obj, function(k){ a.push(k) });
       return a;
     }
  })
}

function download_files_into_cache () {
  // successful return value is null;
  // error returns the error.
  //info messages:
  cache.addEventListener('obsolete',    logEvent, false);
  cache.addEventListener('progress',    logEvent, false);
  cache.addEventListener('checking',    logEvent, false);
  cache.addEventListener('downloading', logEvent, false);

  //new cache:
  cache.addEventListener('updateready', on_update_ready, false);

  //done caching:
  cache.addEventListener('noupdate',    announce_ready_for_interview, false);
  cache.addEventListener('cached',      announce_ready_for_interview, false);
  cache.addEventListener('idle',        announce_ready_for_interview, false);

  // problem:
  cache.addEventListener('error', error_handler, false);

  try  {
    cache.update();
    return null;
  }
  catch(e) {
    return e;
  }
}

function recent_url (family_id) {
  return_value = null
  try {
     return_value = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_states')[family_id]['analytics_data']['recent_url'];
    }
  catch(err) {
     
  }
  return return_value;
}

function update_debug_localstorage() {
  if ($('#debug_localstorage')[0]) {
    $('#debug_localstorage').html( localStorage [LOCAL_STORAGE_KEY]);
  }
}

function function_maker (id) {
  my_new_func = function () {
    local_storage_set ( LOCAL_STORAGE_KEY, 'current_family_id', id);
  }
  return my_new_func
}

function glog (str) {
  nw = str + "\n" + $("#debug_cache_status").html();
  $("#debug_cache_status").html(nw);
}


function head_to (family_id, url) {
  //this sets (or switches) the current family, and heads to the url given.
  local_storage_set ( LOCAL_STORAGE_KEY, 'current_family_id', family_id);
  window.location = url;
}



function set_up_family_links () {
  start_visit_links = "";
  list_of_questions = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_questions');

   if (local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id') == null ) {
      $('#interview_link').hide();
      $('#family_id_nav_display').hide();
   }
   else {
      $('#log_out_link').hide();
   }


  $.each(list_of_questions , function(key, value) {
     family_study_id_number = value['family_study_id_number'];
     family_id = value['family_id'];
     
     url = recent_url(family_id) ||  value ['first_question_url'];

     new_link = "<p> Family " + family_study_id_number + " ( \
     <span id ='progress_info_for_family_" + family_id + "'> </span> )"
    
     if (family_id == local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id')) {
        // (Point the "Interview" link at the top of the page back to the current intervierw.
        $('#interview_link')[0].href = "javascript:head_to( " + family_id + ", \"" + url + "\");"
        $('#interview_link').html('Interview');
        $('#family_id_nav_display').html ( 'Family #' + family_study_id_number);
        
     }
     else {
      // link for other families goes here: 
        new_link += "<a href=\"javascript:head_to(" + family_id + ",'" + url + "')"+ '"> Visit family ' + family_study_id_number + '</a>';
     }
     new_link += "</p>"
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
        their_state   = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_states')[family_id];


        if (their_answers != null) {
             safe_answers =  JSON.stringify (their_answers);
        } else {
            safe_answers = '{}';
        }

        safe_state = JSON.stringify (their_state)
        form_contents +=  "<input type='hidden' \
              name = '"  + family_id + "' \
              class = '" + family_id + "' \
              value = '" + safe_answers + "' />\
              \
              \
              <input type='hidden' \
              name = 'state_"  + family_id + "' \
              class = 'state_" + family_id + "' \
              value = '" + safe_state + "' />\
              ";
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
     $(span_id)[0].innerHTML =  "<span class='num_answers'>" + number + "</span> answers during this interview.";

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

download_success_callback = function () {
  $("#guidance_1").html ("Download was successful. Click one of the 'Visit' buttons below to start.");
  show_buttons();
  $("#progressbar").progressBar(100);
}


function init_family_info() {
  hide_buttons();
  add_keys();

  list_of_questions = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_questions');

  if (list_of_questions == null) {
    alert ('List of questions not found in local storage. Can\'t proceed with interview.');
    return;
  }
  
  //BUILD THE END INTERVIEW FORM
  build_end_interview_form ();

  //SET UP LINKS TO FIRST PAGE OF EACH FAMILY'S INTERVIEW.
  set_up_family_links ();


  //SET UP PROGRESSBAR:
  $("#progressbar").progressBar();

  // TRY AND DOWNLOAD THE FILES NEEDED FOR THE INTERVIEW:
  if (typeof (local_storage_get) == "undefined") {
    glog ('localstorageget not found.');
    return;
  }

  if (typeof (cache) == "undefined") {
    // this might not actually matter.
    glog ('Cache not found, so can\'t update it.');
    show_buttons();
  }
  else {
    error = download_files_into_cache ();
    if (error) {
      status_images_error();
      $('#downloading').hide();
      $('#guidance_1').html ('If you see an "Allow" button at the top of your browser window, please click on it to start the download. If you do not see an "Allow" button, you might have previously told your browser not to accept downloads from this site; you might have to reset your site preferences for this site and try again.)');
      hide_buttons();
      $('#guidance_2').html ('You can also click the "End Visit" button to cancel this visit and go back to the list of families.');
      return;
    }
  }

  // 4) SHOW INTERVIEW PROGRESS SO FAR:
  show_interview_progress();
  
}

///////////////////

if (typeof ($) == "undefined") {
  alert ('Jquery not found.');
} else {
  $(document).ready(init_family_info);
}


