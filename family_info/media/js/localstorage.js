// Convenience array of status values

var cache = window.applicationCache;

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
         console.log('About to try swapping / updating the cache.');
         cache.swapCache();
         console.log('Swapped/updated the cache.');
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
     console.log(''+message);
}

function announce_ready_for_interview(e) {
   logEvent(e);
   show_buttons();
}

function show_buttons() {
   console.log("READY");
   $('#downloading').hide()
   $('.visit_button').show();
}


function isOnline() {
     return navigator.onLine;
}


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



