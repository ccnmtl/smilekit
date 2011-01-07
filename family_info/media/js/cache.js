// Convenience array of status values

var num_files_downloaded;

function percent_done (done, total) {
  return Math.floor((done / total) * 100 );
}

function show_bar (percent) {
  $("#progressbar").progressBar( percent); 
}

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
    status_images_error();

}


// image helper functions:
function status_images_none() {
  $('.download_status_image_div').hide();
}

function status_images_upload() {
  $('.download_status_image_div').hide()
  $('#upload').show()
}

function status_images_download() {
  $('.download_status_image_div').hide()
  $('#download').show();
}

function status_images_error() {
  $('.download_status_image_div').hide()
  $('#error').show()
}

function on_update_ready (e) {
  logEvent(e);
   // Don't perform "swap" if this is the first cache
   if (cacheStatusValues[cache.status] != 'idle') {
       slog('About to try swapping / updating the cache.');
       cache.swapCache();
       slog('Swapped/updated the cache.');
   }
   status_images_none();
   announce_ready_for_interview(e);
 }

function logEvent(e) {
  var num_files_total = 262;
  var online, status, type, message;
  online = (isOnline()) ? 'yes' : 'no';
  status = cacheStatusValues[cache.status];
  type = e.type;
  if (type == 'progress') {
    console.log (num_files_downloaded);
    if (num_files_downloaded == null) {
      num_files_downloaded = 0;
    }
    num_files_downloaded ++;
    show_bar(percent_done( num_files_downloaded, num_files_total));    
  }
  
  
  message = 'online: ' + online;
  message+= ', event: ' + type;
  message+= ', status: ' + status;     if (type == 'error' && navigator.onLine) {
     message+= ' (ERROR)';
      status_images_error();
  }
  slog(''+message);
  if (type != 'error') {
  status_images_download();
  }
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
  status_images_none();
  if (typeof (download_success_callback) == 'function' ) {
    download_success_callback();
  }
}


function isOnline() {
     return navigator.onLine;
}


function autoCheckForUpdates(){
   try {
     setInterval(function(){cache.update()}, 50000);
    } catch (e) {
    slog ("Error");
   }
}



