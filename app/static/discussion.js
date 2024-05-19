$(document).ready(function() {
  // Event handler for the submit button click
  $('#submitBtn').click(function(event) {
    var errorList = $('#errorList');
    errorList.html(''); // Clear previous errors

    // Validate the question form
    if (!validateQuestionForm()) {
      event.preventDefault(); // Prevent form submission if validation fails
    } else {
      // Clear error list upon successful form submission
      errorList.html('');
    }
  });

  // Event handler for the filter button click
  $('#filterButton').click(function() {
    filterQuestions(); // Call the filterQuestions function
  });
});

// Function to filter questions based on unit code and keywords
function filterQuestions() {
  var unitCodeInput = $('#filter_code').val().toUpperCase();
  var keywordsInput = $('#keywords').val().toUpperCase();
  var questions = $('.question-item');
  var warning = $('#warning');
  var found = false;

  console.log("Filtering Unit Code:", unitCodeInput);
  console.log("Filtering Keywords:", keywordsInput);

  // Iterate over each question item
  questions.each(function() {
    var unitCode = String($(this).data('unit-code')).toUpperCase();
    var description = String($(this).data('question')).toUpperCase();

    // Check if the unit code and keywords match the question
    if (unitCode.indexOf(unitCodeInput) > -1 && description.indexOf(keywordsInput) > -1) {
      $(this).show(); // Show the question if it matches the criteria
      found = true;
      console.log("Group:", $(this).data('question-id'));
    } else {
      $(this).hide(); // Hide the question if it doesn't match the criteria
    }
  });

  // Show/hide the warning message based on whether matching questions were found
  if (!found) {
    warning.show();
  } else {
    warning.hide();
  }
}

// Function to validate the question form
function validateQuestionForm() {
  var unitCode = $('#unit_code').val().trim();
  var question = $('#question').val().trim();
  var isValid = true;
  var errorList = $('#errorList');
  errorList.empty();

  // Validate the unit code
  if (unitCode === '') {
    isValid = false;
    appendError('Unit Code is required.', errorList);
  } else if (unitCode.length !== 8) {
    isValid = false;
    appendError('Unit Code must be 8 digits long.', errorList);
  }

  // Validate the question
  if (question === '') {
    isValid = false;
    appendError('Question is required.', errorList);
  }

  return isValid;
}

// Function to append an error message to the error list
function appendError(message, errorList) {
  var li = $('<li>').text(message);
  errorList.append(li);
}
