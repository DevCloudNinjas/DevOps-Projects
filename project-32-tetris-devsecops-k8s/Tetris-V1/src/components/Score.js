import {useEffect, useState} from "react";

export const Score = (props) => {
    const [score, setScore] = useState(props.score);

    useEffect(() => {
        setScore(props.score);
    }, [props.score])

    return (
        <div>
            <span class="title">Score</span>
            <p class="gameText">{score}</p>
        </div>
    )
}

export default Score;
