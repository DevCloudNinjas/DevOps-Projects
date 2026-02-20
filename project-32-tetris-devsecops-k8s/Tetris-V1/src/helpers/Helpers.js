import Colors from "../tetris/Colors";
import Cell from "../components/Cell";
const tetromino2Class = (tetromino, styles) => {
    let clazz = styles.empty;
    if(tetromino == null){
        return clazz;
    } else if(tetromino.isFilled()){
        if(Colors.BLUE === tetromino.color){
            return styles.blue;
        } else if(Colors.RED === tetromino.color){
            return styles.red;
        } else if(Colors.GREEN === tetromino.color){
            return styles.green;
        } else if(Colors.YELLOW === tetromino.color){
            return styles.yellow;
        } else {
            return styles.empty;
        }
    } else {
        return styles.empty;
    }
};

const createTetrominoRow = (tetraminos, rowIndex, styles) => {
    const cols = tetraminos.map( (tetramino, colIndex) =>
        <Cell tetromino={tetramino} key={`${rowIndex}-${colIndex}`}/>
    );
    const rowComponent = <div className={styles.row} key={rowIndex}>{cols}</div>;
    return rowComponent;
};

const createMatrix = (state, styles) => {
    if(state == null){
        return null;
    }
    const matrix = state.map( (tetraminos , rowIndex) => {
        return createTetrominoRow(tetraminos, rowIndex, state, styles);
    });
    return matrix;
}

export {tetromino2Class, createMatrix}

