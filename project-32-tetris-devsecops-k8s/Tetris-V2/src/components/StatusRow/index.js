import React from "react";
import styled from "styled-components";

const Container = styled.div`
	background-color: ${props =>
		props.backgroundColor ? props.backgroundColor : "black"};
	transition: background-color 0.5s;
	border: ${props => (props.borderSize ? props.borderSize : "3")}px solid white;
	${props => !props.portrait && `width: 100%;`}
	font-family: "ZCOOL QingKe HuangYou", cursive;
	padding: ${props => (props.padding ? props.padding : "15")}px
		${props => (props.portrait ? props.padding / 2 : 0)}px; /*15*/
	margin-bottom: ${props => (props.margin ? props.margin : "10")}px; /*10*/
`;

const Title = styled.div`
	width: 100%;
	text-align: center;
	color: white;
`;

const Value = styled.div`
	width: 100%;
	text-align: center;
	color: white;
`;

const StatusRow = ({
	title,
	value,
	padding,
	margin,
	borderSize,
	portrait,
	backgroundColor
}) => (
	<Container
		portrait={portrait}
		padding={padding}
		margin={margin}
		borderSize={borderSize}
		backgroundColor={backgroundColor}
	>
		<Title>{title}</Title>
		<Value>{value}</Value>
	</Container>
);

export default StatusRow;
