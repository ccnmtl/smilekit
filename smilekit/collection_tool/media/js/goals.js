function maybe_hide (a, li)  {
    goal_id = li.id.split('_')[1];
    var hide_it = true;
    $.each (goal_form_fields, function (a, goal_field_code) {
        if (get_goal_text (LOCAL_STORAGE_KEY, family_id, goal_id, goal_field_code) != "")  {
            hide_it = false;
            return;
        }
      }
    );
    //console.log (hide_it);
    if (hide_it) {
        // hide it from goals to look at:   
        $(li).hide()
    }
    else {
        // hide it from goals already looked at:
        $('#other_goal_' + goal_id).hide()
    }
}


function init() {
  $.each ($('li.goal_title.used'), maybe_hide );
}

$(document).ready(init);




