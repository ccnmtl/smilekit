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
    //window.location.href = "/family_info/dashboard/";
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


function set_an_url (url) {
    //new_url = "aaaaaaaaaaaaaaaaa_" + url
    //new_url = "/collection_tool/question/39999/language/en/"
    analytics_data_blob = { recent_url :   url }
    
    //analytics_data_blob = { a:'b' }
    //analytics_data_blob = { asdasd: 'asdasdasdasdasdddddddddddddd' }
    
    //analytics_data_blob = {'':''}
    try { 
      set_analytics_data (LOCAL_STORAGE_KEY, family_id, analytics_data_blob);
     } catch(e) {
        //alert ("setting analytics blob triggered error")
        //alert (e);
    }
    
    //test_analytics_set();
}

function get_an_url () {
  tmp =  get_analytics_data (LOCAL_STORAGE_KEY, family_id)['recent_url'];
  //return "asdasd_asdasd".split("_")[1]
  //return '/collection_tool/question/39/language/en/';
  return tmp;
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
             
             if (is_part_of_assessment ( family_url_list[k ][lan])) {
                set_an_url (family_url_list[k ][lan]);
                //analytics_data_blob = { recent_url : family_url_list[k ][lan] }
                //alert (JSON.stringify(analytics_data_blob));
                /*
                try { 
                  set_analytics_data (LOCAL_STORAGE_KEY, family_id, analytics_data_blob);
                 } catch(e) {
                    alert ("setting analytics blob triggered error")
                    alert (e);
                }
                */
                //alert ('noproblem')
                
                //analytics_data_blob = { recent_url : '/collection_tool/question/39/language/en/aaa' }
                /*
                try { 
                  set_analytics_data (LOCAL_STORAGE_KEY, family_id, analytics_data_blob);
                 } catch(e) {
                    //alert ("setting analytics blob triggered error")
                    //alert (e);
                }
                */
                //alert ('ok');
                
                //
                
                /*
                tmp = '/collection_tool/question/1/language/en/'
                analytics_data_blob = { recent_url :  tmp }

                try { 
                  set_analytics_data (LOCAL_STORAGE_KEY, family_id, analytics_data_blob);
                 } catch(e) {
                    alert ("setting analytics blob triggered error")
                    alert (e);
                }
                */
                //set_an_url (family_url_list[k ][lan]);


             }
             
             if (  k + 1 < family_url_list.length) {
                 next = family_url_list[k + 1][lan]
              }
          }
      });
    });
    return {'prev': prev, 'next':next};
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


