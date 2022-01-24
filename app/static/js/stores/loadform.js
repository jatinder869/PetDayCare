$(document).ready(function () {
    $(".store-listing").on('click', function () {

        $("#form" + $(this).attr("store-id")).submit();

    });
});