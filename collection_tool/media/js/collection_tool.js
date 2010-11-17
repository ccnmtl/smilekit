// just for testing:
 $.extend({
   keys: function(obj){
     var a = [];
     $.each(obj, function(k){ a.push(k) });
     return a;
   }
 })


function family_questions (key, family_id) {
     result = null;
     $.each(local_storage_get(key, 'list_of_questions') , function(k, fam) { 
         if (fam['family_id'] == family_id) {
           result = fam;
           return;
         }
    });
    return result;
}


function check_for_previous_answers (my_question_id) {
  previous_answers_result = null;
  $.each(local_storage_get(LOCAL_STORAGE_KEY, 'list_of_questions') , function(k, fam) { 
     if (fam['family_id'] == family_id) {
       previous_visit_questions = fam['previous_visit_questions'];
       $.each(previous_visit_questions, function (the_question_id, the_answer_id) {
         if (the_question_id == my_question_id) {
            previous_answers_result =  the_answer_id;
         }
       });
    }
  }
  );
  return previous_answers_result;
}

function family_answers () {
    family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
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
  
  if (event.target.tagName == 'IMG') {
    the_link= event.target.parentNode
  } else {
    the_link = event.target
  }
  answer_id = the_link.id.split('_')[1];
  
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
    
    // TODO: 
    // previous_visit_questions
    
    
    all_questions = local_storage_get (LOCAL_STORAGE_KEY, 'list_of_questions');
    questions = null;
    
    for (i = 0; i < all_questions.length; i = i + 1) {
    
      if (all_questions[i].family_id == family_id) {
        questions = all_questions[i].all_questions;
      }
    }
    
      if (questions == null) {
        alert ("Can't find list of questions for family " + family_id);
        $('#left').hide();
        $('#right').hide();
        return;
      }
      
    
    if ( window.location.href.match (/question/)) {
    
      display_question_id = parseInt($('#display_question_id_div')[0].innerHTML);
      question_id = parseInt($('#question_id_div')[0].innerHTML);
      
      // set up next and previous:
      language_code = $('#language_code_div')[0].innerHTML
      
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
      
      init_answer_clicked();
      
      
      
      if (answers [question_id] != null) {
        // did this family answer this question in THIS interview?
        highlight_answer (answers[question_id]);
      }
      else {
        // did this family answer this question in a previous interview?
        previous_answer = check_for_previous_answers(question_id);
        if (previous_answer != null) {
            highlight_answer (previous_answer);
        }
      }
      
      // highlight the chosen answer on the question page:
    } else {
        answered_questions = $.keys( answers)
        $.each(
            answered_questions,
            function (a, question_id) {
                  $('#question_' + question_id).addClass('contentbuttoncomplete');
           }
        )
        $('a.contentbutton').hide()
        if (questions != null) {
          $.each(questions, function (a, question_id) {$('#question_' + question_id).show() })
        }      
        
    }
}
$(document).ready(init);




