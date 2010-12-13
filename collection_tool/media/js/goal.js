function set_goal_field (goal_id, field, text) {
    key = goal_id + "_" + field;
    $('#' + key)[0].value = text
}

function goal_val (goal_id, field) {
    key = goal_id + "_" + field;
    val = $('#' + key).val();
    return val;
}

function test_set_get_goal_text() {
  set_goal_text (LOCAL_STORAGE_KEY, family_id, '999', 'when', 'soon')
  if ('soon' == get_goal_text (LOCAL_STORAGE_KEY, family_id, '999', 'when')) {
    return 'pass';
  }
  return 'fail';
}

function goal_field_changed( e) {
  goal_text = e.originalEvent.target.value;
  goal_key = e.originalEvent.target.id;
  goal_id = goal_key.split('_')[0];
  field_name = goal_key.split('_')[1];
  set_goal_text (LOCAL_STORAGE_KEY, family_id, goal_id, field_name,goal_text);
}

goal_form_fields = ['name','resp', 'stps', 'when'];



function init() {
  goal_id = $('#goal_id_div')[0].innerHTML;
  $.each (goal_form_fields, function (a, field_name) {
      stored_value = get_goal_text (LOCAL_STORAGE_KEY, family_id, goal_id, field_name);
      set_goal_field (goal_id,field_name, stored_value);
      $('#' + goal_id + '_' + field_name ).blur  (goal_field_changed);
      $('#' + goal_id + '_' + field_name ).change(goal_field_changed);
    }
  );
}

$(document).ready(init);




