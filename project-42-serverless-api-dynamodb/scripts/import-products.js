const ora = require('ora');
const spinner = ora({
	spinner: 'simpleDotsScrolling',
});
const boxen = require('boxen');
const moment = require('moment');
var AWS = require('aws-sdk');
require('dotenv').config()
console.log(process.env)
var docClient = new AWS.DynamoDB.DocumentClient({ convertEmptyValues: true, region: 'ap-southeast-1' });
const fs = require('fs');

async function importEmployees() {
	try {
		spinner.start(`Checking AWS credentials`);
		if (process.env.AWS_PROFILE || (process.env.AWS_ACCESS_KEY_ID && process.env.AWS_SECRET_ACCESS_KEY)) {
			spinner.succeed(`Credentials found`);

			const startTime = moment();
			spinner.start(`Reading JSON file`);
			let employees = JSON.parse(fs.readFileSync('sample-employees.json'));
			spinner.succeed(`Reading JSON file`);
			spinner.info(`Found ${employees.length} employees`);

			if (employees.length > 0) {
				spinner.start('Building Put Requests');
				const putRequests = [];
				for (const employee of employees) {
					putRequests.push({
						PutRequest: {
							Item: employee,
						},
					});
				}
				spinner.succeed(`Finished building Put Requests. Request count is ${putRequests.length}`);

				spinner.start('Building batch write chunks');
				const batchWriteChunks = [];
				if (putRequests.length > 0) {
					let index = 0;
					const chunkSize = 20;
					while (index < putRequests.length) {
						batchWriteChunks.push(putRequests.slice(index, chunkSize + index));
						index += chunkSize;
					}
				}
				spinner.succeed(`Finished building batch write chunks. chunk count is ${batchWriteChunks.length}`);

				if (batchWriteChunks.length > 0) {
					spinner.start(`Processing batch write chunks`);
					for (const [i, batchWriteChunk] of batchWriteChunks.entries()) {
						spinner.text = `Processing chunk ${i + 1} of ${batchWriteChunks.length}`;
						const batchWriteParams = {
							RequestItems: {},
						};
						batchWriteParams.RequestItems[process.env.EMPLOYEES_DDB_TABLE] = batchWriteChunk;
						await docClient.batchWrite(batchWriteParams).promise();
					}

					spinner.succeed('Finished batch writing items to Dynamo DB');
				}

				const endTime = moment();
				const processingTime = endTime.diff(startTime);
				if (processingTime < 1000) {
					console.log(boxen(`Finished processing ${employees.length} items in ${processingTime} ms`, { padding: 1 }));
				} else if (processingTime < 60000) {
					console.log(boxen(`Finished processing ${employees.length} items in ${endTime.diff(startTime, 'seconds')} secs`, { padding: 1 }));
				} else {
					console.log(boxen(`Finished processing ${employees.length} items in ${endTime.diff(startTime, 'minutes')} mins`, { padding: 1 }));
				}
			} else {
				spinner.fail(`No items found in ${answers.filename}`);
			}
		} else {
			spinner.fail(`No credentials found. Aborting`);
			process.exit();
		}
	} catch (error) {
		spinner.fail(error.message ? error.message : error);
	}
}

importEmployees();
