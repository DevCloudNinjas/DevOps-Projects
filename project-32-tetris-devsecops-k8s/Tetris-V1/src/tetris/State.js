import {Tetromino, TetrominoStates} from "./Tetromino";
import {randomPiece} from "./Piece";

const MAX_ROW_CLEAR_PER_LEVEL = 10;

const createState = (height, width) => {
    let _height = height;
    let _width = width;
    let paused =  false;
    let started = false;
    let gameOver = false;
    let _level =  1;
    let _score = 0;
    let _nextPiece = null;
    let _currentPiece = null;
    let totalNumberOfClearedRows = 0;
    let onLevelChangeAction = null;

    const isRunning = () => {
        return started && !paused;
    };

    const isStarted = () => {
        return started;
    };

    const isGameOver = () => {
        return gameOver;
    };

    const isPaused = () => {
        return paused;
    };

    const initMatrix = (height, width) => {
        let _matrix = [];
        for (let i = 0; i < height; i++) {
            _matrix[i] = [];
            for (let j = 0; j < width; j++) {
                _matrix[i][j] = Tetromino();
            }
        }
        return _matrix;
    };

    let matrix = initMatrix(height, width);
    let _visibleMatrix = [...matrix];


    const start = () => {
        paused = false;
        started = true;
        gameOver = false;
        _level = 1;
        _score = 0;
        matrix = initMatrix(_height, _width);
        sendNextPiece();
        _visibleMatrix = createVisibleMatrix(matrix);
    };

    const pause = () => {
        paused = true;
    }

    const resume = () => {
        paused = false;
    }

    const sendNextPiece = () => {
        if(_nextPiece == null){
            _nextPiece = randomPiece();
        }
        _currentPiece = _nextPiece;
        _nextPiece = randomPiece();
        _currentPiece  = _currentPiece.moveInitCenter(width);
    }

    const isFilled = (coordinate) => {
        return matrix[coordinate.y][coordinate.x].isFilled();
    };

    const increaseLevel = () => {
        if (totalNumberOfClearedRows > MAX_ROW_CLEAR_PER_LEVEL) {
            _level++;
            totalNumberOfClearedRows = 0;
            notifyLevelChangeListener(_level);
        }
    }

    const moveCurrentPieceDown = () => {
        if(_currentPiece == null){
            return;
        }

        if(overlaps(_currentPiece)){
            setGameOver();
            return;
        }
        const newPosition = _currentPiece.moveDown({isFilled, height});
        //piece cannot move down.
        //merge piece into matrix and start a new piece.
        if(newPosition.isOnSamePosition(_currentPiece)){
            mergePieceIntoMatrix(newPosition);
            sendNextPiece();
        } else {
            _currentPiece = newPosition;
        }
        const numberOfClearedRows = clearRows();
        totalNumberOfClearedRows+=numberOfClearedRows;
        increaseLevel();
        _score = calculateScore(_score, numberOfClearedRows, _level);
        _visibleMatrix = createVisibleMatrix(matrix);
    };

    const calculateScore = (_score, numberOfClearedRows, _level) => {
        return _score + Math.pow(numberOfClearedRows, 2) * _level
    }

    const createVisibleMatrix = (matrix) => {
        const visibleMatrix = matrix.map(row => row.slice());
        if(_currentPiece != null){
            _currentPiece.matrixCoordinates().forEach(coordinate => {
                const tetromino = Tetromino(TetrominoStates.FILLED, _currentPiece.color);
                visibleMatrix[coordinate.y][coordinate.x] = tetromino;
            })
        }
        return visibleMatrix;
    };

    const overlaps = (piece) => {
        const overlap = piece.matrixCoordinates().some(coordinate => {
            return matrix[coordinate.y][coordinate.x].isFilled()
        });

        return overlap;
    };

    const setGameOver = () => {
      started = false;
      paused = false;
      gameOver = true;
    };

    const mergePieceIntoMatrix = (piece) => {
        piece.matrixCoordinates().forEach( coordinate => {
            matrix[coordinate.y][coordinate.x] = Tetromino(TetrominoStates.FILLED, piece.color)
        });
    };

    const rotateCurrentPiece = () => {
        move(() => _currentPiece.rotate({width: _width}));
    }

    const moveLeft = () => {
        move(() => _currentPiece.moveLeft());
    }

    const moveRight = () => {
        move(() => _currentPiece.moveRight({width: _width}));
    }

    const move = (action) => {
        if(_currentPiece == null){
            return;
        }
        let nextPosition = action();
        if(nextPosition != null && !overlaps(nextPosition)){
            _currentPiece = nextPosition;
            _visibleMatrix = createVisibleMatrix(matrix);
        }
    }

    const clearRows = () => {
        let numberOfClearedRows = 0;
        for(let i = height - 1; i >= 0 ; ){
            const allEmpty = matrix[i].every(cell => cell.isEmpty());
            if(allEmpty){
                break;
            }

            const allFilled = matrix[i].every(cell => cell.isFilled());
            if(allFilled){
                matrix.splice(i, 1);
                const emtyRow = [];
                for(let j = 0; j < width; j++){
                    emtyRow.push(Tetromino());
                }
                matrix.unshift(emtyRow);
                numberOfClearedRows++;
            } else {
                i--;
            }
        }
        return numberOfClearedRows;
    };

    const visibleMatrix = () => {
      return _visibleMatrix;
    }

    const score = () => {
        return _score;
    };

    const level = () => {
        return _level;
    };

    const nextPiece = () => {
        return _nextPiece;
    };

    const onLevelChange = (action) => {
        onLevelChangeAction = action;
    };

    const notifyLevelChangeListener = (level) => {
        if(onLevelChangeAction){
            onLevelChangeAction(level);
        }
    };

    return {
        isRunning,
        isStarted,
        isPaused,
        start,
        pause,
        resume,
        level,
        score,
        isFilled,
        isGameOver,
        moveCurrentPieceDown,
        visibleMatrix,
        rotateCurrentPiece,
        moveLeft,
        moveRight,
        nextPiece,
        onLevelChange
    };
};

export {createState};
