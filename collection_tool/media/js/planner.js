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
  $('.timeactionedit').click(editMeal);
  
  if(mode == "tracking") {
    $('#photobox-fluoride').hide();
  }
  
  // hide/show item boxes
  $('.photoboxhideshow').toggle(
    function() {
      $(this).html("+ Show");
      $(this).nextAll(".thumbnails").hide();
    },
    function() {
      $(this).html("- Hide");
      $(this).nextAll(".thumbnails").show();
    }
  );
  
  // collapse/expand timeline
  $('#timelinearrow').toggle(
    function() {
      $(".timerow").addClass("timerowcollapsed");
    },
    function() {
      $(".timerow").removeClass("timerowcollapsed");
    });
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

  $('.mealorsnack', $(this).parent()).html("Meal");
  $('.activityitems', $(this).parent()).html(items);

  $(this).parent().addClass('timerowfilled');
}

function deleteMeal() {
  $(this).parent().removeClass('timerowfilled');
  
  $('.timeactivity', $(this).parent()).html("");
}

function moveUp() {
  var items = $('.timeactivity', $(this).parent()).html();

  var prevElement = $(this).parent().prev();
  if(prevElement.length > 0) {
    $('.timeactivity', prevElement).html(items);
    $(prevElement).addClass('timerowfilled');
  
    $(this).parent().removeClass('timerowfilled');
  }
}

function moveDown() {
  var items = $('.timeactivity', $(this).parent()).html();

  var nextElement = $(this).parent().next();
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