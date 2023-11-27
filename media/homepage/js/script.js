 // function to set csrftoken
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

/*-------------- add/leave group ajax  ------------------ */
$('a.join').click(function(e) {
    const join_url = "/activities/join/";
    e.preventDefault();
    var slug = $(this).data('id');
    fetch(join_url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            "slug" : slug,
        })
    })
    .then(response => {
        return response.json() // convert response to json
    })
    .then(data => {
        // perform action with response data
        var previous_action = $(this).data('action');
        $(this).data('action', previous_action == 'join' ? 'leave':'join');
        if(data['action'] == 'join') {
            $(function() {
                Swal.fire('Group Joined');
            })
        }
        else if(data['action'] == 'leave') {
            $(function() {
                Swal.fire('Left Group');
            })
        }
        
    })
    .catch(error => {
        console.log("Error: " + error);
        $(function() {
            Swal.fire('Error Occured!');
        })
    })
});
$('.join-btn').click(function() {
    var join_html = '<i class="fa fa-user-plus"></i>';
    var leave_html = '<i class="fa fa-user-times"></i>';
    if($(this).parent('a.join').data('action') == 'join') {
        $(this).html(leave_html);
        $(this).removeClass('btn-success');
        $(this).addClass('btn-danger');
    }
    else {
        $(this).html(join_html);
        $(this).removeClass('btn-danger');
        $(this).addClass('btn-success');
    }
});

/* ------------------- view group quiz ajax function ---------------------------*/
$('a.group-quiz').click(function(e) {
    e.preventDefault();
    var loader = `<div class="loader"></div>`;
    $("#group-quiz-body").html(loader);
    var slug = $(this).data('id');
    const group_quiz_url = "/activities/" + slug + "/group-quiz/";
    fetch(group_quiz_url, {
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
        },
    }) 
    .then(response => {
        $("#group-quiz-body").html(`<p>No Quiz Found</p>`);
        return response.json() // convert response to json
        
    })
    .then(data => {
        // perform action with response data
        var head = `${slug} Quiz`;
        $("#group-quiz-header").html(head);
        $("#group-quiz-body").empty();
        if(data) {
            for (var key in data.quiz) {
                var temp = `<div class="group-quiz-item">
                    <span><b>${data.quiz[key].title}</b></span>
                    <span style="color:gray">${data.quiz[key].duration} mins</span>
                    <a href="/quizzes/${data.quiz[key].slug}/">
                        <button class="btn btn-success">Do Quiz</button>
                    </a>
                    <div>`;
                
                $("#group-quiz-body").append(temp);
            }
        }
        
    })
    .catch(error => {
    console.log("Error: " + error);
    $(function() {
        Swal.fire('Error Occured!');
    })
})
})

/* ----------------- show rankings -----------------------*/
const rank_quiz = $(".ranking");
$(rank_quiz).click(function() {
    var loader = `<div class="loader"></div>`;
    $("#quiz-rank-body").html(loader);
    var slug = $(this).data('id');
    const rank_url = "/activities/" + slug + "/quiz-rank/"
    fetch(rank_url, {
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
        },
    })
    .then(response => {
        $("#quiz-rank-body").html(`<p>No Score Found</p>`);
        return response.json() // convert response to json
    })
    .then(data => {
        var head = `${slug} Quiz Ranking`;
        $("#quiz-rank-header").html(head);
        $("#quiz-rank-body").empty();
        var num = 0;
        for (var key in data.scores) {
            num++;
            score = data.scores[key];
            var temp = `<div class="group-quiz-item">
                            <span>${num} <b><a href="/people/${score.name}/">${score.name}</a></b></span>
                            <span style="color:gray"><i class="fa fa-bar-chart" style="color:blue;"></i> ${score.score}%</span>
                            <span><i class="fa fa-star" style="color:gold;"></i> ${score.remark} Medal</span>
                    <div>`;
                
            $("#quiz-rank-body").append(temp);
            }
    })
    .catch(error => {
        console.log("Error: " + error);
        $(function() {
            Swal.fire('Error Occured!');
        })
    })
});


// Add the following code if you want the name of the file appear on select
    // file upload
    $(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });

/* ---------------------- Dashboard ----------------------------*/

// delete quiz ajax function
$('a.delete-quiz').click(function(e) {
    var del_url = "/activities/delete-quiz/";
            e.preventDefault();
            var slug = $(this).data('id');
            fetch(del_url, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    "slug" : slug,
                })
            })
            .then(response => {
                return response.json() // convert response to json
            })
            .then(data => {
                // perform action with response data
                var title = data['title'];
                $(this).parent().parent().parent().remove();
                $(function() {
                    Swal.fire(title + ' Quiz Deleted!');
                })
            })
});

// show submit add question form
$('.add-que-btn').click(function() {
    var title = $(this).data('id');
    $('.add-question-title').text("Question - " + title)
    $('#add-question-form').submit(function(e) {
        e.preventDefault();
        var add_question_url = "/activities/add-question/" + title + "/";
        const formData = new FormData();
        formData.append('order', $('#order').val());
        formData.append('question', $('#question').val());
        formData.append('option_a', $('#optiona').val());
        formData.append('option_b', $('#optionb').val());
        formData.append('option_c', $('#optionc').val());
        formData.append('option_d', $('#optiond').val());
        formData.append('answer', $('#answer').val());
        formData.append('question-image', $('.question-image')[0].files[0]);
        $('#question-add-submit').text('Submitting');
    
        fetch(add_question_url, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData,
        })
        .then(response => {
            return response.json() // convert response to json
        })
        .then(data => {
            if(data['order'] == 'undefined') {
                // perform action with response data
                $(function() {
                    Swal.fire('Question Number Already Exixts!');
                })
            }
            else {
                // perform action with response data
                $(function() {
                    Swal.fire('Question ' + data['order'] + ' Added!');
                })
                $(this).trigger('reset');
            }
            $('#question-add-submit').text('Submit');
        })
        .catch(error => {
            $(function() {
                Swal.fire('Error Occured!');
            })
        })
    });
})


// show add quiz to group form
$(".add-quiz-group").click(function() {
    var groupTitle = $(this).data('id');
    var head = `Add Quiz For <span>${groupTitle}</span>`;
    $('.add-group-quiz-title').html(head);
    // when form is submitted
    $('#add-group-quiz-form').submit(function(e) {
        e.preventDefault();
        // get form data
        title = $('#g-quiz-title').val();
        duration = $('#g-quiz-duration').val();
        const formData = new FormData();
        formData.append('group-title', groupTitle);
        formData.append('quiz-title', title);
        formData.append('duration', duration);

        const add_group_quiz_url = '/activities/add-group-quiz/';
        
        $('#group-quiz-add-submit').text('Submitting');
        fetch(add_group_quiz_url, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData,
        })
        .then(response => {
            return response.json() // convert response to json
        })
        .then(data => {
            // perform action with response data
            var quiz = data.quiz;
            $(this).trigger('reset');
            $('#group-quiz-add-submit').text('Submit');
            $(function() {
                Swal.fire('Quiz Added!');
            })
            var temp = `<div class="dash-item dash-quiz col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                            <div class="dash-des">
                                <h3>${quiz.title}</h3>
                                <div style="color:gray;font-size:15px;">
                                    <i class="fa fa-clock-o"></i> ${quiz.duration} mins&nbsp;&nbsp;&nbsp;
                                    <i class="fa fa-question"></i> ${quiz.questions} questions&nbsp;&nbsp;&nbsp;
                                    <i class="fa fa-group"></i> ${quiz.participants} participants
                                    
                                </div>
                                <div>
                                    <a href="/quizzes/${quiz.slug}/" title="View Quiz"><button class="btn btn-primary"><i class="fa fa-eye"></i></button></a>
                                    <button class="btn btn-info ranking" title="Quiz Rankings" data-toggle="modal" data-target="#quizRankModal" data-id="${quiz.slug}"><i class="fa fa-bar-chart"></i></button>
                                    <button class="btn btn-success add-que-btn" title="Add Questions" data-toggle="modal" data-target="#addQuestionModal" data-id="${quiz.slug}"><i class="fa fa-question"></i> <i class="fa fa-plus"></i></button>
                                    <a href="#" title="Delete Quiz" class="delete-quiz" data-id="${quiz.slug}"><button class="btn btn-danger"><i class="fa fa-trash"></i></button></a>
                                </div>
                            </div>
                        </div>`;
            $('.dash-quiz-con').append(temp);
        })
        .catch(error => {
            $(function() {
                Swal.fire('Error Occured!');
            })
        })
    })
});

/* ---------------------- People ----------------------------*/


function last_chat() {
    $('#chatBody').animate({
        scrollTop: $('.chat-con').offset().top + $('.chat-con')[0].scrollHeight
    }, 10);
    return false;
};

$('.chat-btn').click(function() {
    // get chats on opening
    var username = $(this).data('id');
    var head = `<span>Chat - ${username}</span>`;
    $('#chatTitle').html(head)
    var loader = `<div class="loader"></div>`;
    $(".chat-con").html(loader);
    
    const chat_url = "/activities/get-chats/" + username + "/";
    
    // send chats
    $('#send-chat-form').submit(function(e) {
        e.preventDefault();
        const send_chat_url = "/activities/send-chat/" + username + "/";
        const formData = new FormData();
        formData.append('message', $('#message').val());
        $('send-chat-submit').prop('disabled', true);
        fetch(send_chat_url, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        })
        .then(response => {
        return response.json() // convert response to json
        })
        .then(data => {
            // perform action with response data
            $('#message').val('');
            $('send-chat-submit').prop('disabled', true);
        })
        .catch(error => {
            $(function() {
                Swal.fire('Error while sending message!');
            })
        }) 
    });
    $('#emoji-btn').click(function(e) {
        e.preventDefault();
        $('.dd-content').toggleClass('show');
    })
    chatInterval = setInterval(show_messages, 500, chat_url);
    //last_chat();
});
$('.close-chat').click(function() {
    location.reload();
})

$('.view-profile-btn').click(function() {
    var username = $(this).data('id');
    viewProfile(username);
})
function viewProfile(username) {
    $('#profileTitle').text(username + "'s Profile")
    var loader = `<div class="loader"></div>`;
    $("#profileBody").html(loader);
    const view_profile_url = "/people/" + username + "/";
    fetch(view_profile_url, {
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
        },
    })
    .then(response => {
        return response.json() // convert response to json
    })
    .then(data => {
        // perform action with response data
        profile = data.profile;
        quiz = data.quiz;
        groups = data.groups;
        scores = data.scores;
        s_quiz = data.s_quiz;
        g_image = data.g_image;
        $("#profileBody").empty();
        var temp = `<div class="wrapper" style="width:100%;">
                        <input type="radio" name="slider" checked id="pro">
                        <input type="radio" name="slider" id="group">
                        <input type="radio" name="slider" id="quiz">
                        <input type="radio" name="slider" id="score">
                        <div class="tabs">
                            <label for="pro" class="pro"><i class="fa fa-user"></i><span>Profile</span></label>
                            <label for="group" class="group"><i class="fa fa-group"></i><span>Groups</span></label>
                            <label for="quiz" class="quiz"><i class="fa fa-book"></i><span>Quiz</span></label>
                            <label for="score" class="score"><i class="fa fa-bar-chart"></i><span>Scores</span></label>
                            <div class="slider"></div>
                        </div>

                        <section>
                            <div class="content content-1">
                                <!-- Profile Section -->
                                <div class="dash-item" style="width:100%;">
                                    <img id="dp" src="${profile.dp}" alt="" />
                                    <div class="dash-des" id="des">
                                        <h3 style="font-size:25px;font-weight:600">${profile.username}</h3>
                                        <h3 style="font-size:22px;font-weight:400">${profile.lname} ${profile.fname}</h3>
                                        <span style="font-size:15px;">${profile.about}</span>
                                        <div style="color:gray;font-size:15px;">
                                            <i class="fa fa-university"></i> ${profile.school}&nbsp;&nbsp;&nbsp;
                                            <i class="fa fa-book"></i> ${profile.course}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row content content-2"></div>
                            <div class="row content content-3"></div>
                            <div class="row content content-4"></div>
                        </section>
                    
                    </div>`;
        $("#profileBody").append(temp);
        if(groups) {
            for (var key in groups) {
                var g_temp = `<div class="dash-item" style="width:100%">
                                <img src="${g_image[key]}" alt="" />
                                <div class="dash-des">
                                    <h3 style="font-weight:600;font-size:20px;">${groups[key].title}</h3>
                                    <span style="font-size:15px;">${groups[key].description}</span>
                                    <div style="color:gray;font-size:15px;">
                                        <i class="fa fa-globe"></i> ${groups[key].type}
                                    </div>
                                </div>
                                <div style="width:100%;margin-top:5px;">
                                    <a href="/groups/${groups[key].slug}/" title="View Group"><button class="btn btn-info"><i class="fa fa-eye"></i> View</button></a>
                                    <a href="#" title="Group Quiz" class="group-quiz" data-id="${groups[key].slug}" data-toggle="modal" data-target="#groupQuizModal">
                                        <button class="btn btn-primary"><i class="fa fa-book"></i> Quiz</button>
                                    </a>
                                </div>
                            </div>`;

                $(".content-2").append(g_temp);
            }
        }
        if(quiz) {
            for (var key in quiz) {
                var q_temp = `<div class="dash-item" style="width:100%">
                                <div class="dash-des">
                                    <h3 style="font-weight:600;font-size:20px;">${quiz[key].title}</h3>
                                    <div style="color:gray;font-size:15px;">
                                        <i class="fa fa-clock-o"></i> ${quiz[key].duration} mins&nbsp;&nbsp;&nbsp;
                                    </div>
                                    <div>
                                        <a href="/quizzes/${quiz[key].slug}/"><button class="btn btn-primary"><i class="fa fa-book"></i> Do Quiz</button></a>
                                        <button class="btn btn-info ranking" data-toggle="modal" data-target="#quizRankModal" data-id="${quiz[key].slug}"><i class="fa fa-bar-chart"></i> Scores</button>
                                    </div>
                                </div>
                            </div>`;

                $(".content-3").append(q_temp);
            }
        }
        if(scores) {
            for (var key in scores) {
                var s_temp = `<div class="dash-item" style="width:100%">
                                <div class="dash-des">
                                    <h3 style="font-weight:600;font-size:20px;">${s_quiz[key]}</h3>
                                    <div style="color:gray;font-size:15px;">
                                        <i class="fa fa-bar-chart" style="color:rgb(82, 82, 250);"></i> <span>Score:</span> ${scores[key].score}%&nbsp;&nbsp;&nbsp;
                                        <i class="fa fa-star" style="color:rgb(253, 167, 6);"></i> <span>Medal:</span> ${scores[key].remark}
                                    </div>
                                </div>
                            </div>`;

                $(".content-4").append(s_temp);
            }
        }
    })
    .catch(error => {
        console.log("Error: " + error);
        $(function() {
            Swal.fire('Error occured while fetching profile!');
        })
    })
};


/* ---------------------- Groups ----------------------------*/
// submit add group form
$('#add-group-form').submit(function(e) {
    var add_group_url = "/activities/add-group/";
    e.preventDefault();
    const formData = new FormData();
    formData.append('group-title', $('#group-title').val());
    formData.append('group-description', $('#group-description').val());
    formData.append('group-type', $('#group-type').val());
    formData.append('group-image', $('.group-image')[0].files[0]);
    $('#group-add-submit').text('Submitting');

    fetch(add_group_url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData,
    })
    .then(response => {
        return response.json() // convert response to json
    })
    .then(data => {
        // perform action with response data
        var group = data.group;
        $(this).trigger('reset');
        $('#group-add-submit').text('Submit');
        $(function() {
            Swal.fire('Group Added!');
        })
        var temp = `<div class="dash-item col-12 col-sm-12 col-md-6 col-lg-6 col-xl-4">
                        <img src="${group.image}" alt="" />
                        <div class="dash-des">
                            <h3>${group.title}</h3>
                            <span style="font-size:15px;">${group.des}</span>
                            <div style="color:gray;font-size:15px;">
                                <i class="fa fa-globe"></i> ${group.type}&nbsp;&nbsp;&nbsp;
                                <i class="fa fa-group"></i> <span class="mem-count">1</span> member&nbsp;&nbsp;&nbsp;
                                <i class="fa fa-book"></i> 0 quiz&nbsp;&nbsp;&nbsp;
                                <i class="fa fa-user"></i> Admin
                            </div>
                        </div>
                        <div style="width:100%;margin-top:5px;">
                            <a href="/groups/${group.slug}/" title="View Group"><button class="btn btn-info"><i class="fa fa-eye"></i></button></a>
                            <a href="#" title="Group Quiz" class="group-quiz" data-id="${group.slug}" data-toggle="modal" data-target="#groupQuizModal">
                                <button class="btn btn-primary"><i class="fa fa-book"></i> <i class="fa fa-question"></i></button>
                            </a>
                            <a href="#" class="join" data-id="${group.slug}" data-action="leave">
                                <button class="btn btn-danger join-btn" title="Leave group">
                                    <i class="fa fa-user-times"></i>
                                </button>
                            </a>
                            
                        </div>
                    </div>`;
        $('.dash-group').append(temp);
    })
    .catch(error => {
        $(function() {
            Swal.fire('Error Occured!');
        })
    })
});


/* ---------------------- Quiz ----------------------------*/
// submit add quiz form
$('#add-quiz-form').submit(function(e) {
    var add_quiz_url = "/activities/add-quiz/";
    e.preventDefault();
    title = $('#quiz-title').val();
    duration = $('#quiz-duration').val();
    $('#quiz-add-submit').text('Submitting');
    
    fetch(add_quiz_url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', // necessary to work with .is_ajax verification
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            'title': title,
            'duration': duration,
        }),
    })
    .then(response => {
        return response.json() // convert response to json
    })
    .then(data => {
        // perform action with response data
        var quiz = data.quiz;
        $(this).trigger('reset');
        $('#quiz-add-submit').text('Submit');
        $(function() {
            Swal.fire('Quiz Added!');
        })
        var temp = `<div class="dash-item col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                        <div class="dash-des">
                            <h3>${quiz.title}</h3>
                            <div style="color:gray;font-size:15px;">
                                <i class="fa fa-clock-o"></i> ${quiz.duration} mins&nbsp;&nbsp;&nbsp;
                                <i class="fa fa-question"></i> ${quiz.questions} questions&nbsp;&nbsp;&nbsp;
                                <i class="fa fa-group"></i> ${quiz.participants} participants
                                
                            </div>
                            <div>
                                <a href="/quizzes/${quiz.slug}/"><button class="btn btn-primary"><i class="fa fa-book"></i> Do Quiz</button></a>
                                <button class="btn btn-info ranking" data-toggle="modal" data-target="#quizRankModal" data-id="${quiz.slug}"><i class="fa fa-bar-chart"></i> Scores</button>
                            </div>
                        </div>
                    </div>`;
        $('.dash-quiz').append(temp);
    })
    .catch(error => {
        $(function() {
            Swal.fire('Error Occured!');
        })
    })
});
