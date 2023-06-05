
let playing = false; // Флаг, указывающий, идет ли игра
let currentPlayer = 1; // Текущий игрок (1 - белые, 2 - черные)
let add_time = 5
const timerPanel = document.querySelector('.player'); // Панель таймера
const buttons = document.querySelectorAll('.bttn'); // Кнопки "Старт" и "Сброс"
// Sound effects for project.
// const timesUp = new Audio('audio/460133__eschwabe3__robot-affirmative.wav');
// const click = new Audio('audio/561660__mattruthsound.wav');

// document.getElementById('min1').innerHTML = 1;
// document.getElementById('sec1').innerHTML = 00;
// document.getElementById('min2').innerHTML = 1;
// document.getElementById('sec2').innerHTML = 00;
// Функция для добавления ведущего нуля к числу, если оно меньше 10
const padZero = (number) => {
    if (number < 10) {
        return '0' + number;
    }
    return number;
}


// Создание класса для таймера
class Timer {
    constructor(player, minutes) {
        this.player = player; // Идентификатор таймера игрока
        this.minutes = minutes; // Начальное количество минут
    }
    getMinutes(timeId) {
        return document.getElementById(timeId).textContent; // Получение количества минут из элемента с указанным идентификатором
    }
}

let p1time = new Timer('min1', document.getElementById('min1').textContent); // Таймер игрока 1
let p2time = new Timer('min2', document.getElementById('min2').textContent); // Таймер игрока 2


// Функция для смены игрока
const swapPlayer = () => {
    if (!playing) return; // Если игра не запущена, выходим из функции
    // Toggle the current player. 
     
    currentPlayer = currentPlayer === 1 ? 2 : 1; // Смена текущего игрока на противоположного
    // Play the click sound.
    // click.play();
}


// Функция для предупреждения игрока, если время становится менее 10 секунд
const timeWarning = (player, min, sec) => {
   // Изменение цвета чисел на красный при оставшемся времени менее 10 секунд
    if (min < 1 && sec <= 10) {
        if (player === 1) {
            document.querySelector('.player-1 .player__digits').style.color = '#CC0000'; // Изменение цвета чисел игрока 1
        } else {
            document.querySelector('.player-2 .player__digits').style.color = '#CC0000'; // Изменение цвета чисел игрока 2
        }
    }
}


// Функция для запуска таймера
const startTimer = () => {
    playing = true; // Установка флага игры в true
    let p1sec = 60; // Секунды для игрока 1
    let p2sec = 60; // Секунды для игрока 2

    let timerId = setInterval(function () {
        // Player 1.
        if (currentPlayer === 1) {
            if (playing) {
                // Disable start button.
                buttons[0].disabled = true; // Отключение кнопки "Старт"
                p1time.minutes = parseInt(p1time.getMinutes('min1'), 10); // Получение текущего количества минут для игрока 1
                if (p1sec === 60) {
                    p1time.minutes = p1time.minutes - 1; // Уменьшение количества минут для игрока 1 на 1, если секунды равны 60
                }
                p1sec = p1sec - 1; // Уменьшение количества секунд для игрока 1 на 1
                timeWarning(currentPlayer, p1time.minutes, p1sec); // Проверка предупреждения времени для игрока 1
                document.getElementById('sec1').textContent = padZero(p1sec); // Обновление секунд для игрока 1 на странице
                document.getElementById('min1').textContent = padZero(p1time.minutes); // Обновление минут для игрока 1 на странице
                if (p1sec === 0) {
                    // If minutes and seconds are zero stop timer with the clearInterval method.
                    if (p1sec === 0 && p1time.minutes === 0) {
                        // Play a sound effect.
                        // timesUp.play();
                        // Stop timer.
                        clearInterval(timerId); // Остановка таймера, если секунды и минуты равны 0
                        playing = false; // Установка флага игры в false
                    }
                    p1sec = 60; // Сброс секунд для игрока 1 на 60
                }
            }
        } else {
            // Player 2.
            if (playing) {
                p2time.minutes = parseInt(p2time.getMinutes('min2'), 10); // Получение текущего количества минут для игрока 2
                if (p2sec === 60) {
                    p2time.minutes = p2time.minutes - 1; // Уменьшение количества минут для игрока 2 на 1, если секунды равны 60
                }
                p2sec = p2sec - 1; // Уменьшение количества секунд для игрока 2 на 1
                timeWarning(currentPlayer, p2time.minutes, p2sec); // Проверка предупреждения времени для игрока 2
                document.getElementById('sec2').textContent = padZero(p2sec); // Обновление секунд для игрока 2 на странице
                document.getElementById('min2').textContent = padZero(p2time.minutes); // Обновление минут для игрока 2 на странице
                if (p2sec === 0) {
                    // If minutes and seconds are zero stop timer with the clearInterval method.
                    if (p2sec === 0 && p2time.minutes === 0) {
                        // Play a sound effect.
                        // timesUp.play();
                        // Stop timer.
                        clearInterval(timerId); // Остановка таймера, если секунды и минуты равны 0
                        playing = false; // Установка флага игры в false
                    }
                    p2sec = 60;
                }
            }
        }
    }, 1000);
}


// Слушатель события клика на панели таймера для смены игрока
timerPanel.addEventListener('click', swapPlayer)
   



// Цикл по кнопкам "Старт" и "Сброс"
for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', () => {
        if (buttons[i].textContent === 'START') {
            // Turn the button a gray color to signify a disabled button.
            buttons[i].style.color = '#EEEEEE'; // Изменение цвета кнопки "Старт" на серый
            buttons[i].style.backgroundColor = '#606060'; // Изменение цвета фона кнопки "Старт" на темно-серый
            startTimer(); // Запуск таймера
        } else {
            // Reset everything by reloading the page.
            location.reload(true); // Перезагрузка страницы для сброса всех значений
        }
    });
}

// Слушатель события нажатия клавиши пробела для смены игрока
document.addEventListener('keypress', event => {
    if (event.keyCode === 32 || event.which === 32) {
        swapPlayer();
    }
});
