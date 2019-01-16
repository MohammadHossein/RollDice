let turn = 1;
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

function randomDice() {
    return Math.floor((Math.random() * 6) + 1);
}

function changeTrun() {
    $('.playerCard').toggleClass('itsTurn');
    $('.turn').find('i').toggleClass('hide-dot');
    turn = turn === 1 ? 2 : 1;
}

function rollDice() {
    let change_turn = false;
    let current = 0;
    for (let i = 1; i <= dice_count; i++) {
        let random = randomDice();
        $(`#dice${i}`).attr('src', `/static/game/img/dice-${random}.png`);
        current += random;
        if (hold_number.includes(random)) {
            change_turn = true;
        }
    }
    if (change_turn) {
        score()
    } else {
        score(current)
    }
}

function score(num1) {
    let score = $(`\.player${turn}`).find('.totalScoreNumber');
    if (num1 === undefined) {
        changeTrun();
        score.html(0);
        return;
    }
    // alert(num1 + ' ' + num2);
    let value = parseInt(score.html()) + num1;
    score.html(value.toString())
}

function hold() {
    let playerCard = $(`\.player${turn}`);
    let currentScore = playerCard.find('.totalScoreNumber');
    let score = playerCard.find('.score');
    let value = parseInt(score.html()) + parseInt(currentScore.html());
    score.html(value);
    currentScore.html(0);

    if (value > maxScore) {
        $('#rollDice').off('click');
        $('#hold').off('click');
        let name = $(`.player${turn}`).find('.playerName');
        name.html('Winner!');
        name.css('color', 'red');
        return;
    }
    changeTrun();
}


function showData(data) {
    if (data.winner !== null) {
        let winner = data.winner ? 1 : 2;
        $('#rollDice').off('click');
        $('#hold').off('click');
        let name = $(`.player${winner}`).find('.playerName');
        name.html('Winner!');
        name.css('color', 'red');
        return;
    }
    // console.log(data);
    if (data.dices.length > 0)
        for (let i = 1; i <= data.dice_count; i++) {
            let number = data.dices[i - 1];
            $(`#dice${i}`).attr('src', `/static/game/img/dice-${number}.png`);
        }

    if ((data.turn && turn === 2) || ((!data.turn) && turn === 1)) {
        changeTrun();
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

function interval() {
    update();
    setTimeout(interval, 1000);
}