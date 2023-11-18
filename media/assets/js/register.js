function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // does the cookie has the same name as the one we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function() {
        
    var slider = $('.slide-page');
    var base_url = ``;
    // next buttons
    $('.firstNext').click(function(e) {
        e.preventDefault();
        if($('#first-name').val().trim() == '' || $('#last-name').val().trim() == '') {
            swal('Warning', 'field cannot be empty', 'warning');
            return
        }
        slider.css('margin-left', '-25%');
    })
    $(".next-1").click(function(e) {
        e.preventDefault();
        var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        var telRegex = /^\d{11}$/;;
        if(!emailRegex.test($('#email').val())) {
            swal('Warning', 'Invalid email', 'warning');
            return
        }
        if(!telRegex.test($('#phone-number').val())) {
            swal('Warning', 'Invalid phone number', 'warning');
            return
        }
        slider.css('margin-left', '-50%');
    })
    $(".next-2").click(function(e) {
        e.preventDefault();
        slider.css('margin-left', '-75%');
    })
    // prev buttons
    $(".prev-1").click(function(e) {
        e.preventDefault();
        slider.css('margin-left', '0%');
    })
    $(".prev-2").click(function(e) {
        e.preventDefault();
        slider.css('margin-left', '-25%');
    })
    $(".prev-3").click(function(e) {
        e.preventDefault();
        slider.css('margin-left', '-50%');
    })

    
})


var password = document.querySelector('#password');
var cpassword = document.querySelector('#cpassword');
var pass = document.querySelector('#pass');
var cpass = document.querySelector('#cpass');
pass.onclick = function() {
    if(password.type == "password") {
        password.type = "text";
    }
    else {
        password.type = "password";
    }
}
cpass.onclick = function() {
    if(cpassword.type == "password") {
        cpassword.type = "text";
    }
    else {
        cpassword.type = "password";
    }
}