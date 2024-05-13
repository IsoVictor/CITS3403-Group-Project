function filter() {
    warning.style.display = 'none';
    var input = document.getElementById('unit_code').value.toUpperCase();
    var questions = document.getElementsByClassName('question-item');
    var found = false;

    for (var i = 0; i < questions.length; i++) {
        var unitCode = questions[i].getAttribute('data-unit-code').toUpperCase();
        if (unitCode.indexOf(input) > -1) {
            questions[i].style.display = '';
            found = true;
        } else {
            questions[i].style.display = 'none';
        }
    }
    if (!found) {
        warning.style.display = 'block';
    }
}