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
   slog ("There was an error downloading one of the files, but you can try starting the interview anyway.");
   announce_ready_for_interview(e);
  
}

function on_update_ready (e) {
     
   logEvent(e);
     // Don't perform "swap" if this is the first cache
     if (cacheStatusValues[cache.status] != 'idle') {
         slog('About to try swapping / updating the cache.');
         cache.swapCache();
         slog('Swapped/updated the cache.');
     }
     announce_ready_for_interview(e);
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
     slog(''+message);
}

function slog(a) {
    if (typeof (glog) == "function") {
      glog (a)
    }
    else {
      console.log (a);
    }

}


function announce_ready_for_interview(e) {
   logEvent(e);
    if (typeof (download_success_callback) == 'function' ) {
      download_success_callback();
    }
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



