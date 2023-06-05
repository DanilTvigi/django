import { Chess } from './chess.js';

const board = document.querySelector('chess-board');
const game = new Chess();
let moves = ['f2f4','e7e6', 'g1f3','f8b4', 'h1g1', 'a7a5'];
let i = 0;

document.querySelector('#btn-back').onclick = function(){
    if(i>0){
        i = i - 1;
        let history_move = game.history();
        game.load('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
        for(let j = 0; j < history_move.length - 1; j++){
            game.move(history_move[j]);
        }
        board.setPosition(game.fen());
    }
}
document.querySelector('#btn-next').onclick = function(){
    game.move(moves[i]);
    board.setPosition(game.fen());
    i = i + 1;
}

// let letter = moves[i].split('');
// let a = letter[2]+letter[3]+letter[0]+letter[1];
// console.log(a);