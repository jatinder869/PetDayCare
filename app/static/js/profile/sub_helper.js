$(document).ready(function () {
    $(".sub").on("click",function () {
        let form=$(this).children(".sub-form-div");
        if(form.hasClass("hidden")){
            form.removeClass("hidden")
            form.addClass("column-center-flex")
        }else{
                        form.addClass("hidden")
            form.removeClass("column-center-flex")

        }

    }).find(".credit-input").click(function () {
        return false;
    });
});