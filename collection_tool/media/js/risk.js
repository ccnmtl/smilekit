
function llog (a) {
    console.log(JSON.stringify(a));
}

function family_questions (key, family_id) {
     family_questions_result = null;
     $.each(local_storage_get(key, 'list_of_questions') , function(k, fam) { 
         if (fam['family_id'] == family_id) {
           family_questions_result = fam;
           return;
         }
    });
    return family_questions_result;
}


function calculate_family_answers (family_id, scoring_info) {
    family_key = family_id + '_answers';
    calculate_family_answers_result = local_storage_get (LOCAL_STORAGE_KEY, family_key);
    if (calculate_family_answers_result == null) {
      calculate_family_answers_result = {}
    }
     
    prev = family_questions (LOCAL_STORAGE_KEY, family_id)['previous_visit_questions'];
     $.each(prev, function (qid, aid) {
      if (calculate_family_answers_result [qid] == null) {
          calculate_family_answers_result [qid] = aid;
        }
     });
    
    return calculate_family_answers_result;
}

function the_score_for (topic_id, config_id, answer_id) {
  return scoring_info[topic_id][config_id][answer_id]
}

function max_score_for  (topic_id, config_id, answer_id) {
  return maxmin_scoring_info[topic_id][config_id]['max'][answer_id];
}

function min_score_for  (topic_id, config_id, answer_id) {
  return maxmin_scoring_info[topic_id][config_id]['min'][answer_id];
}

function llog (a) {
    console.log(JSON.stringify(a));
}

function calculate_scores (family_id, scoring_info, config_id, answer_array) {
    var result = {'all': {'score': 0, 'max':0, 'min':0}};
    $.each(scoring_info, function (tid, bla) {
        result[tid] = {'score': 0, 'max':0, 'min':0};
        for (i = 0; i < answer_array.length; i = i + 1) {
            answer_id = answer_array[i]
            found_score = the_score_for (tid, config_id, answer_id);
            if (found_score != null) {
                result['all']['score'] += found_score;
                result['all']['min']   += min_score_for  (tid, config_id, answer_id);
                result['all']['max']   += max_score_for  (tid, config_id, answer_id);
                result[tid]['score']   += found_score;
                result[tid]['min']     += min_score_for  (tid, config_id, answer_id);
                result[tid]['max']     += max_score_for  (tid, config_id, answer_id);
            }        
        }
    }
  );
  return result;
}

function calculate_friendly_score (max_score, min_score, raw_score) {
   range_of_possible_scores = max_score - min_score;
   // if your answers are the BEST possible, your adjusted_score is zero:
   if (range_of_possible_scores == 0) {
      // you need to answer a question to get a score, sorry.
      return null;
   }
   adjusted_score = raw_score - min_score;
   // Now make the best score 10 and the worst score 1:
   //friendly_score =    1 + Math.round ( 9.0 * ( 1.0 - ( adjusted_score /  range_of_possible_scores) ) );
    // other way around actually:   
    friendly_score =    1 + Math.round ( 9.0 * adjusted_score /  range_of_possible_scores ) ;
 
   
   if (true ) {
       console.log ( "User's raw score is " + raw_score);
       console.log ( "Worst possible score is : " + max_score );
       console.log ( "Best possible score is : " +  min_score );
       console.log ( "Adjusted score : " +  adjusted_score );
       console.log ( "Friendly score is " + friendly_score);
   }
   return friendly_score;
}

function between (x, a, b) {
  return a < x && x <= b;
}

function init() {
    LOCAL_STORAGE_KEY = 'la_llave_encantada';
    
    $('.score_div').hide();
    $('.risk_div').hide();
    $('#contentnav').hide();
    
    
    family_configs = JSON.parse($('#family_configs')[0].innerHTML);
    scoring_info   = JSON.parse($('#scoring_info')[0].innerHTML  );
    maxmin_scoring_info = JSON.parse($('#maxmin_scoring_info')[0].innerHTML);
    all_questions = local_storage_get (LOCAL_STORAGE_KEY, 'list_of_questions');
    
    family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
    config_id = family_configs [family_id];
    
    family_answers =  calculate_family_answers(family_id, scoring_info);
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
    var answer_array = [];
      $.each(family_answers, function(k, v){
        answer_array.push(v) 
    });
    the_scores = calculate_scores (family_id, scoring_info, config_id, answer_array);
    overall_score = calculate_friendly_score(the_scores['all']['max'], the_scores['all']['min'], the_scores['all']['score']);
    
    if (overall_score == null) {
      // No questions were answered.
      alert ('Can\'t calculate a score; no questions were answered yet.');
      return;
    }
    
    $('.score_div.score_' + overall_score ).show()
    if (between (overall_score, 0, 3)) {
      $('#low_risk').show();
    }
    if (between (overall_score, 3, 6)) {
      $('#med_risk').show();
    }
    if (between (overall_score, 6, 10)) {
      $('#hig_risk').show();
    }
    
}

$(document).ready(init);




