var actions = require('classes/constants').ACTIONS
var Immutable = require('immutable')

let initialState = Immutable.Map({
	classObj: Immutable.Map(),
	classes: Immutable.List(),
	courses: Immutable.List(),
	isLoading: true,
	isShowingClass: false,
	studentsByClass: Immutable.List(),
	isShowingForm: false,
})

module.exports = (state = initialState, action) => {
	switch (action.type) {
		case actions.RECEIVE_CLASS:
			return receiveClass(state, action.payload)
		case actions.RECEIVE_CLASSES:
			return receiveClasses(state, action.payload)
		case actions.RECEIVE_COURSES:
			return receiveCourses(state, action.payload)
		case actions.RECEIVE_STUDENTS:
			return receiveStudents(state, action.payload)
		case actions.RENDER_CLASS:
			return renderClass(state)
		case actions.RENDER_CLASSES:
			return renderClasses(state)
		case actions.SAVE_FORM:
			return saveForm(state, action.payload)
		case actions.RENDER_FORM:
			return renderForm(state, action.payload)
		case actions.TOGGLE_LOADING:
			return toggleLoading(state, action.payload)
		default:
			return state
	}
}

function receiveClass (state, payload) {
	let { classObj } = payload

	return state.merge({
		isShowingClass: true,
		classObj: classObj,
	})
}

function receiveClasses (state, payload) {
	let { classes } = payload

	return state.merge({
		classes: classes,
	})
}

function receiveCourses (state, payload) {
	let { courses } = payload

	return state.merge({
		courses: courses,
	})
}

function receiveStudents (state, payload) {
	let { students } = payload

	return state.merge({
		studentsByClass: students,
	})
}

function renderClass (state) {
	return state.merge({
		isShowingClass: true,
		isShowingForm: false,
	})
}

function renderClasses (state) {
	return state.merge({
		isShowingClass: false,
		isShowingForm: false,
	})
}

function saveForm (state, paylaod) {

}

function renderForm (state, payload) {
	let { classObj } = payload

	return state.merge({
		isShowingClass: false,
		isShowingForm: true,
		classObj,
	})
}

function toggleLoading (state, payload) {
	let { value } = payload

	return state.merge({
		isLoading: value,
	})
}
