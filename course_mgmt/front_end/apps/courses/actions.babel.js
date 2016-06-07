var $ = require('jquery')
var actions = require('./constants.js').ACTIONS
var API = require('./../constants.js').API

module.exports = {
	saveForm (courseName) {
		let data = {
			data: [{ name: courseName }]
		}

		return dispatch => {
			$.ajax({
				url: API.COURSE,
				type: 'POST',
				contentType: 'application/json',
				data: JSON.stringify(data),
			}).done((res) => {
				dispatch(toggleForm(false))
				dispatch(addCourse(res.data[0]))
			})
		}
	},

	setup () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchCourses())
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},

	showCourse (courseId) {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchCourse(courseId)),
				dispatch(fetchCourseClasses(courseId))
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},

	showCourses () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchCourses())
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},

	toggleForm () {
		return (dispatch, getState) => {
			let isShowingForm = getState().get('isShowingForm')

			dispatch(toggleForm(!isShowingForm))
		}
	}
}

function addCourse (course) {
	return {
		type: actions.ADD_COURSE,
		payload: { course },
	}
}

function toggleLoading (value) {
	return {
		type: actions.TOGGLE_LOADING,
		payload: { value },
	}
}

function fetchCourse (courseId) {
	return dispatch => {
		$.get(API.COURSE + courseId)
			.then(res => dispatch(receiveCourse(res.data)))
	}
}

function fetchCourseClasses (courseId) {
	return dispatch => {
		$.get(API.COURSE + courseId + '/class')
			.then(res => dispatch(receiveCourseClasses(res.data)))
	}
}

function fetchCourses () {
	return dispatch =>
		$.get(API.COURSE)
			.then(res => dispatch(receiveCourses(res.data)))
}

function receiveCourse (course) {
	return {
		type: actions.RECEIVE_COURSE,
		payload: { course },
	}
}

function receiveCourseClasses (classes) {
	return {
		type: actions.RECEIVE_COURSE_CLASSES,
		payload: { classes },
	}
}

function receiveCourses (courses) {
	return {
		type: actions.RECEIVE_COURSES,
		payload: { courses },
	}
}

function toggleForm (value) {
	return {
		type: actions.TOGGLE_FORM,
		payload: { value },
	}
}
