function add_keys() {
  $.extend({
     keys: function(obj){
       var a = [];
       $.each(obj, function(k){ a.push(k) });
       return a;
     }
  })
}

function update_debug_localstorage() {
  if ($('#debug_localstorage')[0]) {
    document.getElementById('debug_localstorage').innerHTML = localStorage [LOCAL_STORAGE_KEY];
  }
}

function function_maker (id) {
  my_new_func = function () {
    local_storage_set ( LOCAL_STORAGE_KEY, 'current_family_id', id);
    //alert ("Setting current family id to " + id);
  }

  return my_new_func
}


function hook_up_form (form) {
  id = form.id
  //alert ("Hooking up form " + id);
  $('#' + id ).submit(function_maker(id));

}

function init_family_info() {
  add_keys()
  console.log('init family info:');
  $.map( $('.start_visit_form') , hook_up_form); 
  if (typeof (local_storage_get) == "undefined") {
    alert ('localstorageget not found.'); 
    return;
  } 
  LOCAL_STORAGE_KEY = 'la_llave_encantada';
  current_family_id = local_storage_get ( LOCAL_STORAGE_KEY, 'current_family_id' );  
  // we can show this now:
  //$('.visit_button').hide();

  localStorage.clear();
  // get the list of questions from the DATABASE:
  // STORE IT FOR THE DURATION OF THE INTERVIEW:
  list_of_questions = JSON.parse($('#list_of_questions')[0].innerHTML);

  // take the list of questions from the database and put it into storage:
  local_storage_set ( LOCAL_STORAGE_KEY, 'list_of_questions', list_of_questions );  
  
}


if (typeof ($) == "undefined") {
  alert ('Jquery not found.');
} else {
  $(document).ready(init_family_info);
}
