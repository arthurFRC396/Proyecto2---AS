$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#date_joined').datetimepicker();
    // $("input[name='iva']").TouchSpin({
    //     min: 0,
    //     max: 100,
    //     step: 0.1,
    //     decimals: 2,
    //     boostat: 5,
    //     maxboostedstep: 10,
    //     postfix: '%'
    // });
});