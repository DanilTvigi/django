import { Chess } from './chess.js';

const board = document.querySelector('chess-board');
const game = new Chess();

var mylist = document.getElementById("list").innerHTML;
mylist = mylist.split(',');
let steps = [];
for (let item of mylist) {
    // Удаляем ненужные символы из каждого элемента списка
    let cleanedItem = item.replace(/[\(\)']+/g, '');
      
    // Разделяем элемент по запятой и удаляем пробелы
    let moves = cleanedItem.split(',').map(move => move.trim());
      
    // Добавляем элементы в выходной список
    steps = steps.concat(moves);
}
// let moves = ['d7d5', 'e2e4', 'c8f5', 'e4f5', ''];
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
    game.move(steps[i]);
    board.setPosition(game.fen());
    i = i + 1;
}

// let letter = moves[i].split('');
// let a = letter[2]+letter[3]+letter[0]+letter[1];
// console.log(a);