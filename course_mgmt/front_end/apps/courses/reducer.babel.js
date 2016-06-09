var actions = require('courses/constants').ACTIONS
var Immutable = require('immutable')

var initialState = Immutable.Map({
	course: {},
	courses: {},
	isLoading: true,
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
		case actions.SHOW_COURSES:
			return showCourses(state, action.payload)
		case actions.TOGGLE_FORM:
			return toggleForm(state, action.payload)
		case actions.TOGGLE_LOADING:
			return toggleLoading(state, action.payload)
		default:
			return state
	}
}

function addCourse (state, payload) {
	let courses = state.get('courses')
	courses.push(payload.course)

	return state.merge({ courses })
}

function receiveCourses (state, payload) {
	return state.merge({
		courses: payload.courses,
		isShowingCourse: false,
	})
}

function receiveCourse (state, payload) {
	return state.merge({
		isShowingCourse: true,
		course: payload.course,
	})
}


function showCourses (state, payload) {
	return state.merge({
		course: {},
		isShowingCourse: false,
	})
}

function toggleForm (state, payload) {
	return state.merge({
		isShowingForm: payload.value,
		course: payload.course || {},
	})
}

function toggleLoading (state, payload) {
	return state.merge({
		isLoading: payload.value,
	})
}
