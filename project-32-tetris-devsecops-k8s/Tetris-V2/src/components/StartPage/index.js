import React from "react";
import styled from "styled-components";

const StyledStartPage = styled.div`
	width: 100vw;
	height: 100vh;
	overflow: hidden;
	background-color: #e3b505;
`;

const StartButton = styled.button`
	font-size: 2.2em;
	font-family: "ZCOOL QingKe HuangYou", cursive;
	/* border: 2px solid #222; */
	border: none;
	padding: 30px 100px;
	background-color: #fff;
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	vertical-align: middle;
	text-decoration: none;
	transition: all 0.5s;
	color: #95190c;
	border-right: 1px solid #eee;
	border-radius: 2px;
	border-bottom: 1px solid #ccc;

	:focus {
		outline: 0;
	}

	:hover {
		margin-left: 5px;
		margin-top: 5px;
		::after {
			right: -5px;
			top: 2px;
			width: 5px;
		}
		::before {
			right: -3px;
			height: 5px;
		}
	}

	::after {
		content: "";
		height: 100%;
		width: 10px;
		background-color: #eee;
		right: -10px;
		top: 5px;
		transform: skewY(45deg);
		position: absolute;
		transition: all 0.5s;
	}

	::before {
		content: "";
		height: 10px;
		width: 100%;
		background-color: #ccc;
		right: -5px;
		top: 95px;
		transform: skewX(45deg);
		position: absolute;
		transition: all 0.5s;
	}
`;

const StartPage = ({ startClick }) => {
	return (
		<StyledStartPage>
			<StartButton onClick={startClick}>Start</StartButton>
		</StyledStartPage>
	);
};
export default StartPage;
