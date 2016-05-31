var actions = require('./constants').ACTIONS
var Immutable = require('immutable')

let initialState = Immutable.Map({
	student: {},
	students: [],
	isLoading: false,
	isShowingStudent: false,
})

module.exports = (state = initialState, action) => {
	switch (action.type) {
		case actions.RECEIVE_STUDENT:
			return receiveStuden(state, action.payload)
		case actions.RECEIVE_STUDENTS:
			return receiveStudents(state, action.payload)
		case actions.TOGGLE_LOADING:
			return toggleLoading(state, action.payload)
		default:
			return state
	}
}

function receiveStudent (state, payload) {
	return state.merge({
		isShowingStudent: true,
		student: payload.student,
	})
}

function receiveStudents (state, payload) {
	return state.merge({
		isShowingStudent: false,
		students: payload.students,
	})
}

function toggleLoading (state, payload) {
	return state.merge({
		isLoading: payload.value,
	})
}
