import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import Switch from "react-switch";

import useWindowDimensions from "../../hooks/useWindowDimensions";
import background from "../../images/background.jpg";
import StatusRow from "../StatusRow";
import LoseGame from '../LoseGame';

import Color from "color";

const Game = styled.div`
	width: 100vw;
	height: ${props => (props.portrait ? "95" : "100")}vh;
	display: flex;
	flex-direction: ${props => (props.portrait ? "column" : "row")};
	justify-content: center;
	align-items: center;
	background-image: url(${background});
	background-size: cover;
	background-position: center;
`;

const ContainerNext = styled.div`
	${props =>
		!props.portrait && `height: ${props.pixelSize * 18 + (18 / 3) * 1}px;`}
	${props => props.portrait && `width: ${props.pixelSize * 10 + (10 / 3) * 1}px;`}
	margin-right: ${props => (props.portrait ? 0 : props.pixelSize / 3)}px;
	margin-bottom: ${props => (props.portrait ? props.pixelSize / 3 : 0)}px;
	display: flex;
	flex-direction: ${props => (props.portrait ? "row" : "column")};
	justify-content: ${props => (props.portrait ? "space-between" : "flex-start")};
	align-items: center;
`;

const Next = styled.div`
	width: ${props => props.pixelSize * 3}px;
	height: ${props => props.pixelSize * 3}px;
	background-color: ${props => (props.theme3d ? "#444" : "black")};
	transition: background-color 0.5;
	border: ${props => props.pixelSize / 10}px solid white;
	overflow: hidden;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	margin-bottom: ${props => (props.portrait ? 0 : props.pixelSize / 3)}px;
	margin-right: ${props => (!props.portrait ? 0 : props.pixelSize / 3)}px;
`;

const StyledStage = styled.div`
	border: ${props => props.pixelSize / 10}px solid white;
	background-color: ${props => (props.theme3d ? "#444" : "black")};
	transition: background-color 0.5s;
	overflow: hidden;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
`;

const Center = styled.div`
	width: 100%;
	height: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
`;

const Row = styled.div`
	display: flex;
	flex-direction: row;
	justify-content: center;
	height: ${props => (props.stage ? props.pixelSize : props.pixelSize / 1.6)}px;
`;

const Pixel = React.memo(styled.div`
	width: ${props => (props.stage ? props.pixelSize : props.pixelSize / 1.6)}px;
	height: ${props => (props.stage ? props.pixelSize : props.pixelSize / 1.6)}px;
	background-color: ${props => (props.fill === 1 ? props.color : "inherited")};
	position: relative;
	z-index: ${props => props.zIndex};

	${props =>
		props.paused &&
		`
		transition: all 1s;
	`};

	${props =>
		props.fill &&
		props.theme3d &&
		`;
		box-shadow: ${props.pixelSize / 4.16}px ${props.pixelSize /
			4.16}px ${props.pixelSize / 5.55}px #222${
			props.topBloco
				? `, 0 ${-props.pixelSize / 4.16}px 0 ${Color(props.color).lighten(0.2)}`
				: ""
		} 
	`};

	${props =>
		!props.theme3d &&
		`
		border-left: 1px solid ${
			props.stage || props.fill || props.hint ? "#222" : "black"
		};
		border-top: 1px solid ${
			props.stage || props.fill || props.hint ? "#222" : "black"
		};	
	`};

	${props =>
		props.hint &&
		`
		border: 1px solid ${Color(props.playerColor).alpha(0.5)};
		background-color: rgba(255,255,255,0.1);
	`};
`);

const ContainerSwitch = styled.div`
	${props =>
		props.portrait &&
		`
		height: 100%;
		width: 100%;
		display: flex;
		align-items: flex-end;
		flex-direction: column;
		justify-content: flex-end;
	`};
`;

const ContainerStatus = styled.div`
	width: ${props => props.pixelSize * 8}px;
	${props =>
		!props.portrait && `height: ${props.pixelSize * 18 + (18 / 3) * 1}px;`}
	${props => props.portrait && `width: ${props.pixelSize * 10 + (10 / 3) * 1}px;`}
	margin-left: ${props => (props.portrait ? 0 : props.pixelSize / 3)}px;
	margin-top: ${props => (props.portrait ? props.pixelSize / 3 : 0)}px;
	display: flex;
	flex-direction: ${props => (props.portrait ? "row" : "column")};
	align-items: center;
	justify-content: ${props => (props.portrait ? "space-between" : "flex-start")};
	font-size: ${props => props.pixelSize}px;
`;

const getRenderizacaoBloco = bloco => {
	let trimRowBloco = [];
	let sumColumn = {};
	bloco.forEach((row, y) => {
		let rowSum = 0;
		row.forEach(pixel => (rowSum = rowSum + pixel));
		if (rowSum > 0) trimRowBloco.push(row);
		row.forEach((pixel, x) => {
			sumColumn[x] = (sumColumn[x] ? sumColumn[x] : 0) + pixel;
		});
	});
	let trimBloco = [];
	trimRowBloco.forEach((row, y) => {
		let newRow = [];
		row.forEach((pixel, x) => {
			if (sumColumn[x] > 0) newRow.push(pixel);
		});
		trimBloco.push(newRow);
	});
	return trimBloco;
};

const Stage = ({ lose, restartClick, map, player, hint, status, paused, ...others }) => {
	const [pixelSize, setPixelSize] = useState(30);
	const [portrait, setPortrait] = useState(false);
	const { width, height } = useWindowDimensions();
	const [theme3d, setTheme3d] = useState(false);
	const [nextRender, setNextRender] = useState();
	const stageRef = useRef(null);

	useEffect(() => {
		let pixelSizeHeight = height / 20;
		let pixelSizeWidth = width / 32;
		if (portrait) {
			pixelSizeHeight = height / 26;
			pixelSizeWidth = width / 12;
		}
		setPixelSize(
			pixelSizeWidth < pixelSizeHeight ? pixelSizeWidth : pixelSizeHeight
		);
		setPortrait(height > width);
	}, [width, height, portrait]);

	useEffect(() => {
		if (!player.next) return;
		setNextRender(getRenderizacaoBloco(player.next.bloco));
	}, [player.next]);

	useEffect(() => {
		if (!lose) {
			stageRef.current.focus();
		}
	}, [lose]);

	useEffect(() => {
		stageRef.current.focus();
	}, [theme3d]);

	return (
		<div>
			<Game portrait={portrait}>
				{nextRender && (
					<ContainerNext portrait={portrait} pixelSize={pixelSize}>
						<Next portrait={portrait} theme3d={theme3d} pixelSize={pixelSize}>
							{nextRender.map((row, y) => (
								<Row pixelSize={pixelSize} key={`row-${y}`}>
									{row.map((pixel, x) => {
										let topBloco = pixel && (!nextRender[y - 1] || !nextRender[y - 1][x]);
										return (
											<Pixel
												paused={paused}
												theme3d={theme3d}
												topBloco={topBloco}
												zIndex={y}
												pixelSize={pixelSize}
												key={`pixel-${x}`}
												fill={pixel}
												color={player.next.color}
											/>
										);
									})}
								</Row>
							))}
						</Next>
						<ContainerSwitch portrait={portrait}>
							<Switch
								width={pixelSize * 2}
								height={pixelSize / 1.2}
								onChange={setTheme3d}
								checked={theme3d}
								offColor="#000"
								onColor="#444"
								uncheckedIcon={
									<Center>
										<Pixel
											theme3d={false}
											pixelSize={pixelSize / 3}
											stage="true"
											fill={1}
											color={"#e54b4b"}
										/>
									</Center>
								}
								checkedIcon={
									<Center>
										<Pixel
											theme3d="true"
											pixelSize={pixelSize / 3}
											stage="true"
											fill={1}
											color={"#e54b4b"}
											topBloco="true"
										/>
									</Center>
								}
							/>
						</ContainerSwitch>
					</ContainerNext>
				)}
				{map && (
					<StyledStage ref={stageRef} {...others} theme3d={theme3d} pixelSize={pixelSize}>
						{map.map((row, y) => (
							<Row stage="true" pixelSize={pixelSize} key={`row-${y}`}>
								{row.map((pixel, x) => {
									let playerFill =
										player.bloco.bloco[y - player.pos[0]] &&
										player.bloco.bloco[y - player.pos[0]][x - player.pos[1]];
									let playerHint =
										hint.bloco.bloco[y - hint.pos[0]] &&
										hint.bloco.bloco[y - hint.pos[0]][x - hint.pos[1]];
									let topBloco =
										(playerFill || pixel.fill) &&
										(!player.bloco.bloco[y - player.pos[0] - 1] ||
											!player.bloco.bloco[y - player.pos[0] - 1][x - player.pos[1]]) &&
										(!map[y - 1] || !map[y - 1][x].fill);
									let zIndex = !playerFill && !pixel.fill && playerHint ? 99 : y;
									return (
										<Pixel
											paused={paused}
											theme3d={theme3d}
											hint={!pixel.fill && !playerFill && playerHint}
											pixelSize={pixelSize}
											stage="true"
											key={`pixel-${x}`}
											fill={pixel.fill || playerFill}
											color={playerFill ? player.bloco.color : pixel.color}
											playerColor={player.bloco.color}
											topBloco={topBloco}
											zIndex={zIndex}
										></Pixel>
									);
								})}
							</Row>
						))}
					</StyledStage>
				)}
				{status && (
					<ContainerStatus portrait={portrait} pixelSize={pixelSize}>
						<StatusRow
							backgroundColor={theme3d ? "#444" : "black"}
							portrait={portrait}
							borderSize={pixelSize / 10}
							margin={pixelSize / 3}
							padding={pixelSize / 2}
							title="SCORE"
							value={status.score}
						/>
						<StatusRow
							backgroundColor={theme3d ? "#444" : "black"}
							portrait={portrait}
							borderSize={pixelSize / 10}
							margin={pixelSize / 3}
							padding={pixelSize / 2}
							title="LEVEL"
							value={status.level}
						/>
						<StatusRow
							backgroundColor={theme3d ? "#444" : "black"}
							portrait={portrait}
							borderSize={pixelSize / 10}
							margin={pixelSize / 3}
							padding={pixelSize / 2}
							title="LINES"
							value={status.lines}
						/>
					</ContainerStatus>
				)}
			</Game>
			{ lose && 
				<LoseGame portrait={portrait} restartClick={restartClick} status={status} pixelSize={pixelSize} theme3d={theme3d}>
				</LoseGame>}
		</div>
	);
};

export default Stage;
