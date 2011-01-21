
///FUNCTIONS USED JUST FOR RISK PAGE:
function init() {
    
    $('.score_div').hide();
    $('.risk_div').hide();
    
    //family_configs = JSON.parse($('#family_configs')[0].innerHTML);
    // aha! fixes bug #71035
    family_configs =  local_storage_get(LOCAL_STORAGE_KEY, 'list_of_family_configs') 
    
    if (family_configs [family_id] == undefined) {
        alert ("Can't find the list of weights for this family.");
    }
    
    
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
            family_url_list = all_questions[i]['url_list'];
        }
    }
    set_nav_urls (prev_next_url (family_url_list));
    
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
    
    
    //store the scores so the topic page can use them to show scores on individual topics:
    set_score_data (LOCAL_STORAGE_KEY, family_id, the_scores);
    
    
    
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




