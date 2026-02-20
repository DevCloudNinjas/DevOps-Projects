import {createState} from "./State.js";


const createTetris = ({height, width} = {height: 20, width:10}) => {
    const _height = height;
    const _width = width;
    const state = createState(_height, _width);
    let timer = null;
    const stateChangeListeners = [];

    state.onLevelChange((level) => startTimer(timer, calculateSpeedForCurrentLevel(level)))

    const startTimer = (timer, delay) => {
        if (timer != null) {
            clearInterval(timer);
        }

        const newTimer = setInterval(tick, delay)
        return newTimer;
    };

    const stopTimer = (timer) => {
        if (timer != null) {
            clearInterval(timer);
        }
    };

    const calculateSpeedForCurrentLevel = (level) => {
        return Math.floor(900 * (Math.pow(0.9, level - 1)));
    };


    //eslint-disable-next-line no-unused-vars
    const toString = () => {
        let str = state.visibleMatrix().map(row => {
            return row.map(tetromino => {
                if (tetromino.isFilled()) {
                    return tetromino.color;
                } else {
                    return tetromino.state;
                }
            }).join(",");
        }).join("\n");

        return str;
    };

    const tick = () => {
        if (!state.isRunning()) {
            return;
        }

        state.moveCurrentPieceDown();
        if(state.isGameOver()){
            stopTimer(timer);
        }
        notifyOnStateChangeListeners();
    };

    const notifyOnStateChangeListeners = () => {
        stateChangeListeners.forEach(fn => fn({...state}));
    };

    const resume = () => {
        state.resume();
        notifyOnStateChangeListeners();
        timer = startTimer(timer, calculateSpeedForCurrentLevel(state.level()));

    };

    const start = () => {
        if (state.isStarted()) {
            return;
        }
        state.start();
        notifyOnStateChangeListeners();
        timer = startTimer(timer, calculateSpeedForCurrentLevel(state.level()));
    };

    const pause = () => {
        if (state.isPaused()) {
            return;
        }
        if (timer != null) {
            clearInterval(timer);
        }
        state.pause();
        stopTimer(timer);
        notifyOnStateChangeListeners();
    };

    const isPaused = () => {
        return state.isPaused();
    }

    const moveLeft = () => {
        state.moveLeft();
        notifyOnStateChangeListeners();
    };

    const moveRight = () => {
        state.moveRight();
        notifyOnStateChangeListeners();
    }

    const rotateCurrentPiece = () => {
        state.rotateCurrentPiece();
        notifyOnStateChangeListeners();
    }



    return {
        onStateChange(fn) {
            stateChangeListeners.push(fn);
        },
    
        isGameOver()  {
            return state.gameOver;
        },
    
        isRunning() {
            return state.isRunning();
        },
    
        isStarted() {
            return state.isStarted();
        },
        state,
        rotateCurrentPiece,
        moveLeft,
        moveRight,
        start,
        pause,
        isPaused,
        resume,
        tick,
        height: _height,
        width: _width
    };

};

export {createTetris}
