import React from 'react';
import styled from 'styled-components';

const CenterOverlay = styled.div`
	position: fixed;
	top: 0;
  left: 0;
  right: 0;
  bottom: 0;
	width: 100vw;
	height: 100vh;
	z-index: 100;
	background-color: rgba(0,0,0,0.5);
	display: flex;
	justify-content: center;
	align-items: center;
`;

const LoseContainer = styled.div`
	transition: all 0.2s;
	width: ${props => props.pixelSize * (props.portrait ? 12 : 20)}px;
	height: ${props => props.pixelSize * (props.portrait ? 20 : 10)}px;
	border: ${props => props.pixelSize / 10}px solid white;
	background-color: ${props => props.theme3d ? '#444' : '#000'};
	font-size: ${props => props.pixelSize}px;
	font-family: "ZCOOL QingKe HuangYou", cursive;
	color: white;
	display: flex;
	flex-flow: column;
`;

const Title = styled.div`
	width: 100%;
	font-size: 2em;
	padding: ${props => props.portrait ? 10 : 2}% 0;
	text-align: center;
	border-bottom: 1px solid white;
	flex: 0 1 auto;
`;

const ContainerStatus = styled.div`
	flex: 1 1 auto;
	display: flex;
	flex-direction: column;
	justify-content: space-evenly;
`;

const StatusRow = styled.div`
	text-align: center;
`;

const ContainerButton = styled.div`
	flex: 0 1 auto;
	padding: ${props => props.portrait ? 10 : 2}% 0;
	display: flex;
	justify-content: center;
	align-items: center;
	border-top: 1px solid white;
`;

const Button = styled.button`
	width: ${props => props.pixelSize * 10}px;
	height: ${props => props.pixelSize * 2}px;
	font-size: ${props => props.pixelSize / 1.5}px;
	font-family: "ZCOOL QingKe HuangYou", cursive;
	color: white;
	border: ${props => props.pixelSize / 20}px solid white;
	border-radius: ${props => props.pixelSize / 10}px;
	background-color: rgba(0,0,0,0);
	transition: all 0.5s;

	:hover {
		color: #222;
		border: ${props => props.pixelSize / 20}px solid rgba(0,0,0,0);
		background-color: white;
	}

`;

const LoseGame = ({status, portrait, pixelSize, theme3d, restartClick}) => (
	<CenterOverlay>
		<LoseContainer portrait={portrait} pixelSize={pixelSize} theme3d={theme3d}>
			<Title portrait={portrait}>Game Over</Title>
			<ContainerStatus>
				<StatusRow>SCORE: {status.score}</StatusRow>
				<StatusRow>LEVEL: {status.level}</StatusRow>
				<StatusRow>LINES: {status.lines}</StatusRow>
			</ContainerStatus>
			<ContainerButton portrait={portrait}>
				<Button pixelSize={pixelSize} onClick={() => restartClick()}>Restart</Button>
			</ContainerButton>
		</LoseContainer>
	</CenterOverlay>
);

export default LoseGame;