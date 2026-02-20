import {Tetromino, TetrominoStates} from "./Tetromino";
import {randomColor} from "./Colors";

const Piece = ({x = 0, y = 0, color = randomColor(), state}) => {
    const FILLED = 1;
    let _x = x;
    let _y = y;
    let _color = color;
    let _state = state;
    let width = _state[0].length;
    let height = _state.length;
    const rotate = (matrixState) => {
        let newState = [];
        for(let i = 0; i < width; i ++){
            newState.push([]);
            for(let j = 0; j < height; j ++){
                newState[i].push(_state[height - j - 1][i]);
            }
        }

        const nextPieceState = Piece({x: _x, y: _y, color: _color, state: newState});
        const leftMost = Math.min(...nextPieceState.matrixCoordinates().map(coordinate => coordinate.x));
        let rightMost = Math.max(...nextPieceState.matrixCoordinates().map(coordinate => coordinate.x));

        let newX = _x;
        let newY = _y;

        if(leftMost < 0){
            newX  = _x + Math.abs(leftMost);
        }

        if(rightMost >= matrixState.width - 1){
            newX = _x - (rightMost - (matrixState.width - 1));
        }

        return Piece({x: newX, y: newY, color: _color, state: newState});

    };

    const move = (x, y) => {
        return Piece(x, y, _color, _state);
    };

    const moveInitCenter = (matrixWidth) => {
        const x = Math.floor((matrixWidth - width) / 2);
        const upMostPoint = Math.min(...matrixCoordinates().map(coordinate => coordinate.y));
        const y = 0 - upMostPoint;
        return Piece({x: x, y: y, color: _color, state: _state})
    }

    const moveLeft = () => {
        let newX = _x - 1;
        let newY = _y;

        const leftMost = Math.min(...matrixCoordinates().map(coordinate => coordinate.x));
        //if piece out of matrix after rotation, auto align coordinates.
        if(leftMost <= 0){
            newX = _x;
        }

        return Piece({x: newX, y: newY, color: _color, state:_state});
    };

    const moveRight = (matrixState) => {
        let newX = _x + 1;
        let newY = _y;

        let rightMost = Math.max(...matrixCoordinates().map(coordinate => coordinate.x));
        if(rightMost >= matrixState.width - 1){
            newX = _x;
        }
        return Piece({x: newX, y: newY, color: _color, state:_state});
    };

    const matrixCoordinates = () => {
        const coordinates = [];
        for(let i = 0; i < height; i ++){
            for(let j = 0; j < width; j++){
                if(_state[i][j] === FILLED){
                    const x = j + _x;
                    const y = i + _y;
                    //if piece is rotated at initial position (especially for I piece),
                    // some cells can go to out of matrix
                    if(x < 0 || y < 0){
                        continue;
                    }
                    coordinates.push({x: x, y: y});
                }
            }
        }
        return coordinates;
    };

    const moveDown = (gameState) => {
        const newY = _y + 1;
        const piece = Piece({x: _x, y: newY, color, state});
        const matrixCoordinates = piece.matrixCoordinates();
        const canMoveDown = matrixCoordinates.every(coordinate => {
            const canMove = (coordinate.y < gameState.height) && !gameState.isFilled(coordinate);
            return canMove;
        });

        if(canMoveDown){
            return piece;
        } else {
            const samePiece  = Piece({x: _x, y: _y, color, state});
            return samePiece;
        }
    };

    const isOnSamePosition = (piece) =>{
        return _x === piece.x && _y === piece.y;
    };

    const toTetrominos = (state, color) => {
        const tetrominos = [];
        for(let i = 0; i < state.length; i ++){
            const row = [];
            for(let j = 0; j < state[0].length; j ++){
                let tetromino = Tetromino();
                if(state[i][j] === FILLED){
                  tetromino = Tetromino(TetrominoStates.FILLED, color);
                }
                row.push(tetromino);
            }
            tetrominos.push(row);
        }
        return tetrominos;
    };

    const tetrominos = () => {
        return toTetrominos(_state, _color);
    };

    return {
        rotate,
        move,
        moveLeft,
        moveRight,
        moveDown,
        x: _x,
        y: _y,
        isOnSamePosition,
        matrixCoordinates,
        color: _color,
        tetrominos,
        moveInitCenter
    };
}

const I_Piece = () => {
    let initalState =  [
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
    ];

    const piece = Piece({state: initalState});
    return piece;
}

const O_Piece = () => {
    let initalState =  [
        [1,1],
        [1,1],

    ];

    const piece = Piece({state: initalState});
    return piece;
}

const Z_Piece = () => {
    let initalState =  [
        [1,1,0],
        [0,1,1],
        [0,0,0]
    ];

    const piece = Piece({state: initalState});
    return piece;
}

const S_Piece = () => {
    let initalState =  [
        [0,1,1],
        [1,1,0],
        [0,0,0]
    ];

    const piece = Piece({state: initalState});
    return piece;
}

const J_Piece = () => {
    let initalState =  [
        [1,0,0],
        [1,1,1],
        [0,0,0],

    ];

    const piece = Piece({state: initalState});
    return piece;
}

const L_Piece = () => {
    let initalState =  [
        [0,0,1],
        [1,1,1],
        [0,0,0],

    ];

    const piece = Piece({state: initalState});
    return piece;
}

const M_Piece = () => {
    let initalState =  [
        [1,1,1],
        [0,1,0],
        [0,0,0],

    ];

    const piece = Piece({state: initalState});
    return piece;
}

const X_Piece = () => {
    let initalState =  [
        [1,0,1],
        [0,1,0],
        [1,0,1],

    ];

    const piece = Piece({state: initalState});
    return piece;
}


const empty_Piece = () => {
    let initalState =  [
        [0,0,0],
        [0,0,0],
        [0,0,0],

    ];

    const piece = Piece({state: initalState});
    return piece;
}

const randomPiece = () => {
    const i = I_Piece();
    const o = O_Piece();
    const z = Z_Piece();
    const s = S_Piece();
    const j = J_Piece();
    const l = L_Piece();
    const m = M_Piece();

    //eslint-disable-next-line no-unused-vars
    const x = X_Piece();
    const pieces = [
        i,
        o,
        z,
        s,
        j,
        l,
        m,
        //x --> experimental X piece.
    ];

    const rnd = Math.floor(Math.random() * pieces.length);
    const randomPiece = pieces[rnd];
    return randomPiece;
}

const emtpyPiece = () => {
    return empty_Piece();
}

export {randomPiece, emtpyPiece};