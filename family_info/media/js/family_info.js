var LOCAL_STORAGE_KEY;

$.extend({
   keys: function(obj){
     var a = [];
     $.each(obj, function(k){ a.push(k) });
     return a;
   }
})

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

// Convenience array of status values
var cacheStatusValues = [];
 cacheStatusValues[0] = 'uncached';
 cacheStatusValues[1] = 'idle';
 cacheStatusValues[2] = 'checking';
 cacheStatusValues[3] = 'downloading';
 cacheStatusValues[4] = 'updateready';
 cacheStatusValues[5] = 'obsolete';

 // Listeners for all possible events
 var cache = window.applicationCache;
 cache.addEventListener('cached', logEvent, false);
 cache.addEventListener('checking', logEvent, false);
 cache.addEventListener('downloading', logEvent, false);
 cache.addEventListener('error', logEvent, false);
 cache.addEventListener('noupdate', logEvent, false);
 cache.addEventListener('obsolete', logEvent, false);
 cache.addEventListener('progress', logEvent, false);
// cache.addEventListener('updateready', logEvent, false);

 cache.addEventListener('updateready', announce_ready_for_interview, false);

 function announce_ready_for_interview(e) {
   $('#downloading').hide()
   $('#done_downloading').show()
  // show the 
 
 }


 // Log every event to the console
 function logEvent(e) {
     var online, status, type, message;
     online = (isOnline()) ? 'yes' : 'no';
     status = cacheStatusValues[cache.status];
     type = e.type;
     message = 'online: ' + online;
     message+= ', event: ' + type;
     message+= ', status: ' + status;
     if (type == 'error' && navigator.onLine) {
         message+= ' (ERROR)';
     }
     glog(''+message);
}

function glog(s) {
  $('#debug_cache_status')[0].innerHTML += ( '\n' + s);
}

function isOnline() {
     return navigator.onLine;
}


 // Swap in newly download files when update is ready
 cache.addEventListener('updateready', function(e){
         // Don't perform "swap" if this is the first cache
         if (cacheStatusValues[cache.status] != 'idle') {
             glog('About to try swapping / updating the cache.');
             cache.swapCache();
             glog('Swapped/updated the cache.');
         }
     }
 , false);

 // These two functions check for updates to the manifest file
 function checkForUpdates(){
     cache.update();
 }
 function autoCheckForUpdates(){
   try {
     setInterval(function(){cache.update()}, 50000);
    } catch (e) {
    alert ("a");
   }
 }



function update_debug_localstorage() {
  if ($('#debug_localstorage')[0]) {
    document.getElementById('debug_localstorage').innerHTML = localStorage [LOCAL_STORAGE_KEY];
  }
}


function start_interview() {
  glog('Erasing all contents of local storage');
  localStorage.clear();
  
  list_of_questions = JSON.parse($('#list_of_questions')[0].innerHTML)
  first_question = list_of_questions[0]
  
  glog ('Setting family key');
  local_storage_set ( LOCAL_STORAGE_KEY, 'family_id', parseInt($('#family_id')[0].innerHTML));
  
  
  glog('Setting list of questions for this configuration in localstorage.');
  local_storage_set ( LOCAL_STORAGE_KEY, 'list_of_questions', list_of_questions );
  
  glog('Leaving page to go to the first page in this configuration:');
  
  first_question_path = '/collection_tool/question/' + first_question + '/language/en/';
  
  glog (first_question_path);
  
  location.href = first_question_path;
}


function init_family_info() {
   $('#done_downloading').hide()

   LOCAL_STORAGE_KEY = 'la_llave_encantada';
 
}


$(document).ready(init_family_info);

