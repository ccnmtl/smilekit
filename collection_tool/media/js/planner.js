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
  $('.thumbnail').click(function () {
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
  
  $('.time').click(saveMeal);
  $('.timeactiondelete').click(deleteMeal);
  $('.timeactionup').click(moveUp);
  $('.timeactiondown').click(moveDown);
  $('.timeactionswap').click(editMeal);
  
  if(mode == "food") {
    $('#photobox-fluoride').hide();
  }
  if(mode == "fluoride") {
    $('.timeactionswap').hide();
    $('.timeactiondelete').css('right', '100px');
    //$('.mealorsnack').hide();
    $('#photobox-foods').hide();
    $('#photobox-drinks').hide();
  }
  
  // hide/show item boxes
  $('.photoboxhideshow').toggle(
    function() {
      $(this).html("+");
      $(this).nextAll(".thumbnails").hide();
    },
    function() {
      $(this).html("-");
      $(this).nextAll(".thumbnails").show();
    }
  );
  
  // collapse/expand timeline
  $('.arrowclose').click(
    function() {
      $('.arrowclose').hide();
      $('.arrowopen').show();
      $('.timerow').addClass("timerowcollapsed");
      $('#plannerright').show();
      $('#plannerleft').width(100);
    }
  );
  $('.arrowopen').click(
    function() {
      $('.arrowclose').show();
      $('.arrowopen').hide();
      $('.timerow').removeClass("timerowcollapsed");
      $('#plannerright').hide();
      $('#plannerleft').width("95%");
    }
  );
}

function findNearestEmpty(elem) {
  if( ! $(elem).hasClass("timerowfilled") ) {
    return elem;
  }

  var next = $(elem).next(".timerow");
  var prev = $(elem).prev(".timerow");

  var found = false;
  while( !found && ( (next.length > 0) || (prev.length > 0) ) ) {
    if( (next.length > 0) && (! $(next).hasClass("timerowfilled"))) {
      found = next;
    }
    else if( (prev.length > 0) && (! $(prev).hasClass("timerowfilled"))) {
      found = prev;
    }
    else {
      next = $(next).next(".timerow");
      prev = $(prev).prev(".timerow");
    }
  }
  
  return found;
}

function saveMeal() {
  var items = "";
  $('.thumbnailselected').each(function() {
    var label = $('.thumbnaillabel', this).html();
    items += label + ", ";
    $(this).removeClass('thumbnailselected');
  });
  if(items == "") { return; }  // nothing was selected

  items = items.slice(0, -2);
  
  var goodrow = findNearestEmpty($(this).parent());

  if(savingFluoride) {
    jQuery('.mealorsnack', jQuery(goodrow)).hide();
    savingFluoride = false;
  }
  else {
    $('.mealorsnack', $(goodrow)).html("Snack: ");
  }
  $('.activityitems', $(goodrow)).html(items);

  $(goodrow).toggleClass('timerowfilled');

  // re-enable any disabled items
  jQuery('.thumbnaildisabled').removeClass('thumbnaildisabled');
}

function deleteMeal() {
  $(this).parent().toggleClass('timerowfilled');
  $('.timeactivity', $(this).parent()).html("");
}

function moveUp() {
  var items = $('.timeactivity', $(this).parent()).html();

  var prevElement = $(this).parent().prevAll(".timerow:not(.timerowfilled)").first();
  if(prevElement.length > 0) {
    $('.timeactivity', prevElement).html(items);
    $(prevElement).toggleClass('timerowfilled');
  
    $(this).parent().toggleClass('timerowfilled');
  }
}

function moveDown() {
  var items = $('.timeactivity', $(this).parent()).html();

  var nextElement = $(this).parent().nextAll(".timerow:not(.timerowfilled)").first();
  console.log(nextElement);
  if(nextElement.length > 0) {
    $('.timeactivity', nextElement).html(items);
    $(nextElement).toggleClass('timerowfilled');
 
    $(this).parent().toggleClass('timerowfilled');
  }
}

function editMeal() {
  var mealorsnack = $('.mealorsnack', $(this).parent());
  if(mealorsnack.html() == "Meal: ") {
    mealorsnack.html("Snack: ");
  } else {
    mealorsnack.html("Meal: ");
  }
}

$(document).ready(initPlanner);

// TODO: load/save functionality