


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


goal_form_fields = ['name','resp', 'stps', 'when'];


function set_goal_text (LOCAL_STORAGE_KEY, family_id, goal_id, goal_field_code, goal_text ) {
  tmp = get_goals_data(LOCAL_STORAGE_KEY, family_id);
  key = goal_id + '_' + goal_field_code;
  tmp[key] = goal_text;
  set_goals_data(LOCAL_STORAGE_KEY, family_id, tmp);
}


function get_goal_text (LOCAL_STORAGE_KEY, family_id, goal_id, goal_field_code) {
  key = goal_id + '_' + goal_field_code;
  try {
     goal_text = get_goals_data(LOCAL_STORAGE_KEY, family_id)[key];
     if (goal_text != null) {
      return goal_text
     }
  } catch (e){
      // Have a nice day.
  }
  return '';
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
      // TODO: remove this once test families are excised.
      if (qid != 23 && qid != 22) {
      /// IGNORE TWO OBSOLETE QUESIONS.
        if (calculate_family_answers_result [qid] == null) {
            calculate_family_answers_result [qid] = aid;
          }
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

function irrelevant (topic_id, config_id) {
  return maxmin_scoring_info[topic_id][config_id]['irrelevant'];
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
    $.each(scoring_info, function (tid) {
        // for each topic:
        //llog ("topic is now " + tid);
        result[tid] = {'score': 0, 'max':0, 'min':0, 'answered_count':0, 'question_count':0};
        
        // how many questions count toward this topic, including unanswered ones?
        result[tid]['question_count']  = scoring_info[tid][config_id]['question_count'];
        result[tid]['irrelevant'] = irrelevant (tid, config_id);

        //llog (answer_array);
        
        for (i = 0; i < answer_array.length; i = i + 1) {
            // for each answer:
            answer_id = answer_array[i]
            found_score = the_score_for (tid, config_id, answer_id);
            if (found_score != null) {
                // this answer counts towards this topic.
                //llog (" answer " + answer_id + " counts towards " + tid );
                // overall score:
                result['all']['score'] += found_score;
                result['all']['min']   += min_score_for  (tid, config_id, answer_id);
                result['all']['max']   += max_score_for  (tid, config_id, answer_id);
                
                // score for this topic (used on the Topics screen:
                result[tid]['score']   += found_score;
                result[tid]['min']     += min_score_for  (tid, config_id, answer_id);
                result[tid]['max']     += max_score_for  (tid, config_id, answer_id);
                result[tid]['answered_count']     ++;
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
 
   
   if (false ) {
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
      //llog (score_data);
  } catch (e){
      return -1
  } 
  if (score_data['min'] == score_data['max'] ) {
      return -1;
  }
  return calculate_friendly_score (score_data['max'], score_data['min'], score_data['score']);
}


function topic_is_irrelevant (LOCAL_STORAGE_KEY, family_id, topic_id) {
  try {
      score_data = get_goals_data(LOCAL_STORAGE_KEY, family_id)['score_data'][topic_id];
      return (score_data['irrelevant'] == 'true');
  } catch (e){
      return true
  }
  return true;
}




function answered_all_questions (LOCAL_STORAGE_KEY, family_id, topic_id) {
 try {
     score_data = get_goals_data(LOCAL_STORAGE_KEY, family_id)['score_data'][topic_id];
     return (score_data['answered_count'] >= score_data['question_count'])
 } catch (e){
      return -1
 }
 return false;
}

var family_id;

function risk_topics_init() {
  family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
  set_family_id_in_nav ( family_id);
  set_assessment_url (); // so a click on "assessment" will go back to the most recent question or index page.
}

$(document).ready( risk_topics_init );

