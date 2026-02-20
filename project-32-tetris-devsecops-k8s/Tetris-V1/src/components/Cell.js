import styles from "./Cell.module.css";
import React, { useEffect, useState } from 'react';
import {tetromino2Class} from "../helpers/Helpers";
export const Cell = (props) => {
    const [tetromino, setTetromino] = useState(props.tetromino);

    useEffect(() => {
        setTetromino(props.tetromino);
    }, [props.tetromino])

    return (
        <div className={`${styles.tetromino} ${tetromino2Class(tetromino, styles)}`} />
    )
}

export default Cell;
