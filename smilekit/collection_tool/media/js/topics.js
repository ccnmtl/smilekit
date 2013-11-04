function show_topic_details (topic_id) {
    $('.topic_div').hide();
    $('.topic_div.topic_' + topic_id).show();
}


var family_id;

function bound_show_topic_details(tid) {
    return function () {
        show_topic_details(tid);
    }
}



function decorate_firebutton (index, my_div) {
    tid = my_div.getAttribute('topic_id');
    $(my_div).click(bound_show_topic_details(tid));
    
    
    try {
      score =  score_data_for_topic_id (LOCAL_STORAGE_KEY, family_id, tid);
      
      if (topic_is_irrelevant (LOCAL_STORAGE_KEY, family_id, tid)) {
      /// no matter how many questions you answered on this topic, your answers are irrelevant.
        $(my_div).addClass( 'topic_irrelevant' );
      }
      else {
              score_class = 'topic_score_' + score;
              if (score == -1 ) {
                   $(my_div).addClass( 'topic_no_score' );
              }
              else {
                  $(my_div).addClass( score_class );
              }
      }
      
      completed = answered_all_questions (LOCAL_STORAGE_KEY, family_id, tid);      
      if (completed ) {
           $(my_div).addClass( 'topic_completed' );
      }
      
    }
    catch (e) {
      // score data for topic id shouldn't throw any errors.
      log_wrapper ('enh');
    } 
     
    //score = score_data_for_topic_id (LOCAL_STORAGE_KEY, family_id, 1);
    //alert (score);
}

function init() {
    $('.topic_div').hide();
    family_id = local_storage_get (LOCAL_STORAGE_KEY, 'current_family_id');
    $('.firebutton').each(decorate_firebutton);

}

$(document).ready(init);




