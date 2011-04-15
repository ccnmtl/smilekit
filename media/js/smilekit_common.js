LOCAL_STORAGE_KEY = 'la_llave_encantada';
function log_wrapper (a) {
  try {
    console.log(a);
  } catch (e) {
    // Have a nice day.
  }
}

function llog (a) {
    log_wrapper(JSON.stringify(a));
}

function local_storage_has_data (namespace) {
  if (namespace == null) { return false; }
  if (typeof(localStorage ) == "undefined" ) { return false; }
  if (localStorage[namespace] == null  ) { return false; }
  try {
    if (localStorage [namespace] == "{}"){
      return false;
    }
    else {
      return true;
    }  
  }
  catch (e){
    return false;
  }
}


function end_visit_before_logout () {
  if (local_storage_has_data (LOCAL_STORAGE_KEY)) {
    alert ("Please end your visit before logging out.");
  } else {
    window.location.href = "/logout";
  }
}

function set_nav_url (id, url) {
  if (url == null) {
    $(id).hide();
  } else {
    if ($(id).length) {
      $(id)[0].href = url;
    }
  }
}

function set_nav_urls (urls) {
  set_nav_url ('#left',  urls ['prev']);
  set_nav_url ('#right', urls ['next']);
}

function is_part_of_assessment (url) {
    return url.match ('question') != null || url.match ('section') != null;
}

/*
function set_an_url (url) {
    // THIS OVERWRITES THE BLOB:
    analytics_data_blob = { recent_url :   url }
    set_analytics_data (LOCAL_STORAGE_KEY, family_id, analytics_data_blob);
    
}
*/
//CORRECTING THIS:
function set_an_url (url) {
    recent_url_key = 'recent_url';
    // do not overwrite existing data:
    analytics_data_blob = get_analytics_data (LOCAL_STORAGE_KEY, family_id)
    analytics_data_blob [recent_url_key] = url;
    set_analytics_data (LOCAL_STORAGE_KEY, family_id, analytics_data_blob);
}




function set_user_name_in_nav() {
    if ($('#user_id_nav_display') && local_storage_get(LOCAL_STORAGE_KEY, 'user_name')) {
        $('#user_id_nav_display').html('Hi, ' + local_storage_get(LOCAL_STORAGE_KEY, 'user_name'));
    }  
}


function study_id_number ( fam_id ) {
  all_questions = local_storage_get (LOCAL_STORAGE_KEY, 'list_of_questions');
  for (i = 0; i < all_questions.length; i = i + 1) {
    if (all_questions[i].family_id == fam_id) {
      return all_questions[i]['family_study_id_number']
    }
  }
  return null;
}

function set_family_id_in_nav ( fam_id) {
  var family_study_id = study_id_number (fam_id);
  if ($('#family_id_nav_display')) {
    $('#family_id_nav_display').html( 'Family #' + family_study_id );
  }    
  set_user_name_in_nav();
}

function test_setting_url() {
  //setup:
  var correct_url = get_an_url();
  //test:
  try {
      var old_url = '/collection_tool/question/2/language/en/'
      set_an_url (old_url);
      var new_url = get_an_url();
  }
  catch (err) {
    alert (err.name);
    return;
  }
  
  if (old_url == new_url) { 
    alert ('good');
  }
  else {
    alert ('bad');  
  }
  //teardown:
  set_an_url (correct_url);
}

function prev_next_url (family_url_list) {
    var next = null;
    var prev = null;
    $.each(['en','es'], function(i, lan){
      $.each(family_url_list, function(k, v){
          if ( window.location.href.match (v[lan]) != null) {
            if ( k > 0) {
                prev = family_url_list[k - 1][lan]
            }
            // store the assessment page:
            var our_current_url =  family_url_list[k ][lan];
            if (is_part_of_assessment ( our_current_url)) {
               /// store the current page's url.
               set_an_url (our_current_url);
            }
            
            if (  k + 1 < family_url_list.length) {
                 next = family_url_list[k + 1][lan]
            }
          }
      });
    });
    return {'prev': prev, 'next':next};
}




function get_an_url () {
  // TODO: return null if undefined.
  tmp =  get_analytics_data (LOCAL_STORAGE_KEY, family_id)['recent_url'];
  return tmp;
}


function get_last_interview_url () {
  var  last_interview_url_key = 'last_interview_url';
  if (get_analytics_data (LOCAL_STORAGE_KEY, family_id)[last_interview_url_key] == undefined) {
    return null;
  }
  return get_analytics_data (LOCAL_STORAGE_KEY, family_id)[last_interview_url_key];
}


function set_last_interview_url () {
  our_current_url = window.location.pathname
  if (is_part_of_interview( our_current_url )) {
    last_interview_url_key = 'last_interview_url';
    // do not overwrite existing data:
    analytics_data_blob = get_analytics_data (LOCAL_STORAGE_KEY, family_id)
    analytics_data_blob [last_interview_url_key] = our_current_url;
    set_analytics_data (LOCAL_STORAGE_KEY, family_id, analytics_data_blob); 
  }
}


function test_last_interview_url() {
    old_url = get_last_interview_url ();


    new_url = "/collection_tool/question/5/language/es/";    
    set_last_interview_url (new_url) 
    alert (get_last_interview_url ());

    new_url = "/collection_tool/question/6/language/es/";
    set_last_interview_url (new_url) 
    alert (get_last_interview_url ());


    set_an_url ('/collection_tool/question/6/language/es/');
    alert (JSON.stringify( get_analytics_data (LOCAL_STORAGE_KEY, family_id)  ));


    set_last_interview_url (old_url) 
}

//test_last_interview_url();


function return_to_last_interview_url() {
    there = get_last_interview_url ()
    if (there != null) {
        window.location = there;
    }
}

function is_part_of_interview (url) {
    return   url.match ('collection_tool/intro'       ) != null
     ||      url.match ('collection_tool/question'    ) != null
     ||      url.match ('collection_tool/section'     ) != null
     ||      url.match ('collection_tool/risk'        ) != null
     ||      url.match ('collection_tool/topics'      ) != null
     ||      url.match ('collection_tool/goal'        ) != null
     ||      url.match ('collection_tool/planner/goal') != null
     ||      url.match ('collection_tool/goals'       ) != null
     ;
}


function set_assessment_url () {
    if (  LOCAL_STORAGE_KEY == null) {
        return;
    }
    if (  family_id == null) {
        return;
    }
    if (  get_analytics_data (LOCAL_STORAGE_KEY, family_id) == null ) {
        return;
    }
    if (  get_analytics_data (LOCAL_STORAGE_KEY, family_id)['recent_url'] == null ) {
        return;
    }
    var the_url = get_an_url();
    if ($('#assessmenttab').length == 0) {
        return;
    }
    $('#assessmenttab')[0].href = the_url;
}
