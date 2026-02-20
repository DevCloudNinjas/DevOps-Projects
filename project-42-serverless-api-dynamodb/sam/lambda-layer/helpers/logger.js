const winston = require('winston');
const { printf } = winston.format;

const myLogFormat = printf(({ level, message }) => {
	return `${level.toUpperCase()} ${message}`;
});

exports.logger = winston.createLogger({
	format: myLogFormat,
	transports: [new winston.transports.Console()],
});