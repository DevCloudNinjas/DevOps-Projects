import {useEffect, useState} from "react";
export const Level = (props) => {
    const [level, setLevel] = useState(props.level);

    useEffect(() => {
        setLevel(props.level);
    }, [props.level])

    return (
        <div>
            <span class="title">Level</span>
            <p class="gameText">{level}</p>
        </div>
    )
}

export default Level;
