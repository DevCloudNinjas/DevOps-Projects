import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Game from './components/Game';
import {createTetris} from "./tetris/Tetris";

const tetris = createTetris();
tetris.start();
document.addEventListener("keydown", (event) => {
    const keyName = event.key;
    if (tetris.isRunning()) {
        if (keyName === "ArrowUp") {
            tetris.rotateCurrentPiece();
        } else if (keyName === "ArrowDown") {
            tetris.tick();
        }
        else if (keyName === "ArrowLeft") {
            tetris.moveLeft();
        } else if (keyName === "ArrowRight") {
            tetris.moveRight();
        } else if (keyName === " ") {
            tetris.pause();
        }
    } else {
        if(keyName === " ") {
            if (tetris.isPaused()) {
                tetris.resume();
            } else {
                tetris.start();
            }
        }
    }
});
ReactDOM.render(
    <React.StrictMode>
        <Game tetris={tetris}/>
    </React.StrictMode>,
    document.getElementById('root')
);
