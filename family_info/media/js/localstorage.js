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


function get_planner_data(LOCAL_STORAGE_KEY, family_id) {
  null_state = {'timeline': {}}
  var all_states = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_states');
  if (all_states == null ) {
      alert ("No planner data found.");
      return;
  }
  var family_state = all_states [family_id]
  if (all_states == null ) {
      alert ("No planner data found for this family.");
      return;
  }
  var planner_data = family_state['planner_data']
  if (planner_data == null ) {
      return null_state;
  }
  return planner_data;
}

function set_planner_data(LOCAL_STORAGE_KEY, family_id, blob) {
  var all_states = local_storage_get(LOCAL_STORAGE_KEY, 'list_of_states');
  all_states[family_id]['planner_data'] = blob;
  local_storage_set(LOCAL_STORAGE_KEY, 'list_of_states', all_states);    
}


function test_planner_set() {
  var initial =   get_planner_data(LOCAL_STORAGE_KEY, family_id);

  var before = {"a":{"b":"c<c<c>c"}};
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


