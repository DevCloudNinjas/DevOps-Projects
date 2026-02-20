const Colors = {
    RED: 1,
    BLUE: 2,
    YELLOW: 3,
    GREEN: 4,
};

const randomColor = () => {
    const rand = Math.floor(Math.random() * Object.keys(Colors).length);
    const randColorValue = Colors[Object.keys(Colors)[rand]];
    return randColorValue;
}

export default Colors;
export {randomColor}
