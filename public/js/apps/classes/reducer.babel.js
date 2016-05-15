var ACTIONS = require('./constants').ACTIONS
var Immutable = require('immutable')

let initialState = Immutable.Map({
	classes: {}
})

module.exports = function (state = initialState, action) {
	switch (action.type) {
		case ACTIONS.BOOTSTRAP:
			return handleBootstrap(state, action.payload)
		default:
			return state
	}
}

function handleBootstrap (state, payload) {
	return state.merge({
		classes: {}
	})
}
