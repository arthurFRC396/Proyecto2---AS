var vents ={
    items:{
        cli:'',
        date_joined:'',
        subtotal:0.00,
        iva: 0.00,
        total: 0.00,
        products:[]
    },
    add: function () {
        
    }
};



$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'en',
        minDate: moment().format("YYYY-MM-DD")
    });

    $('#iva').TouchSpin({
        min: -6,
        max: 6,
        step: 0.25,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10
    }).change(function () {
        var val = $(this).val();
        if (parseFloat(val) > 0) {
            $(this).val("+" + val);//add + for positive numbers
        }
    });
$('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            console.log(vents.items);
            vents.add(ui.item);
            $(this).val('');
        }
    });


});