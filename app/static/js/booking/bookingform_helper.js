$(document).ready(function () {

    document.getElementById("bookingDate").valueAsDate = new Date();
    $.post("/bookform/getstoresincity", {city_id: $("#city").val()}, function (data) {

        appendStores(data);
        let selected = document.getElementById("store").getAttribute("selected")


        if (selected != "-1") {
            $("#store").children("option[value='" + selected + "']").attr("selected", "selected");
        }

    }, "json");

    function appendStores(data) {
        var options = "";

        $("#store").empty();
        for (let i = 0; i < data.length; i++) {
            console.log(data[i]);
            if (data[i].default == true) {
                options += "<option value='" + data[i].id + "' selected>" + data[i].address + "</option>";
            }else {
                options += "<option value='" + data[i].id + "' >" + data[i].address + "</option>";
            }
        }

        $("#store").append(options);
    }

    $("#city").on("change", function () {
        let id = $(this).val();
        $.post("/bookform/getstoresincity", {city_id: id}, function (data) {
            appendStores(data);
        }, "json");
    })
});

