var actions = require('lectures/constants').ACTIONS
var Immutable = require('immutable')

let initialState = Immutable.Map({
	courses: Immutable.List(),
	lectures: Immutable.List(),
	lecture: Immutable.Map(),
	isLoading: true,
	isShowingForm: false,
	isShowingLecture: false,
})

module.exports = (state = initialState, action) => {
	switch (action.type) {
		case actions.RECEIVE_COURSES:
			return receiveCourses(state, action.payload)
		case actions.RECEIVE_LECTURE:
			return receiveLecture(state, action.payload)
		case actions.RECEIVE_LECTURES:
			return receiveLectures(state, action.payload)
		case actions.RENDER_FORM:
			return renderForm(state)
		case actions.RENDER_LECTURE:
			return renderLecture(state)
		case actions.RENDER_LECTURES:
			return renderLectures(state)
		case actions.TOGGLE_LOADING:
			return toggleLoading(state, action.payload)
		default:
			return state
	}
}

function toggleLoading (state, payload) {
	return state.merge({
		isLoading: payload.value,
	})
}

// RECEIVE
function receiveCourses (state, payload) {
	let { courses } = payload

	return state.merge({
		courses: Immutable.fromJS(courses)
	})
}

function receiveLecture(state, payload) {
	let { lecture } = payload

	return state.merge({
		lecture: Immutable.fromJS(lecture),
	})
}

function receiveLectures(state, payload) {
	let { lectures } = payload

	return state.merge({
		lectures: Immutable.fromJS(lectures),
	})
}

// RENDER
function renderForm (state) {
	return state.merge({
		isShowingForm: true,
		isShowingLecture: false,
	})
}

function renderLecture (state) {
	return state.merge({
		isShowingForm: false,
		isShowingLecture: true,
	})
}

function renderLectures (state) {
	return state.merge({
		isShowingForm: false,
		isShowingLecture: false,
	})
}
