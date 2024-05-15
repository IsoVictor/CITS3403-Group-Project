function filterGroups() {
    var input = document.getElementById('filter_code').value.toUpperCase();
    var groups = document.querySelectorAll('.group-item');
    var warning = document.getElementById('warning');
    var found = false;

    // Log filtering unit code
    console.log("Filtering unit code:", input);

    for (var i = 0; i < groups.length; i++) {
        var unitCode = groups[i].getAttribute('data-unit-code').toUpperCase();
        if (unitCode.indexOf(input) > -1) {
            groups[i].style.display = '';
            found = true;
            // Log group corresponding to filtered unit code
            console.log("Group:", groups[i].getAttribute('group-id'));
        } else {
            groups[i].style.display = 'none';
        }
    }
    if (!found) {
        warning.style.display = 'block';
    } else {
        warning.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('filterButton').addEventListener('click', filterGroups);
});
