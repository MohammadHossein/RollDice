let turn = 1;
let score6 = 0;
let maxScore = null;
let twoDice = true;
$(document).ready(function () {
    // $('#maxScore').hide();
    $('#newGame').on('click', newGame);
    newGame();
    $('#rollDice').on('click', rollDice);
    $('#hold').on('click', hold);
});


function newGame() {
    maxScore = null;
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
    while (maxScore == null) {
        maxScore = prompt('Enter max score of game!', "100");
        if (maxScore != null) {
            maxScore = parseInt(maxScore);
            if (isNaN(maxScore) || maxScore < 1)
                maxScore = null;
        }
    }
    $('#maxScore').html(`First person who earn ${maxScore} points, wins!`);

    twoDice = confirm('Play with 2 Dice or one?(Yes for 2 dice)');
    if (!twoDice) {
        $('#secondDice').hide()
    } else {
        $('#secondDice').show()
    }

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
    let random1 = randomDice();
    let random2 = randomDice();
    $('#dice1').attr('src', `/static/game/img/dice-${random1}.png`);
    if (twoDice) {
        $('#dice2').attr('src', `/static/game/img/dice-${random2}.png`);
        if (random1 === 6 && random2 === 6)
            score6 += 2;
        else if (random1 === 6)
            score6++;
        else if (random2 === 6)
            score6++;
        else
            score6 = 0
    } else {
        random2 = 0;
        if (random1 === 6)
            score6++
    }

    if (random1 === 1 || random2 === 1 || score6 >= 2) {
        score()
    } else {
        score(random1, random2)
    }
}

function score(num1, num2) {
    let score = $(`\.player${turn}`).find('.totalScoreNumber');
    if (num1 === undefined) {
        changeTrun();
        score.html(0);
        score6 = 0;
        return;
    }
    // alert(num1 + ' ' + num2);
    let value = parseInt(score.html()) + num1 + num2;
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

