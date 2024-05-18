$(document).ready(function() {
    $('#submitBtn').click(function(event) {
        var errorList = $('#errorList');
        errorList.html(''); // Clear previous errors
        if (!validateGroupForm()) {
            event.preventDefault(); 
        } else {
            // Clear error list upon successful form submission
            errorList.html('');
        }
    });

    $('#filterButton').click(function() {
        filterGroups();
    });
});

function filterGroups(){
    var unitCodeInput = $('#filter_code').val().toUpperCase();
    var keywordsInput = $('#keywords').val().toUpperCase();
    var groups = $('.group-item');
    var warning = $('#warning');
    var found = false;

    // Log filtering inputs
    console.log("Filtering Unit Code:", unitCodeInput);
    console.log("Filtering Keywords:", keywordsInput);

    groups.each(function() {
        var unitCode = String($(this).data('unit-code')).toUpperCase(); // Ensure value is converted to string
        var description = String($(this).data('description')).toUpperCase(); // Ensure value is converted to string
        if ((unitCode.indexOf(unitCodeInput) > -1) && (description.indexOf(keywordsInput) > -1)) {
            $(this).show();
            found = true;
            // Log group corresponding to filtered inputs
            console.log("Group:", $(this).data('group-id'));
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
    

function validateGroupForm() {
    var unitCode = $('#unit_code').val().trim();
    var location = $('#location').val().trim();
    var date = $('#dateof').val().trim();
    var time = $('#time').val().trim();
    var description = $('#description').val().trim();
    var isValid = true;
    var errorList = $('#errorList');
    errorList.html(''); // Clear previous errors

    if (unitCode === '') {
        isValid = false;
        appendError('Unit Code is required.', errorList);
    } else if (unitCode.length !== 8) {
        isValid = false;
        appendError('Unit Code must be 8 digits long.', errorList);
    }

    if (location === '') {
        isValid = false;
        appendError('Location is required.', errorList);
    }

    if (date === '') {
        isValid = false;
        appendError('Date is required.', errorList);
    } else if (new Date(date) < new Date()) {
        isValid = false;
        appendError('Date cannot be before the current date.', errorList);
    }

    if (time === '') {
        isValid = false;
        appendError('Time is required.', errorList);
    }

    if (description === '') {
        isValid = false;
        appendError('Description is required.', errorList);
    }

    return isValid;
}

function appendError(message, errorList) {
    var li = $('<li>').text(message);
    errorList.append(li);
}