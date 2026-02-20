import React, { useState } from "react";

import StartPage from "../StartPage";
import Game from "../Game";

const Tetris = () => {
	const [runing, setRuning] = useState(false);
	return runing ? (
		<Game stopClick={() => setRuning(false)} />
	) : (
		<StartPage startClick={() => setRuning(true)} />
	);
};

export default Tetris;
