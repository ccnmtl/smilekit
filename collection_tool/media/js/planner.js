// meal planner widget
var mode = "all";  // options: food, fluoride, all
var savingFluoride = false;

function saveState() {
  // save state to localstorage
  var testblob = jQuery("#timetable").html();
  //local_storage_set(LOCAL_STORAGE_KEY, 'planner_data', {'timeline': testblob});

  set_planner_data(LOCAL_STORAGE_KEY, family_id,{"timeline": testblob })

  if(mode == "food") {
    /* calculate risk # */
    var risky_exposures = 0;
    jQuery(".timerowfilled .activityitems").each(function() {
      var risk = jQuery(this).data('risk');
      // an average of 3 or higher is 'risky'
      if(risk >= 3) { risky_exposures++; }
    });

    // store answer to "risky exposures" question
    // 3 bins - 0 risky events, 1-2 risky events, 3 or more risky events
    var key = '3 or more';
    if(risky_exposures == 0) {
      key = '0';
    }
    else if(risky_exposures < 3) {
      key = '1-2';
    }
    var answer_id = risky_answers_values[risky_answers_keys.indexOf(key)];
    store_answer(risky_question_id, answer_id);
  }
  
  if(mode == "fluoride") {
    var fluoride_times = 0;
    var brushing_times = 0;
    jQuery(".timerowfilled .activityitems").each(function() {
      if(jQuery(this).html().indexOf("brush teeth") != -1) {
        brushing_times++;
      }
      if(jQuery(this).html().indexOf("fluoride rinse") != -1) {
        fluoride_times++;
      }
    });
    
    // store answers to fluoride questions in database
    // fluoride rinse exposures: "none", "once", "twice or more"
    var fluoride_key = "twice or more";
    if(fluoride_times == 0) {
      fluoride_key = "none";
    }
    else if(fluoride_times == 1) {
      fluoride_key = "once"
    }

    // daily toothbrushing: "none", "once", "twice or more"
    var brushing_key = "twice or more";
    if(brushing_times == 0) { brushing_key = "none"; }
    else if(brushing_times == 1) { brushing_key = "once"; }
  
    var fluoride_answer_id = fluoride_answers_values[fluoride_answers_keys.indexOf(fluoride_key)];
    store_answer(fluoride_question_id, fluoride_answer_id);
    var brushing_answer_id = brushing_answers_values[brushing_answers_keys.indexOf(brushing_key)];
    store_answer(brushing_question_id, brushing_answer_id);
  }
}



function loadState() {
  // load state from localstorage
  //var test = local_storage_get(LOCAL_STORAGE_KEY, 'planner_data');
  
  var test = get_planner_data (LOCAL_STORAGE_KEY, family_id);
  
  if ((test == null) || (test['timeline'] == "")) {
    return;
  }
  
  jQuery("#timetable").html(test['timeline']);
  
  // reset clicky stuff 'cause it breaks
  jQuery('.time').click(saveMeal);
  jQuery('.timeactiondelete').click(deleteMeal);
  jQuery('.timeactionup').click(moveUp);
  jQuery('.timeactiondown').click(moveDown);
  jQuery('.timeactionswap').click(editMeal);

  jQuery('.arrowclose').click(
    function() {
      jQuery('.arrowclose').hide();
      jQuery('.arrowopen').show();
      jQuery('.timerow').addClass("timerowcollapsed");
      jQuery('#plannerright').show();
      jQuery('#plannerleft').width(100);
    }
  );
  jQuery('.arrowopen').click(
    function() {
      jQuery('.arrowclose').show();
      jQuery('.arrowopen').hide();
      jQuery('.timerow').removeClass("timerowcollapsed");
      jQuery('#plannerright').hide();
      jQuery('#plannerleft').width("95%");
    }
  );
}


function setMode(newMode) {
  mode = newMode;
  if(mode != "food" && mode != "fluoride" && mode != "all") {
    mode = "all";
  }
}

function initPlanner() {
  jQuery('.thumbnail').click(function () {
    if(jQuery(this).hasClass('thumbnaildisabled')) { return; }
    jQuery(this).toggleClass('thumbnailselected');

    var id= jQuery(this).parent().parent('.photoboxcontainer').attr('id');
    if(jQuery(this).hasClass('thumbnailselected')) {
      if(id == "photoboxcontainer-fluoride") {
        // disable all non-fluoride items
        jQuery('.photoboxcontainer').not('#photoboxcontainer-fluoride').children().children('.thumbnail').each(function() {
          jQuery(this).addClass('thumbnaildisabled');
          savingFluoride = true;
        });
      }
      else {
        // disable fluoride items
        jQuery('#photoboxcontainer-fluoride').children().children('.thumbnail').each(function() {
          jQuery(this).addClass('thumbnaildisabled');
          savingFluoride = false;
        });
      }
    }
    else {
      // if nothing is selected, enable all choices again
      if( jQuery('.thumbnailselected').length == 0) {
        jQuery('.thumbnaildisabled').removeClass('thumbnaildisabled');
      }
    }

  });
  
  jQuery('.time').click(saveMeal);
  jQuery('.timeactiondelete').click(deleteMeal);
  jQuery('.timeactionup').click(moveUp);
  jQuery('.timeactiondown').click(moveDown);
  jQuery('.timeactionswap').click(editMeal);
  
  if(mode == "food") {
    jQuery('#photobox-fluoride').hide();
    //jQuery('.timeactiondelete').disable();
  }
  if(mode == "fluoride") {
    jQuery('.timeactionswap').hide();
    jQuery('.timeactiondelete').css('right', '100px');
    //jQuery('.mealorsnack').hide();
    jQuery('#photobox-foods').hide();
    jQuery('#photobox-drinks').hide();
    //jQuery('.timeactiondelete').disable(); 
  }
  
  // hide/show item boxes
  jQuery('.photoboxhideshow').toggle(
    function() {
      jQuery(this).html("+");
      jQuery(this).nextAll(".thumbnails").hide();
    },
    function() {
      jQuery(this).html("-");
      jQuery(this).nextAll(".thumbnails").show();
    }
  );
  
  // collapse/expand timeline
  jQuery('.arrowclose').click(
    function() {
      jQuery('.arrowclose').hide();
      jQuery('.arrowopen').show();
      jQuery('.timerow').addClass("timerowcollapsed");
      jQuery('#plannerright').show();
      jQuery('#plannerleft').width(100);
    }
  );
  jQuery('.arrowopen').click(
    function() {
      jQuery('.arrowclose').show();
      jQuery('.arrowopen').hide();
      jQuery('.timerow').removeClass("timerowcollapsed");
      jQuery('#plannerright').hide();
      jQuery('#plannerleft').width("95%");
    }
  );
  
  // save and cancel buttons
  loadState();
  jQuery('#right').click(saveState);
  jQuery('#left').click(saveState);
}

function findNearestEmpty(elem) {
  if( ! jQuery(elem).hasClass("timerowfilled") ) {
    return elem;
  }

  var next = jQuery(elem).next(".timerow");
  var prev = jQuery(elem).prev(".timerow");

  var found = false;
  while( !found && ( (next.length > 0) || (prev.length > 0) ) ) {
    if( (next.length > 0) && (! jQuery(next).hasClass("timerowfilled"))) {
      found = next;
    }
    else if( (prev.length > 0) && (! jQuery(prev).hasClass("timerowfilled"))) {
      found = prev;
    }
    else {
      next = jQuery(next).next(".timerow");
      prev = jQuery(prev).prev(".timerow");
    }
  }
  
  return found;
}

function saveMeal() {
  var items = "";
  var total_risk = 0;
  var num_items = 0;
  jQuery('.thumbnailselected').each(function() {
    var label = jQuery('#'+this.id+'-label').html();
    items += label + ", ";
    var risk = parseInt(jQuery('#'+this.id+'-risk').val());
    total_risk += risk;
    num_items++;
    jQuery(this).removeClass('thumbnailselected');
  });
  if(num_items == 0) { return; }  // nothing was selected

  var avg_risk = total_risk / num_items;

  items = items.slice(0, -2); // take off the final ", "
  
  // skip to the next valid row if this one is already full
  var goodrow = findNearestEmpty(jQuery(this).parent());

  if(savingFluoride) {
    jQuery('.mealorsnack', jQuery(goodrow)).hide();
    savingFluoride = false;
  }
  else {
    jQuery('.mealorsnack', jQuery(goodrow)).html("<span id=\"label-snack\">Snack</span>");
  }
  jQuery('.activityitems', jQuery(goodrow)).html(items);
  jQuery('.activityitems', jQuery(goodrow)).data("risk", avg_risk);

  jQuery(goodrow).toggleClass('timerowfilled');

  // re-enable any disabled items
  jQuery('.thumbnaildisabled').removeClass('thumbnaildisabled');
}

function deleteMeal() {
  jQuery(this).parent().toggleClass('timerowfilled');
  jQuery('.mealorsnack', jQuery(this).parent()).html("");
  jQuery('.activityitems', jQuery(this).parent()).html("");
  jQuery('.activityitems', jQuery(this).parent()).removeData();
}

function moveUp() {
  var items = jQuery('.timeactivity', jQuery(this).parent()).html();

  var prevElement = jQuery(this).parent().prevAll(".timerow:not(.timerowfilled)").first();
  if(prevElement.length > 0) {
    jQuery('.timeactivity', prevElement).html(items);
    jQuery(prevElement).toggleClass('timerowfilled');
  
    jQuery(this).parent().toggleClass('timerowfilled');
  }
}

function moveDown() {
  var items = jQuery('.timeactivity', jQuery(this).parent()).html();

  var nextElement = jQuery(this).parent().nextAll(".timerow:not(.timerowfilled)").first();
  if(nextElement.length > 0) {
    jQuery('.timeactivity', nextElement).html(items);
    jQuery(nextElement).toggleClass('timerowfilled');
 
    jQuery(this).parent().toggleClass('timerowfilled');
  }
}

function editMeal() {
  var mealorsnack = jQuery('.mealorsnack', jQuery(this).parent());
  if(mealorsnack.html() == "\<span\ id\=\"label-meal\"\>Meal\<\/span\>") {
    mealorsnack.html("<span id=\"label-snack\">Snack</span>");
  } else {
    mealorsnack.html("<span id=\"label-meal\">Meal</span>");
  }
}

jQuery(document).ready(initPlanner);

// TODO: load/save functionality
