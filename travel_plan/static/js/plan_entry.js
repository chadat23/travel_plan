var gar_amber = 36;
var gar_red = 61;

function int0(x) {
    var parsed = parseInt(x);
    if (isNaN(parsed)) { return 0 }
    return parsed;
  }

function gar_math() {
    var i = 0;
    var j = 0;
    var grand_total = 0;
    
    while($("[name='supervision" + i.toString() + "']").length) {
        var supervision = $("[name='supervision" + i.toString() + "']").val();
        var planning = $("[name='planning" + i.toString() + "']").val();
        var contingency = $("[name='contingency" + i.toString() + "']").val();
        var comms = $("[name='comms" + i.toString() + "']").val();
        var teamselection = $("[name='teamselection" + i.toString() + "']").val();
        var fitness = $("[name='fitness" + i.toString() + "']").val();
        var env = $("[name='env" + i.toString() + "']").val();
        var complexity = $("[name='complexity" + i.toString() + "']").val();

        var total = int0(supervision) + int0(planning) + int0(contingency) + int0(comms) + int0(teamselection) + int0(fitness) + int0(env) + int0(complexity);
        if (total > 0) {
            $("[name='total" + i.toString() + "']").val(total);

            $("[name='total" + i.toString() + "']").removeClass('gar-green');
            $("[name='total" + i.toString() + "']").removeClass('gar-amber');
            $("[name='total" + i.toString() + "']").removeClass('gar-red');

            if (total < gar_amber) {$("[name='total" + i.toString() + "']").addClass('gar-green');}
            else if (total < gar_red) {$("[name='total" + i.toString() + "']").addClass('gar-amber');}
            else {$("[name='total" + i.toString() + "']").addClass('gar-red');}

            grand_total += total;
            j += 1;
        }        
        
        i += 1;
    }
    if (grand_total > 0) {
        avg = grand_total / j;

        $("[name='garavg']").val(avg);

        $("[name='garavg']").removeClass('gar-green');
        $("[name='garavg']").removeClass('gar-amber');
        $("[name='garavg']").removeClass('gar-red');

        if (avg < gar_amber) {$("[name='garavg']").addClass('gar-green');}
        else if (avg < gar_red) {$("[name='garavg']").addClass('gar-amber');}
        else {$("[name='garavg']").addClass('gar-red');}
    }
};



$('[name^="supervision"]').blur(function() {
    gar_math();
    });

$('[name^="planning"]').blur(function() {
    gar_math();
    });

$('[name^="contingency"]').blur(function() {
    gar_math();
    });

$('[name^="comms"]').blur(function() {
    gar_math();
    });

$('[name^="teamselection"]').blur(function() {
    gar_math();
    });

$('[name^="fitness"]').blur(function() {
    gar_math();
    });

$('[name^="env"]').blur(function() {
    gar_math();
    });

$('[name^="complexity"]').blur(function() {
    gar_math();
    });

$('[name="mitigatedgar"]').blur(function() {
    $("[name='mitigatedgar']").removeClass('gar-green')
    $("[name='mitigatedgar']").removeClass('gar-amber')
    $("[name='mitigatedgar']").removeClass('gar-red')

    value = $("[name='mitigatedgar']").val()

    if (value < gar_amber) {$("[name='mitigatedgar']").addClass('gar-green')}
    else if (value < gar_red) {$("[name='mitigatedgar']").addClass('gar-amber')}
    else {$("[name='mitigatedgar']").addClass('gar-red')}
    });

function autofill_contact_info(index) {
    $.getJSON($SCRIPT_ROOT + '/traveler/get-responsible-party-info', {
        name: $('[name="contactname' + index + '"]').val()
    }, function(data) {
        $('[name="contactemail' + index + '"]').val(data.email);
        $('[name="contactwork' + index + '"]').val(data.work_number);
        $('[name="contacthome' + index + '"]').val(data.home_number);
        $('[name="contactcell' + index + '"]').val(data.cell_number);
    });
    return false;
    }

$('[name="contactname0"]').blur(function() {
    autofill_contact_info('0')
    });  


$('[name="contactname1"]').blur(function() {
    autofill_contact_info('1')
    });


$('[name="carplate"]').blur(function() {
    $.getJSON($SCRIPT_ROOT + '/vehicle/get-vehicle-info', {
        plate: $('[name="carplate"]').val()
    }, function(data) {
        console.log('going')
        $('[name="carplate"]').val(data.plate);
        $('[name="carmake"]').val(data.make);
        $('[name="carmodel"]').val(data.model);
        $('[name="carcolor"]').val(data.color);
    });
    return false;
    });

function autofill_travelerunit_info(index) {
    $.getJSON($SCRIPT_ROOT + '/travel/get-travelunit-info', {
        name: $('[name="travelername' + index + '"]').val()
    }, function(data) {
        $('[name="callsign' + index + '"]').val(data.callsign);
        $('[name="packcolor' + index + '"]').val(data.work_number);
        $('[name="tentcolor' + index + '"]').val(data.home_number);
        $('[name="flycolor' + index + '"]').val(data.cell_number);
    });
    return false;
    }

$('[name="travelername0"]').blur(function() {
    autofill_contact_info('0')
    });



