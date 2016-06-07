var actions = require('./constants').ACTIONS
var Immutable = require('immutable')

var initialState = Immutable.Map({
	course: {},
	courses: [],
	isLoading: false,
	isShowingCourse: false,
	isShowingForm: false,
})

module.exports = (state = initialState, action) => {
	switch (action.type) {
		case actions.ADD_COURSE:
			return addCourse(state, action.payload)
		case actions.RECEIVE_COURSES:
			return receiveCourses(state, action.payload)
		case actions.RECEIVE_COURSE:
			return receiveCourse(state, action.payload)
		case actions.TOGGLE_FORM:
			return toggleForm(state, action.payload)
		case actions.TOGGLE_LOADING:
			return toggleLoading(state, action.payload)
		default:
			return state
	}
}

function addCourse (state, payload) {
	let courses = state.get('courses').push(payload.course)

	return state.merge({ courses })
}

function receiveCourses (state, payload) {
	let courses = state.get('courses').concat(payload.courses)

	return state.merge({ courses })
}

function receiveCourse (state, payload) {
	return state.merge({
		course: payload.course,
	})
}

function toggleForm (state, payload) {
	return state.merge({
		isShowingForm: payload.value,
	})
}

function toggleLoading (state, payload) {
	return state.merge({
		isLoading: payload.value,
	})
}
