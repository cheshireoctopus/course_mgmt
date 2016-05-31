var $ = require('jquery')
var actions = require('./constants').ACTIONS

module.exports = {
	showStudent () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchStudent())
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},

	showStudents () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchStudents())
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},
}

function fetchStudent () {
	return dispatch => {
		$.get('/api/student')
			.then(res => {
				dispatch(receiveStudent(res))
			})
	}
}

function fetchStudents () {
	return dispatch => {
		$.get('/api/students')
			.then(res => {
				dispatch(receiveStudents(res))
			})
	}
}

function receiveStudent (student) {
	return {
		type: actions.RECEIVE_STUDENTS,
		payload: {
			student,
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

function toggleLoading (value) {
	return {
		type: actions.TOGGLE_LOADING,
		payload: {
			value,
		}
	}
}
