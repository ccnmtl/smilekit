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



// TODO refactor check_for_previous_answers to use family_questions (LOCAL_STORAGE_KEY, family_id) to find fam.
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
    var family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
    var family_key = family_id + '_answers';
    var result = local_storage_get (LOCAL_STORAGE_KEY, family_key);
    if (result == null) {
      result = {}
    }
    return result;
}

function store_answer(question_id, answer_id) {
    answers = family_answers ();
    var family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
    var family_key = family_id + '_answers';
    answers [question_id] = answer_id;
    local_storage_set (LOCAL_STORAGE_KEY, family_key, answers);
    update_debug_localstorage(); 
}

function answer_clicked(event) {
  event.preventDefault();
  if (event.target.tagName == 'IMG') {
    the_link= event.target.parentNode
  } else {
    the_link = event.target
  }
  answer_id = the_link.id.split('_')[1];
  question_id = $('#question_id_div')[0].innerHTML;
  store_answer (question_id, answer_id); 
  update_debug_localstorage(); 
  highlight_answer (answer_id);
}

function unhighlight_answer (a, b) {
  $('#' + b.id).removeClass('contentbuttonchosen')
}


function page_has_pictures_to_illustrate_answers() {
  return $('.answerthumbnail').length > 0
}


function highlight_answer (answer_id) {
  if ( page_has_pictures_to_illustrate_answers()) {
    $('.answerthumbnail').removeClass('chosen_thumbnail_div')
    $('#answer_' + answer_id).parent().addClass ('chosen_thumbnail_div');
  }
  else {
    // regular questions:
    $.each ( $('.contentbuttonchosen'), unhighlight_answer);
    $('#answer_' + answer_id).addClass('contentbuttonchosen')
  }
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

function hilite_answered_questions (arr) {
    $.each(arr,
        function (a, question_id) {
            it =  $('.question_id_' + question_id);
            it.addClass('contentbuttoncomplete');
        }
    )
}

function init() {



           
    family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
    update_debug_localstorage();
    answers = family_answers();
    
    all_questions = local_storage_get (LOCAL_STORAGE_KEY, 'list_of_questions');
    questions = null;
    
    var family_study_id = null;
    
    for (i = 0; i < all_questions.length; i = i + 1) {
      if (all_questions[i].family_id == family_id) {
        questions = all_questions[i].all_questions;
        family_study_id =  all_questions[i]['family_study_id_number'];
        family_url_list = all_questions[i]['url_list'];
      }
    }
    
  
    if (questions == null) {
      alert ("Can't find list of questions for family " + family_id);
      $('#left').hide();
      $('#right').hide();
      return;
    }
    
    set_nav_urls (prev_next_url (family_url_list));
    set_assessment_url();
    
    set_family_id_in_nav ( family_id);
    
    if ( window.location.href.match (/question/)) {
        ///// QUESTION PAGE
        // highlight the chosen answer on the question page:    
        display_question_id = parseInt($('#display_question_id_div')[0].innerHTML);
        question_id = parseInt($('#question_id_div')[0].innerHTML);
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
      } else {
        ///// SECTION INDEX PAGE
        /// show all questions that are in the topic for this config:
        $('a.contentbutton').hide()
        if (questions != null) {
          $.each(questions, function (a, question_id) {$('#question_' + question_id).show() })
        }      
        //highlight the ones that are answered:
        new_answered_questions = $.keys( answers);
        old_answered_questions = $.keys(family_questions(LOCAL_STORAGE_KEY, family_id)['previous_visit_questions']);
        hilite_answered_questions(old_answered_questions);
        hilite_answered_questions(new_answered_questions);
        
    }
    set_last_interview_url ();
}
$(document).ready(init);




