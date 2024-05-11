function filterGroups() {
    var input = document.getElementById('unit_code').value.toUpperCase();
    var groups = document.getElementsByClassName('group-item');

    for (var i = 0; i < groups.length; i++) {
        var unitCode = groups[i].getAttribute('data-unit-code').toUpperCase();
        if (unitCode.indexOf(input) > -1) {
            groups[i].style.display = '';
        } else {
            groups[i].style.display = 'none';
        }
    }
}