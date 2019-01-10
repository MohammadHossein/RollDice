let turn = 1;

$(document).ready(function () {
    // $('#maxScore').hide();
    newGame();
    $('#rollDice').on('click', rollDice);
    $('#hold').on('click', hold);
});


function newGame() {
    for (let i = 1; i <= dice_count; i++) {
        $(`#dice${i}`).show()
    }
    let playerCard = $('.player');
    let currentScore = playerCard.find('.totalScoreNumber');
    let score = playerCard.find('.score');
    currentScore.html(0);
    score.html(0);
    let name1 = $('.player1').find('.playerName');
    name1.html('Player 1');
    name1.css('color', 'black');
    let name2 = $('.player2').find('.playerName');
    name2.html('Player 2');
    name2.css('color', 'black');

    turn = 1;

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

