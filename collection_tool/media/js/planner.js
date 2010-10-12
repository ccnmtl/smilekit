// meal planner widget
var mode = "planner";

function setMode(newMode) {
  mode = newMode;
  if(mode != "tracking" && mode != "planner") {
    mode = "planner";
  }
}

function initPlanner() {
  $('.thumbnail').click(function () {
    $(this).toggleClass('thumbnailselected');
  });
  
  $('.time').click(saveMeal);
  $('.timeactiondelete').click(deleteMeal);
  $('.timeactionup').click(moveUp);
  $('.timeactiondown').click(moveDown);
  $('.timeactionswap').click(editMeal);
  
  if(mode == "tracking") {
    $('#photobox-fluoride').hide();
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

  $('.mealorsnack', $(goodrow)).html("Meal");
  $('.activityitems', $(goodrow)).html(items);

  $(goodrow).addClass('timerowfilled');
}

function deleteMeal() {
  $(this).parent().removeClass('timerowfilled');
  
  $('.timeactivity', $(this).parent()).html("");
}

function moveUp() {
  var items = $('.timeactivity', $(this).parent()).html();

  var prevElement = $(this).parent().prevAll(".timerow:not(.timerowfilled)").first();
  if(prevElement.length > 0) {
    $('.timeactivity', prevElement).html(items);
    $(prevElement).addClass('timerowfilled');
  
    $(this).parent().removeClass('timerowfilled');
  }
}

function moveDown() {
  var items = $('.timeactivity', $(this).parent()).html();

  var nextElement = $(this).parent().nextAll(".timerow:not(.timerowfilled)").first();
  console.log(nextElement);
  if(nextElement.length > 0) {
    $('.timeactivity', nextElement).html(items);
    $(nextElement).addClass('timerowfilled');
 
    $(this).parent().removeClass('timerowfilled');
  }
}

function editMeal() {
  var mealorsnack = $('.mealorsnack', $(this).parent());
  if(mealorsnack.html() == "Meal") {
    mealorsnack.html("Snack");
  } else {
    mealorsnack.html("Meal");
  }
}

$(document).ready(initPlanner);

// TODO: load/save functionality