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

LOCAL_STORAGE_KEY = 'la_llave_encantada';
