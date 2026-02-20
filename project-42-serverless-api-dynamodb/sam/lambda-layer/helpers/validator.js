var Validator = require('jsonschema').Validator;
var v = new Validator();

// Schema Definitions
const getDataSchema = {
	id: '/getdata',
	type: 'object',
	properties: {
		name: { type: 'string', minLength: 1 },
		description: { type: 'string', minLength: 1 },
	},
	anyOf: [{ required: ['name'] }, { required: ['description'] }],
};

const putDataSchema = {
	id: '/putdata',
	type: 'object',
	properties: {
		name: { type: 'string', minLength: 1 },
		description: { type: 'string', minLength: 1 },
		url: { type: 'string', minLength: 1 },
		tags: { type: 'string', minLength: 1 },
		department: { type: 'string', minLength: 1 },
		price: { type: 'number', minLength: 1 },
		
	},
	required: ['name', 'description', 'price'],
};

// Add schema definition to the validator
v.addSchema(getDataSchema, '/getdata');
v.addSchema(putDataSchema, '/putdata');

// Validate function
exports.validate = async (data, schema) => {
	const validationResult = v.validate(data, schema);
	const status = {};
	if (validationResult.errors.length > 0) {
		(status.result = 'invalid'), (status.errors = validationResult.errors.map((e) => e.stack.replace('instance.', 'payload.')));
	} else {
		(status.result = 'valid'), (status.errors = []);
	}
	return status;
};