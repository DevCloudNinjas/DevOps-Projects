const log = require('/opt/helpers/logger').logger;
const validator = require('/opt/helpers/validator');

var AWS = require('aws-sdk');
var docClient = new AWS.DynamoDB.DocumentClient({ convertEmptyValues: true });

exports.lambdaHandler = async (event, context) => {
	try {
		// Checking event
		log.info('Checking evnet');
		if (!event) throw new Error('Event not found');

		// Validating Payload
		log.info('Validating payload');
		const validation = await validator.validate(event, 'putdata');

		if (validation.result === 'invalid') {
			// Invalid Payload
			log.error(JSON.stringify(validation.errors));
			return { status: 'Error', message: validation.errors };
		} else {
			// Valid payload
			log.info('Payload valid');

			// DDb put data parameters
			const putDataParams = {
				TableName: process.env.PRODUCTS_DDB_TABLE,
				Item: event,
			};

			// Put data into Dynamo DB
			log.info('Adding data to Dynamo DB');
			const putDataRes = await docClient.put(putDataParams).promise();
			log.info(putDataRes);

			// Return Data
			return {
				status: 'Success',
				message: 'Data added successfully',
			};
		}
	} catch (error) {
		log.error(error.message ? error.message : error);
		return { status: 'Error', message: error.message ? error.message : error };
	}
};
