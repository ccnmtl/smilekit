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

function local_storage_get ( namespace, key) {
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


//////////////

function get_planner_data(LOCAL_STORAGE_KEY, family_id) {
  var key = 'planner_data';
  return get_state_data(LOCAL_STORAGE_KEY, family_id, key);
}
function get_goals_data(LOCAL_STORAGE_KEY, family_id) {
  var key =  'goals_data';
  return get_state_data(LOCAL_STORAGE_KEY, family_id, key);
}
function get_state_data(LOCAL_STORAGE_KEY, family_id, key) {
  null_state = null;
  var all_states = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_states');
  if (all_states == null ) {
      alert ("No data found for key " + key);
      return;
  }
  var family_state = all_states [family_id]
  if (all_states == null ) {
      alert ("No data found for this family and key" + key);
      return;
  }
  var return_value = family_state[key];
  if ( typeof ( return_value ) == "undefined" || return_value == null ) {
      return null_state;
  }
  return return_value;
}

//////////////
function set_planner_data(LOCAL_STORAGE_KEY, family_id, blob) {
  var key = 'planner_data';
  return set_state_data(LOCAL_STORAGE_KEY, family_id, key, blob);
}
function set_goals_data(LOCAL_STORAGE_KEY, family_id, blob) {
  var key =  'goals_data';
  return set_state_data(LOCAL_STORAGE_KEY, family_id, key, blob);
}
function set_state_data(LOCAL_STORAGE_KEY, family_id,  key, blob) {
  var all_states = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_states');
  all_states[family_id][key] = blob;
  local_storage_set(LOCAL_STORAGE_KEY, 'list_of_states', all_states);    
}



//////////////
function test_goals_set() {
  var initial =   get_goals_data(LOCAL_STORAGE_KEY, family_id);

  var before = {"aaa":{"bdd":"c<c<c>&&'c"}};
  var after =  {"aaa":{"bdd":"aasd*asõõõd3w'&&"}};
  set_goals_data(LOCAL_STORAGE_KEY, family_id, before)
  var should_be_before = get_goals_data(LOCAL_STORAGE_KEY, family_id);
  
  console.log("should be equal:");
  console.log(JSON.stringify(before));
  console.log(JSON.stringify(should_be_before));

  set_goals_data(LOCAL_STORAGE_KEY, family_id, after)
  var should_be_after = get_goals_data(LOCAL_STORAGE_KEY, family_id);
    
  console.log("should be equal:");
  
  console.log(JSON.stringify(after));
  console.log(JSON.stringify(should_be_after));

  set_goals_data(LOCAL_STORAGE_KEY, family_id, initial);
}




function test_planner_set() {
  var initial =   get_planner_data(LOCAL_STORAGE_KEY, family_id);

  var before = {"a":{"b":"c<óóóc<c>c"}};
  var after =  {"d":{"e":"f>&d"}};
  set_planner_data(LOCAL_STORAGE_KEY, family_id, before)
  var should_be_before = get_planner_data(LOCAL_STORAGE_KEY, family_id);
  
  console.log("should be equal:");
  console.log(JSON.stringify(before));
  console.log(JSON.stringify(should_be_before));

  set_planner_data(LOCAL_STORAGE_KEY, family_id, after)
  var should_be_after = get_planner_data(LOCAL_STORAGE_KEY, family_id);
    
  console.log("should be equal:");
  
  console.log(JSON.stringify(after));
  console.log(JSON.stringify(should_be_after));

  set_planner_data(LOCAL_STORAGE_KEY, family_id, initial);
}


