var actions = require('./constants').ACTIONS
var Immutable = require('immutable')

let initialState = Immutable.Map({
	class: {},
	classes: [],
	isLoading: false,
	isShowingClass: false,
	studentsByClass: [],
	isShowingForm: false,
})

module.exports = (state = initialState, action) => {
	switch (action.type) {
		case actions.RECEIVE_CLASS:
			return receiveClass(state, action.payload)
		case actions.RECEIVE_CLASSES:
			return receiveClasses(state, action.payload)
		case actions.RECEIVE_STUDENTS:
			return receiveStudents(state, action.payload)
		case actions.TOGGLE_LOADING:
			return toggleLoading(state, action.payload)
		default:
			return state
	}
}

function receiveClass (state, payload) {
	console.log(payload)
	return state.merge({
		isShowingClass: true,
		class: payload.classObj,
	})
}

function receiveClasses (state, payload) {
	return state.merge({
		isShowingClass: false,
		classes: payload.classes,
		studentsByClass: [],
	})
}

function receiveStudents (state, payload) {
	return state.merge({
		studentsByClass: payload.students,
	})
}

function toggleLoading (state, payload) {
	return state.merge({
		isLoading: payload.value,
	})
}
