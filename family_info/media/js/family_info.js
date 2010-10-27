



//////////////////////
//////////////////////
//// START CACHE LIBRARY:
///CACHE HANDLER FUNCTIONS:
// TODO: move to separate file and add to manifest, headers.


// Convenience array of status values
var cacheStatusValues = [];
 cacheStatusValues[0] = 'uncached';
 cacheStatusValues[1] = 'idle';
 cacheStatusValues[2] = 'checking';
 cacheStatusValues[3] = 'downloading';
 cacheStatusValues[4] = 'updateready';
 cacheStatusValues[5] = 'obsolete';



function error_handler(e) {
   logEvent(e);
   status = cacheStatusValues[cache.status]; 
   // warn, but allow to continue.
   alert ("There was an error downloading one of the files, but you can try starting the interview anyway.");
   announce_ready_for_interview(e);
  
}


function on_update_ready (e) {
     // Don't perform "swap" if this is the first cache
     if (cacheStatusValues[cache.status] != 'idle') {
         glog('About to try swapping / updating the cache.');
         cache.swapCache();
         glog('Swapped/updated the cache.');
         announce_ready_for_interview(e);
     }
 }    
function logEvent(e) {
     var online, status, type, message;
     online = (isOnline()) ? 'yes' : 'no';
     status = cacheStatusValues[cache.status];
     type = e.type;
     message = 'online: ' + online;
     message+= ', event: ' + type;
     message+= ', status: ' + status;     if (type == 'error' && navigator.onLine) {
         message+= ' (ERROR)';
     }
     glog(''+message);
}

function announce_ready_for_interview(e) {
   logEvent(e);
   show_buttons();
}

function show_buttons() {
   glog("READY");
   $('#downloading').hide()
   $('.visit_button').show();
}


function glog(s) {
  $('#debug_cache_status')[0].innerHTML =   s + '\n' + $('#debug_cache_status')[0].innerHTML;
}

function isOnline() {
     return navigator.onLine;
}



var cache = window.applicationCache;


// These two functions check for updates to the manifest file
function checkForUpdates(){
   cache.update();
}


function autoCheckForUpdates(){
   try {
     setInterval(function(){cache.update()}, 50000);
    } catch (e) {
    alert ("Error");
   }
}


// END CACHE LIBRARY.
//////////////////
///////////////////
//////////////////


var LOCAL_STORAGE_KEY;


//value can be any object that can be turned into a json object.
function local_storage_set ( namespace, key, value ) {
  temp_state = JSON.parse(  localStorage [namespace] )
  
  if (temp_state == null) {
    temp_state = {};
  }
  
  temp_state [key] = value;
  localStorage [namespace] = JSON.stringify(temp_state);
  temp_state = null;
}

function local_storage_get ( namespace, key, value ) {
  temp_state = JSON.parse(  localStorage [namespace] )
  if (temp_state == null) {
    return null;
  }
  if (temp_state[key] == null) {
    return null;
  }
  return temp_state[key];
}

function add_keys() {
  $.extend({
     keys: function(obj){
       var a = [];
       $.each(obj, function(k){ a.push(k) });
       return a;
     }
  })
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


function hook_up_form (form) {
  id = form.id
  //alert ("Hooking up form " + id);
  $('#' + id ).submit(function_maker(id));

}

function init_family_info() {
  add_keys()
  glog('init family info:');
  $.map( $('.start_visit_form') , hook_up_form); 



  if (typeof (local_storage_get) == "undefined") {
    alert ('localstorageget not found.'); 
    return;
  } 

  LOCAL_STORAGE_KEY = 'la_llave_encantada';
  current_family_id = local_storage_get ( LOCAL_STORAGE_KEY, 'current_family_id' );  
  
  if (current_family_id) {
      glog ("Welcome back to the interview launch page.");
      glog ('Interview already in progress. -- current family id is ' + current_family_id);
      
      current_interview_questions = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_questions');
      $.each(current_interview_questions , function(key, value) { 
         //loop throught all current interview answers:
         console.log("Family_id is " + JSON.stringify(value['family_id']));
         family_id = value['family_id'];
         console.log (JSON.stringify( local_storage_get ( LOCAL_STORAGE_KEY, (family_id + '_answers'))));        
         their_answers = local_storage_get ( LOCAL_STORAGE_KEY, (family_id + '_answers'));

         if (their_answers != null) {
             console.log("Questions answered is" + $.keys(their_answers).length); 
             console.log($.keys(their_answers).length);
             $( "#this_interview_answered_by_" + family_id ).html( $.keys(their_answers).length );
             $('form.end_interview_form input.' + family_id)[0].value = JSON.stringify (their_answers);
         
         } else {
            console.log ("no answers found for family " + family_id );
         }
         $('#downloading').hide();
       
      });
        
  
  }
  else {
            glog ("First visit; no data collected yet.");
            $('.visit_button').hide();
            $('#done_downloading').hide();

            //glog('Erasing all contents of local storage');
            //localStorage.clear();

            // get the list of questions from the DATABASE:
            // STORE IT FOR THE DURATION OF THE INTERVIEW:
            list_of_questions = JSON.parse($('#list_of_questions')[0].innerHTML);

            // take the list of questions from the database and put it into storage:
            local_storage_set ( LOCAL_STORAGE_KEY, 'list_of_questions', list_of_questions );  
            glog('list of questions is ' + list_of_questions);
            


            //setup listeners:
            //informational:
            cache.addEventListener('obsolete',    logEvent, false);
            cache.addEventListener('progress',    logEvent, false);
            cache.addEventListener('checking',    logEvent, false);
            cache.addEventListener('downloading', logEvent, false);

             
            // cache.addEventListener('updateready', logEvent, false);
            //cache.addEventListener('error', logEvent, false);
            // cache.addEventListener('noupdate', logEvent, false);

            // these are all success messages
            
            // 
            //cache.addEventListener('updateready', announce_ready_for_interview, false);
            
            cache.addEventListener('noupdate',    announce_ready_for_interview, false);
            cache.addEventListener('cached',      announce_ready_for_interview, false);
            cache.addEventListener('idle',        announce_ready_for_interview, false);


            cache.addEventListener('error', error_handler, false);



             // Swap in newly download files when update is ready
             cache.addEventListener('updateready', on_update_ready, false);        

          
          // start downloading them files:
          
          cache.update();
          
          /*
          // start downloading them files:
          if(confirm('Attempt to download files?')) {
            cache.update();
          }
          else {
            show_buttons();
          }
          */
          
   }
}


if (typeof ($) == "undefined") {
  alert ('Jquery not found.');
} else {
  $(document).ready(init_family_info);
}


