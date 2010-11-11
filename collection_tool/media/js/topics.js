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

function calculate_family_answers () {
    family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
    family_key = family_id + '_answers'
    result = local_storage_get (LOCAL_STORAGE_KEY, family_key);
    if (result == null) {
      result = {}
    }
    return result;
}

function update_debug_localstorage() {
  if ($('#debug_localstorage')[0]) {
    document.getElementById('debug_localstorage').innerHTML = localStorage [LOCAL_STORAGE_KEY];
  }
}

function calculate_absolute_score (family_id, scoring_info, config_id, answer_array) {
    score = 0;
    $.each(scoring_info, function (topic_id, topic_info) {
        answer_info =  topic_info [config_id];
        $.each (answer_info, function (answer_id, answer_score) {
            if( answer_array.indexOf (answer_id) != -1) {
                score += answer_score;
            }
        });
    }
  );
  return score;
}

function calculate_relative_score (absolute_score,  scoring_info, config_id, answer_array, maxmin_scoring_info) {
  min_score = 0;
  max_score = 0;
  $.each(maxmin_scoring_info, function (topic_id, topic_info) {
      min_answer_info =  topic_info [config_id]['min'];
      max_answer_info =  topic_info [config_id]['max'];
      //console.log (answer_array);
      //console.log (answer_array);
      //console.log (min_answer_info);
      for (i = 0; i < answer_array.length; i = i + 1) {
        //console.log (answer_array[i]);
        if (min_answer_info[answer_array[i]] !== undefined) {
          min_score += min_answer_info[answer_array[i]];
        }
        if  (max_answer_info[answer_array[i]] !== undefined) {
          max_score += max_answer_info[answer_array[i]];
          console.log (" min_score is now " + min_score );        
          console.log (" max_score is now " + max_score );     
        }
      } // end for
    }); // end each
   
   range_of_possible_scores = max_score - min_score;
   if (range_of_possible_scores == 0) {
       console.log ( "Best and worst scores are the same; can't calculate a risk rating." );
       return null;
   }
   
   console.log ( "Worst possible score is : " + max_score );
   console.log ( "Best possible score is : " +  min_score );
   // if your answers are the BEST possible, your adjusted_score is zero:
   console.log ("Absolute score is " + absolute_score);
   adjusted_score = absolute_score - min_score;
   console.log ( "Adjusted score : " +  adjusted_score );
   // 10 is best, 1 is worst. (So the range is  actually 9):
   result =    1 + Math.round ( 9.0 * ( 1.0 - ( adjusted_score /  range_of_possible_scores) ) );
   console.log ("Relative score is " + result);
   return result;
}

function between (x, a, b) {
  return a < x && x <= b;
}

function init() {
    LOCAL_STORAGE_KEY = 'la_llave_encantada';
    family_configs = JSON.parse($('#family_configs')[0].innerHTML);
    scoring_info   = JSON.parse($('#scoring_info')[0].innerHTML  );
    maxmin_scoring_info = JSON.parse($('#maxmin_scoring_info')[0].innerHTML);
    family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
    family_answers =  calculate_family_answers();
    all_questions = local_storage_get (LOCAL_STORAGE_KEY, 'list_of_questions');
    questions = null;
    for (i = 0; i < all_questions.length; i = i + 1) {
        if (all_questions[i].family_id == family_id) {
            questions = all_questions[i].all_questions;
        }
    }
    if (questions == null) {
      alert ("Can't find list of questions for family " + family_id);
      return;
    }
    config_id = family_configs [family_id];
    var answer_array = [];
      $.each(family_answers, function(k, v){
        answer_array.push(v) 
    });
    absolute_score = calculate_absolute_score (family_id, scoring_info, config_id, answer_array);
    relative_score = calculate_relative_score (absolute_score,  scoring_info, config_id, answer_array, maxmin_scoring_info);
    $('.score_div').hide();
    $('.risk_div').hide();
    
    if relative_score == null {
      // do something;
      return;
    }
    
    $('.score_div.score_' + relative_score ).show()
    if (between (relative_score, 0, 3)) {
      $('#hig_risk').show();
    }
    if (between (relative_score, 3, 6)) {
      $('#med_risk').show();
    }
    if (between (relative_score, 6, 10)) {
      $('#low_risk').show();
    }
    
}

$(document).ready(init);




