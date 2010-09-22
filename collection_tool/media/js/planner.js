// meal planner widget

function initPlanner() {
  $('.thumbnail').click(function () {
    $(this).toggleClass('thumbnailselected');
  });
  
  $('.time').click(saveMeal);
  $('.timeactiondelete').click(deleteMeal);
  $('.timeactionup').click(moveUp);
  $('.timeactiondown').click(moveDown);
  $('.timeactionedit').click(editMeal);
}

function saveMeal() {
  // TODO: check to see if any thumbnails are selected
  $(this).parent().removeClass('timerow');
  $(this).parent().addClass('timerowfilled');
  
  var items = "";
  $('.thumbnailselected').each(function() {
    var label = $('.thumbnaillabel', this).html();
    items += label + ", ";
  });
  if(items != "") {
    items = items.slice(0, -2);
  }
  $('.mealorsnack', $(this).parent()).html("Meal");
  $('.activityitems', $(this).parent()).html(items);
}

function deleteMeal() {
  $(this).parent().addClass('timerow');
  $(this).parent().removeClass('timerowfilled');
  
  $('.timeactivity', $(this).parent()).html("");
}

function moveUp() {
  var items = $('.timeactivity', $(this).parent()).html();

  var prevElement = $(this).parent().prev();
  if(prevElement.length > 0) {
    $('.timeactivity', prevElement).html(items);
    $(prevElement).addClass('timerowfilled');
    $(prevElement).removeClass('timerow');
  
    $(this).parent().addClass('timerow');
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
    $(nextElement).removeClass('timerow');
  
    $(this).parent().addClass('timerow');
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

// connect all times so when clicked on, currently selected thumbnails
// are saved into time div.

// buttons: delete, move up/down, edit, toggle snack/meal

// TODO: load/save functionality