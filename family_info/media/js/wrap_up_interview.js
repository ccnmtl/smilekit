var LOCAL_STORAGE_KEY;

$.extend({
   keys: function(obj){
     var a = [];
     $.each(obj, function(k){ a.push(k) });
     return a;
   }
})

//value can be any object that can be turned into a json object.
function local_storage_set ( namespace, key, value ) {
  temp_state = JSON.parse(  localStorage [namespace] )
  
  if (temp_state == null) {
    temp_state = {};
  }
  
  temp_state [key] = value;
  localStorage [namespace] = JSON.stringify(temp_state);
  temp_state = null;
}

function local_storage_get ( namespace, key, value ) {
  temp_state = JSON.parse(  localStorage [namespace] )
  if (temp_state == null) {
    return null;
  }
  if (temp_state[key] == null) {
    return null;
  }
  return temp_state[key];
}


function init_wrap_up_interview() {
   LOCAL_STORAGE_KEY = 'la_llave_encantada';
   /*
   family_id = local_storage_get(LOCAL_STORAGE_KEY, 'family_id');
   family_answers = local_storage_get(LOCAL_STORAGE_KEY, (family_id + '_answers'));
   questions = $.keys(family_answers);
   for (i=0; i<questions.length; i++) {
      question_id = questions[i];
      answer_id = family_answers [question_id];
      $('#responses_form').append('<input name = "' + question_id + '" value = "' + answer_id + '" type = "hidden"  />');
      $('#responses_form').append('<div>Question ' + question_id + ' -- answer: ' + answer_id + ' </div>');
   }
   $('#responses_form').append('<input name="family_id" value = "' + family_id + '" type = "hidden"  />');
   $('#responses_form').append('<input type="submit" value = "End interview" />');
    */
}


$(document).ready(init_wrap_up_interview);

