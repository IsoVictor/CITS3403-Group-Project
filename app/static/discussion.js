$(document).ready(function() {
    $('#submitBtn').click(function(event) {
        var errorList = $('#errorList');
        errorList.html(''); // Clear previous errors
        if (!validateQuestionForm()) {
            event.preventDefault(); 
        } else {
            // Clear error list upon successful form submission
            errorList.html('');
        }
    });

    $('#filterButton').click(function() {
        filterQuestions();
    });
});

function filterQuestions(){
    var unitCodeInput = $('#filter_code').val().toUpperCase();
        var keywordsInput = $('#keywords').val().toUpperCase();
        var questions = $('.question-item');
        var warning = $('#warning');
        var found = false;

        console.log("Filtering Unit Code:", unitCodeInput);
        console.log("Filtering Keywords:", keywordsInput);

        questions.each(function() {
            var unitCode = String($(this).data('unit-code')).toUpperCase();
            var description = String($(this).data('question')).toUpperCase();
            if (unitCode.indexOf(unitCodeInput) > -1 && description.indexOf(keywordsInput) > -1) {
                $(this).show();
                found = true;
                console.log("Group:", $(this).data('question-id'));
            } else {
                $(this).hide();
            }
        });

        if (!found) {
            warning.show();
        } else {
            warning.hide();
        }
    }

function validateQuestionForm() {
    var unitCode = $('#unit_code').val().trim();
    var question = $('#question').val().trim();
    var isValid = true;
    var errorList = $('#errorList');
    errorList.empty();

    if (unitCode === '') {
        isValid = false;
        appendError('Unit Code is required.', errorList);
    } else if (unitCode.length !== 8) {
        isValid = false;
        appendError('Unit Code must be 8 digits long.', errorList);
    }

    if (question === '') {
        isValid = false;
        appendError('Question is required.', errorList);
    }

    return isValid;
}

function appendError(message, errorList) {
    var li = $('<li>').text(message);
    errorList.append(li);
}