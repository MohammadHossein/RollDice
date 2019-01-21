let turn = 1;
let waiting = 0;
let started = false;
let user_rating = 0;
let game_rating = 0;
let opponent_user_id = 0;
let db_game_id = 0;
let winner = null;
$(document).ready(function () {
    // $('#maxScore').hide();
    newGame();
    update();
    $('#rollDice').on('click', function () {
        update('roll-dice')
    });
    $('#hold').on('click', function () {
        update('hold')
    });
    interval();
    const urlParams = new URLSearchParams(window.location.search);
    db_game_id = urlParams.get('id');
    $('#rating-user').stars({
        stars: 5,
        click: function (i) {
            user_rating = i;
        }

    });
    $('#rating-game').stars({
        stars: 5,
        click: function (i) {
            game_rating = i;
        }
    });

    $('#game-comment-button').on('click', sendGameComment);
    $('#user-comment-button').on('click', sendUserComment);

});


function newGame() {
    for (let i = 1; i <= dice_count; i++) {
        $(`#dice${i}`).show()
    }
    let name1 = $('.player1').find('.playerName');
    name1.html('Player 1');
    name1.css('color', 'black');
    let name2 = $('.player2').find('.playerName');
    name2.html('Player 2');
    name2.css('color', 'black');
}


function changeTurn() {
    $('.playerCard').toggleClass('itsTurn');
    $('.turn').find('i').toggleClass('hide-dot');
    turn = turn === 1 ? 2 : 1;
}



function showData(data) {
    started = data.started;
    if (myUserID === data.player1_id) {
        opponent_user_id = data.player2_id;
    } else {
        opponent_user_id = data.player1_id;
    }
    if (data.winner !== null) {
        winner = data.winner ? 1 : 2;
        $('#rollDice').off('click');
        $('#hold').off('click');
        let name = $(`.player${winner}`).find('.playerName');
        name.html('Winner!');
        name.css('color', 'red');
        $('#game-comment-modal').modal({backdrop: 'static', keyboard: false});
        return;
    }
    // console.log(data);
    if (data.dices.length > 0)
        for (let i = 1; i <= data.dice_count; i++) {
            let number = data.dices[i - 1];
            $(`#dice${i}`).attr('src', `/static/game/img/dice-${number}.png`);
        }

    if ((data.turn && turn === 2) || ((!data.turn) && turn === 1)) {
        changeTurn();
    }
    $('#max-score').val(data.max_score);
    let player1 = $('.player1');
    player1.find('.score').html(data.player1_total);
    player1.find('.totalScoreNumber').html(data.player1_current);
    let player2 = $('.player2');
    player2.find('.score').html(data.player2_total);
    player2.find('.totalScoreNumber').html(data.player2_current);
    if (myTurn !== turn) {
        $('#player-turn').show();
        $('#game-button').hide();
    } else {
        $('#player-turn').hide();
        $('#game-button').show();
    }
}

function update(action) {
    $.ajax({
        url: '/game/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            game_id: game_id,
            action: action ? action : " "
        }),
        success: function (data) {
            showData(JSON.parse(data));
        }
    })
}

function showTimeout() {
    $.ajax({
        url: '/end_game?id=' + game_id,
        type: 'GET',
        success: function (e) {
            $('#timeout-modal').modal({backdrop: 'static', keyboard: false})
        },
        error: function (e) {
            waiting = 0;
            setTimeout(interval, 1000);
        }
    });
}

function interval() {
    update();
    waiting++;
    if ((!started) && waiting > 120) {
        showTimeout();
        return;
    }
    if (winner === null)
        setTimeout(interval, 1000);
}

function sendGameComment() {
    $.ajax({
        url: '/game_comment',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            text: $('#game-comment-input').val(),
            rate: game_rating,
            game: db_game_id,
            user: myUserID
        })
    });
    $('#game-comment-modal').modal('hide');
    $('#user-comment-modal').modal({backdrop: 'static', keyboard: false});
}

function sendUserComment() {
    $.ajax({
        url: '/user_comment',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            text: $('#user-comment-input').val(),
            rate: user_rating,
            game: db_game_id,
            user: myUserID,
            to_user: opponent_user_id
        }),
        success: function () {
            window.location.replace('/');
        }
    });
}