const TetrominoStates = {
    EMPTY: 0,
    FILLED: 1,
    SHADOW: 2
};
const Tetromino = (state, color) => {

    let _state = state == null ? TetrominoStates.EMPTY : state;
    let _color = color;

    return {
        isEmpty() {
            return _state === TetrominoStates.EMPTY || _state === TetrominoStates.SHADOW;
        },
        isShadow() {
            return _state === TetrominoStates.SHADOW;
        },
        isFilled() {
            return _state === TetrominoStates.FILLED;
        },
        color: _color,
        state: _state

    }
}

export {Tetromino, TetrominoStates};
