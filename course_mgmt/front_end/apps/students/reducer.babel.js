var actions = require('students/constants').ACTIONS
var Immutable = require('immutable')

let initialState = Immutable.Map({
	classes: Immutable.List(),
	student: Immutable.Map(),
	students: Immutable.List(),
	isLoading: false,
	isShowingStudent: false,
	isShowingForm: false,
})

module.exports = (state = initialState, action) => {
	switch (action.type) {
		case actions.RECEIVE_CLASSES:
			return receiveClasses(state, action.payload)
		case actions.RECEIVE_STUDENT:
			return receiveStudent(state, action.payload)
		case actions.RECEIVE_STUDENTS:
			return receiveStudents(state, action.payload)
		case actions.RENDER_FORM:
			return renderForm(state)
		case actions.RENDER_STUDENT:
			return renderStudent(state)
		case actions.RENDER_STUDENTS:
			return renderStudents(state)
		case actions.TOGGLE_LOADING:
			return toggleLoading(state, action.payload)
		default:
			return state
	}
}

// RECEIVE
function receiveClasses (state, payload) {
	return state.merge({
		classes: payload.classes,
	})
}

function receiveStudent (state, payload) {
	return state.merge({
		student: payload.student,
	})
}

function receiveStudents (state, payload) {
	return state.merge({
		students: payload.students,
	})
}

function renderForm (state) {
	return state.merge({
		isShowingStudent: false,
		isShowingForm: true,
	})
}

// RENDER
function renderStudent (state) {
	return state.merge({
		isShowingStudent: true,
		isShowingForm: false,
	})
}

function renderStudents (state) {
	return state.merge({
		student: Immutable.Map(),
		isShowingStudent: false,
		isShowingForm: false,
	})
}

function toggleLoading (state, payload) {
	return state.merge({
		isLoading: payload.value,
	})
}
