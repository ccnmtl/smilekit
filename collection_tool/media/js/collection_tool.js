var LOCAL_STORAGE_KEY;

// just for testing:

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


function family_answers () {
    family_id = local_storage_get (LOCAL_STORAGE_KEY, 'family_id');
    family_key = family_id + '_answers'
    result = local_storage_get (LOCAL_STORAGE_KEY, family_key);
    if (result == null) {
      result = {}
    }
    return result;
}



function store_answer(question_id, answer_id) {
    answers = family_answers ();
    answers [question_id] = answer_id;
    local_storage_set (LOCAL_STORAGE_KEY, family_key, answers);
    update_debug_localstorage(); 
}

function answer_clicked(event) {
  event.preventDefault();
  //console.log(event.target.id.split('_')[1]);  
  answer_id = event.target.id.split('_')[1];
  question_id = $('#question_id_div')[0].innerHTML;
  //local_storage_set (LOCAL_STORAGE_KEY, question_id, answer_id);
  
  
  //console.log("Answered " + answer_id + " to question " + question_id);
  
  store_answer (question_id, answer_id); 
  
  update_debug_localstorage(); 
  highlight_answer (answer_id);
}



/* haven't figured out how else to do this in jquery yet: */
function unhighlight_answer (a, b) {
  $('#' + b.id).removeClass('contentbuttonchosen')
}

function highlight_answer (answer_id) {
  $.each ( $('.contentbuttonchosen'), unhighlight_answer);
  $('#answer_' + answer_id).addClass('contentbuttonchosen')
}

function init_answer_clicked() {
  $('a.answerthumbnailimage').click(answer_clicked);
  $('a.contentbutton').click(answer_clicked);

}


function update_debug_localstorage() {
  if ($('#debug_localstorage')[0]) {
    document.getElementById('debug_localstorage').innerHTML = localStorage [LOCAL_STORAGE_KEY];
  }
}

function init() {
    LOCAL_STORAGE_KEY = 'la_llave_encantada';
    update_debug_localstorage();
    answers = family_answers();
    
    
    questions = local_storage_get (LOCAL_STORAGE_KEY, 'list_of_questions');
    
    if ( window.location.href.match (/question/) ||
         window.location.href.match (/insert_visit/)
    ) {
    
      display_question_id = parseInt($('#display_question_id_div')[0].innerHTML);
      question_id = parseInt($('#question_id_div')[0].innerHTML);
      
      // set up next and previous:
      language_code = $('#language_code_div')[0].innerHTML
      // /collection_tool/question/{{displayquestion.prev.id}}/language/{{language_code}}/
      // /collection_tool/question/{{displayquestion.next.id}}/language/{{language_code}}/
      
      if (questions == null) {
        alert ("Can't find list of questions.");
        $('#left').hide();
        $('#right').hide();
        return;
      }
      
      position_of_next_question = questions.indexOf(display_question_id) + 1;
      position_of_prev_question = questions.indexOf(display_question_id) -1;
      
      
      if (position_of_prev_question < 0) {
        $('#left').hide()  
      } else {
        prev_question_id = questions[position_of_prev_question];
        prev_url = '/collection_tool/question/' + prev_question_id + '/language/' + language_code 
        $('#left')[0].href = prev_url
      }
      
      
      
      if (position_of_next_question >= questions.length) {
        $('#right').hide()  
      }
      else {
        next_question_id = questions[position_of_next_question];
        next_url = '/collection_tool/question/' + next_question_id + '/language/' + language_code 
        $('#right')[0].href = next_url
      }
      
      
      
      
      // highlight the chosen answer on the question page:
      init_answer_clicked();
      answer_id = answers[question_id];
      highlight_answer (answer_id);
    } else {
        answered_questions = $.keys( answers)
        $.each(
            answered_questions,
            function (a, question_id) {
                  $('#question_' + question_id).addClass('contentbuttoncomplete');
           }
        )
        $('a.contentbutton').hide()
        $.each(questions, function (a, question_id) {$('#question_' + question_id).show() })
        
        
    }
}



$(document).ready(init);




