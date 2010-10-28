// meal planner widget
var mode = "all";  // options: food, fluoride, all
var savingFluoride = false;

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
  }
  if(mode == "fluoride") {
    jQuery('.timeactionswap').hide();
    jQuery('.timeactiondelete').css('right', '100px');
    //jQuery('.mealorsnack').hide();
    jQuery('#photobox-foods').hide();
    jQuery('#photobox-drinks').hide();
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
  jQuery('.thumbnailselected').each(function() {
    var label = jQuery('.thumbnaillabel', this).html();
    items += label + ", ";
    jQuery(this).removeClass('thumbnailselected');
  });
  if(items == "") { return; }  // nothing was selected

  items = items.slice(0, -2);
  
  var goodrow = findNearestEmpty(jQuery(this).parent());

  if(savingFluoride) {
    jQuery('.mealorsnack', jQuery(goodrow)).hide();
    savingFluoride = false;
  }
  else {
    jQuery('.mealorsnack', jQuery(goodrow)).html("<span id=\"label-snack\">Snack</span>");
  }
  jQuery('.activityitems', jQuery(goodrow)).html(items);

  jQuery(goodrow).toggleClass('timerowfilled');

  // re-enable any disabled items
  jQuery('.thumbnaildisabled').removeClass('thumbnaildisabled');
}

function deleteMeal() {
  jQuery(this).parent().toggleClass('timerowfilled');
  jQuery('.timeactivity', jQuery(this).parent()).html("");
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
  console.log(nextElement);
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