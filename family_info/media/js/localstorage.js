var LOCAL_STORAGE_KEY;

//value can be any object that can be turned into a json object.
function local_storage_set ( namespace, key, value ) {

  if (typeof(localStorage ) == "undefined" ) {
    //alert ("localStorage not found.");
    return;
  }

  if (typeof(localStorage [namespace]) == "undefined")  {
    //alert ("Nothing found stored in localStorage.");
    localStorage [namespace] = '{}';
  }
  
  temp_state = JSON.parse(  localStorage [namespace] )
  
  if (temp_state == null) {
    temp_state = {};
  }
  
  temp_state [key] = value;
  localStorage [namespace] = JSON.stringify(temp_state);
  temp_state = null;
}

function local_storage_get ( namespace, key, value ) {
  if (typeof(localStorage ) == "undefined" ) {
    //alert ("localStorage not found.");
    return;
  }

  if (typeof(localStorage [namespace]) == "undefined")  {
    //alert ("Nothing found stored in localStorage.");
    localStorage [namespace] = '{}';
  }

  temp_state = JSON.parse(  localStorage [namespace] )
  if (temp_state == null) {
    return null;
  }
  if (temp_state[key] == null) {
    return null;
  }
  return temp_state[key];
}
