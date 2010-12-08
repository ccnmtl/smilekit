
function get_goals_data(LOCAL_STORAGE_KEY, family_id) {
  goals_data =  get_state_data(LOCAL_STORAGE_KEY, family_id, 'goals_data');
  
  // just set to empty object if nothing is found:
  if (goals_data == null) {
    return {}
  }
  return goals_data;
}

function set_goals_data(LOCAL_STORAGE_KEY, family_id, blob) {
  var key =  'goals_data';
  set_state_data(LOCAL_STORAGE_KEY, family_id, key, blob);
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


function set_score_data (LOCAL_STORAGE_KEY, family_id, score_data) {
        tmp = get_goals_data(LOCAL_STORAGE_KEY, family_id);
        tmp['score_data'] = score_data;
        set_goals_data(LOCAL_STORAGE_KEY, family_id, tmp);
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


function calculate_scores (family_id, scoring_info, config_id, answer_array) {

    // Takes your scoring info and figures out, for each topic and for all topics combined,
    // what the best and possible worst scores you could
    // have gotten based on the questions you answered.
    // The return value is:
    /*
      { 
          'all' : {
                    'min': x,
                    'max': y,
                    'score': z,
           },
           
           // and then, for each topic id:
           
           'tid1' : {
                    'min': x,
                    'max': y,
                    'score': z,
           },
           
           'tid2' : {
                    'min': x,
                    'max': y,
                    'score': z,
           },
           
           // etc.
           ...
           
      }
    
    
    */
    
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
   if (range_of_possible_scores == 0) {
      // you need to answer a question to get a score, sorry.
      return null;
   }
   adjusted_score = raw_score - min_score;
   // Friendly score: 1 is good, 10 is a lot of risk:
   friendly_score =    1 + Math.round ( 9.0 * adjusted_score /  range_of_possible_scores ) ;
 
   
   if (true ) {
       log_wrapper ( "User's raw score is " + raw_score);
       log_wrapper ( "Worst possible score is : " + max_score );
       log_wrapper ( "Best possible score is : " +  min_score );
       log_wrapper ( "Adjusted score : " +  adjusted_score );
       log_wrapper ( "Friendly score is " + friendly_score);
   }
   return friendly_score;
}

function between (x, a, b) {
  return a < x && x <= b;
}


function score_data_for_topic_id (LOCAL_STORAGE_KEY, family_id, topic_id) {
        try {
            score_data = get_goals_data(LOCAL_STORAGE_KEY, family_id)['score_data'][topic_id];
        } catch (e){
            return -1
        } 
        if (score_data['min'] == score_data['max'] ) {
            return -1;
        }
        return calculate_friendly_score (score_data['max'], score_data['min'], score_data['score']);
}

// i'm moving this here and out of the other files that depend on this:
family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');

