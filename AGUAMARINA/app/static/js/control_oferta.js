function prueba() {
            $.ajax({
                url: window.location.pathname, //window.location.pathname
                type: 'POST',
                data: {
                    'action': 'prueba'
                },
                dataType: 'json',
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });

}
