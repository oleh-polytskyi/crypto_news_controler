$(document).ready(function() {
    $("#main-form").validate({
        rules: {
            day_of_week: {
                number: true,
                min: 0,
                max: 6
            },
            hour: {
                number: true,
                min: 0,
                max: 23
            },
            minute: {
                number: true,
                min: 0,
                max: 59
            }
        },
        messages: {
            day_of_week: {
                min: "Number of day_of_week must be start from 0",
                max: "Number of day_of_week must be less then 6"
            },
            hour: {
                min: "Number of hour must be start from 0",
                max: "Number of hour must be less then 23"
            },
            minute: {
                min: "Number of minute must be start from 0",
                max: "Number of minute must be less then 59"
            }
        },
        submitHandler: save_data
    });
})

function save_data() {
    var token = "{{csrf_token}}";
    var day_of_week = $("#day_of_week").val();
    var hour = $("#hour").val();
    var minute = $("#minute").val();
    var spiders = [];
    $(".form-check-input:checked").each(function() {
        spiders.push($(this).val());
    });
    $.ajax({
        type: "POST",
        headers: {
            "X-CSRFToken": token
        },
        url: "{% url crypto_news_app:ajaxsaved %}",
        data: {
            day_of_week: day_of_week,
            hour: hour,
            minute: minute,
            spiders: spiders
        },

        success: function(data) {
            $("#error-list").html(
                '<p style="color:green">Form Successfully Submitted</p>'
            );
            console.log(data);
        },
        error: function(data) {},
    });
}