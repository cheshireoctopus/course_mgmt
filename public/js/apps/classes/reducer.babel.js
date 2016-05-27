var actions = require('./constants').ACTIONS
var Immutable = require('immutable')

let initialState = Immutable.Map({
	classes: {},
	isLoading: null,
})

module.exports = (state = initialState, action) => {
	switch (action.type) {
		case actions.RECEIVE_CLASSES:
			return receiveClasses(state, action.payload)
		case actions.TOGGLE_LOADING:
			return toggleLoading(state, action.payload)
		default:
			return state
	}
}

function receiveClasses (state, payload) {
	return state.merge({
		classes: payload.classes
	})
}

function toggleLoading (state, payload) {
	return state.merge({
		isLoading: payload.value
	})
}
