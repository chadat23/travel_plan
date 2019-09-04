count = 0;
inputs1 = '<div>Is this working ' + count.toString() + '</div>';
names = ['patroller_name', 'callsign', 'packcolor'];

function line(count) {
    return '<div class="row">'
           + '<input type="text" name="p' + count + names[0] + '" placeholder="Name" class="col-xl-4" value=""/> '
           + '<input type="text" name="p' + count + names[1] + '" placeholder="Call Sign" class="col-xl-4" value=""/> '
           +' <input type="text" name="p' + count + names[2] + '" placeholder="Pack Color" class="col-xl-4" value=""/> '
           // +' <input type="text" name="nusers" value="' + count + '" disabled style="visibility: hidden"/>'
           +'</div>'
}

function get_values(count) {
    values = {};
    var i;
    var j;
    for (i = 0; i < count; i++) {
        for (j = 0; j < names.length; j++){
            n = 'planning' + i + names[j];
            val = document.getElementsByName(n)[0].value;
            console.log('val', val, n)
            if (val === undefined) {
                val = '';
            }
            values[n] = val;
        }
    }

    return values
}

function update_values(values) {
    for (k in values) {
        document.getElementsByName(k)[0].value = values[k]
    }
}

document.getElementById('add-patroller-btn').onclick = function () {
    document.getElementsByName('npatrollers')[0].value = 0;

    values = get_values(count);

    document.getElementById('added-patroller').innerHTML += line(count);

    update_values(values);

    count += 1;

    document.getElementsByName('npatrollers')[0].value = count;
};