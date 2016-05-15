var actions = require('./constants').ACTIONS

module.exports = {
	bootstrap (options) {
		return {
			type: actions.BOOTSTRAP,
			payload: {
				options,
			}
		}
	}
}
