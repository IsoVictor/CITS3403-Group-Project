function filterGroups() {
    warning.style.display = 'none';
    var input = document.getElementById('unit_code').value.toUpperCase();
    var groups = document.getElementsByClassName('group-item');
    var found = false;

    for (var i = 0; i < groups.length; i++) {
        var unitCode = groups[i].getAttribute('data-unit-code').toUpperCase();
        if (unitCode.indexOf(input) > -1) {
            groups[i].style.display = '';
            found = true;
        } else {
            groups[i].style.display = 'none';
        }
    }
    if (!found) {
        warning.style.display = 'block';
    }
}