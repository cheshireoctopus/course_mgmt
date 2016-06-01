var $ = require('jquery')
var actions = require('./constants').ACTIONS
var API = require('../constants.js').API

module.exports = {
	setup () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchClasses())
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},

	showClass (classId) {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchClass(classId)),
				dispatch(fetchStudentsByClassId(classId))
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},

	showClasses () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchClasses())
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	}
}

function toggleLoading (value) {
	return {
		type: actions.TOGGLE_LOADING,
		payload: {
			value,
		}
	}
}

function fetchClass (classId) {
	return dispatch => {
		$.get(API.CLASS + classId)
			.then(res => {
				dispatch(receiveClass(res.data))
			})
	}
}

function fetchClasses () {
	return dispatch =>
		$.get(API.CLASS)
			.then(res => {
				dispatch(receiveClasses(res.data))
			})
}

function fetchStudentsByClassId (classId) {
	return dispatch => {
		$.get('/api/students/class/' + classId)
			.then(res => {
				dispatch(receiveStudents(res))
			})
	}
}

function receiveClass (classObj) {
	return {
		type: actions.RECEIVE_CLASS,
		payload: {
			classObj,
		}
	}
}

function receiveClasses (classes) {
	return {
		type: actions.RECEIVE_CLASSES,
		payload: {
			classes,
		}
	}
}

function receiveStudents (students) {
	return {
		type: actions.RECEIVE_STUDENTS,
		payload: {
			students,
		}
	}
}

