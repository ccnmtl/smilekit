var LOCAL_STORAGE_KEY;

// just for testing:

 $.extend({
   keys: function(obj){
     var a = [];
     $.each(obj, function(k){ a.push(k) });
     return a;
   }
 })
  

/*
function local_storage_write () {
  v = document.getElementById('the_value_to_write').value;
  localStorage [LOCAL_STORAGE_KEY] = v;
  alert ('Wrote "' + v + '" to local storage.');
}
*/
function local_storage_set ( namespace, key, value ) {
  temp_state = JSON.parse(  localStorage [namespace] )
  temp_state [key] = value;
  localStorage [namespace] = JSON.stringify(temp_state);
  temp_state = null;
}


function local_storage_read () {
  v = localStorage[LOCAL_STORAGE_KEY];
  if ( v == null) {
    alert ('Local storage is empty.');
  }
  else {
    alert ('Found "' + v + '" in local storage.');
  }  
}

function local_storage_keys () {

}

function local_storage_clear () {
  localStorage.clear();
  alert ('Wiped local storage.');
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
 cache.addEventListener('updateready', logEvent, false);

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
  $('#debug_cache_status')[0].innerHTML = s;
}

 function isOnline() {
     return navigator.onLine;
 }


 // Swap in newly download files when update is ready
 cache.addEventListener('updateready', function(e){
         // Don't perform "swap" if this is the first cache
         if (cacheStatusValues[cache.status] != 'idle') {
             cache.swapCache();
             console.log('Swapped/updated the Cache Manifest.');
         }
     }
 , false);

 // These two functions check for updates to the manifest file
 function checkForUpdates(){
     cache.update();
 }
 function autoCheckForUpdates(){
     setInterval(function(){cache.update()}, 50000);
 }
     


var online_check_number = 0;     
     
function check_if_we_are_online() {
  jQuery.get('/collection_tool/online_check', online_check_callback);
  jQuery.get('/collection_tool/online_check', online_check_callback);
}

function online_check_callback(data) {
  //console.log('checking');
  //alert(data);
  if (online_check_number == 0) {
    online_check_number = parseInt(data);
  }
  else {
    if (online_check_number == parseInt(data)) {
        // cached
        //console.log('cached');
        $('#online_or_not')[0].src = "/collection_tool/media/images/icon_offline.jpg"
        
    }else {
        //fresh
        //console.log('fresh');
        $('#online_or_not')[0].src = "/collection_tool/media/images/icon_online.jpg"
        
    }
  }
}


function answer_clicked(event) {
  event.preventDefault();
  //console.log(event.target.id.split('_')[1]);  
  answer_id = event.target.id.split('_')[1];
  question_id = $('#question_id_div')[0].innerHTML;
  local_storage_set (LOCAL_STORAGE_KEY, question_id, answer_id);
  update_debug_localstorage(); 
  highlight_answer (answer_id);
}

/* haven't figured out how else to do this in jquery yet: */
function unhighlight_answer (a, b) {
  $('#' + b.id).removeClass('contentbuttonchosen')
}

function highlight_answer (answer_id) {
  $.each ( $('.contentbuttonchosen'), unhighlight_answer);
  $('#answer_' + answer_id).addClass('contentbuttonchosen')
}

function init_answer_clicked() {
  $('a.contentbutton').click(answer_clicked);
}

$('#online_or_not').ajaxError(function(e, xhr, settings, exception) {
  //if (settings.url == 'ajax/missing.html') {
  //  $(this).text('Triggered ajaxError handler.');
  //}
  console.log('ERROR');
});


function update_debug_localstorage() {
  if ($('#debug_localstorage')[0]) {
    document.getElementById('debug_localstorage').innerHTML = localStorage [LOCAL_STORAGE_KEY];
  }
}

function init() {
        LOCAL_STORAGE_KEY = 'la_llave_encantada';
        if (localStorage [LOCAL_STORAGE_KEY] == null) {
          localStorage [LOCAL_STORAGE_KEY] = '{}';
        }
        update_debug_localstorage();
        if ( window.location.href.match (/question/)) {
          init_answer_clicked();
        }
        //check_if_we_are_online();
        //autoCheckForUpdates();
        
        
        if ( window.location.href.match (/question/)) {
          // highlight the chosen answer on the question page:
          question_id = $('#question_id_div')[0].innerHTML;
          answer_id = JSON.parse( localStorage [LOCAL_STORAGE_KEY])[question_id];
          highlight_answer (answer_id);
        } else {
            // highlight all answered questions on the section page:
            answered_questions = $.keys( JSON.parse( localStorage [LOCAL_STORAGE_KEY]))
            $.each(
                answered_questions,
                function (a, question_id) {
                      $('#question_' + question_id).addClass('contentbuttoncomplete');
               }
            )
        }
}



$(document).ready(init);




