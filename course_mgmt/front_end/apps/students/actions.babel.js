var $ = require('jquery')
var _ = require('underscore')
var Immutable = require('immutable')
var actions = require('students/constants').ACTIONS
var API = require('constants.js').API

module.exports = {
	setup () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchStudents()),
				dispatch(fetchClasses())
			)
			.then(() => dispatch(toggleLoading(false)))
		}
	},

	onEditStudent (studentId) {
		return (dispatch, getState) => {
			let students = getState().get('students').toJS()
			let student = _.findWhere(students, { id: studentId })

			dispatch(renderForm(student))
		}
	},

	onDeleteStudent (studentId) {
		let data = {
			data: [{ id: studentId }]
		}

		return (dispatch, getState) => {
			dispatch(toggleLoading(true))

			$.ajax({
				url: API.STUDENT,
				type: 'DELETE',
				data: JSON.stringify(data),
				contentType: 'application/json',
			})
			.then(() => {
				$.when(
					dispatch(fetchStudents())
				)
				.then(() => {
					dispatch(renderStudents())
					dispatch(toggleLoading(false))
				})
			})
		}
	},

	onSaveForm (student) {
		return dispatch => {
			dispatch(toggleLoading(true))

			if (student.id) return dispatch(editStudent(student))
			return dispatch(createStudent(student))
		}
	},

	onShowForm (student) {
		return dispatch => dispatch(renderForm())
	},

	onShowStudent (studentId) {
		return dispatch => {
			dispatch(toggleLoading(true))
			$.when(
				dispatch(fetchStudent(studentId))
			)
			.then(() => {
				dispatch(renderStudent())
				dispatch(toggleLoading(false))
			})
		}
	},

	onShowStudents () {
		return dispatch => dispatch(renderStudents())
	},
}

function toggleLoading (value) {
	return {
		type: actions.TOGGLE_LOADING,
		payload: {
			value,
		}
	}
}

function createStudent (student) {
	let data = { data: [student] }

	return (dispatch, getState) => {
		$.ajax({
			url: API.STUDENT,
			type: 'POST',
			data: JSON.stringify(data),
			contentType: 'application/json',
		})
		.then(res => {
			$.when(
				dispatch(fetchStudents())
			)
			.then(() => {
				dispatch(renderStudents())
				dispatch(toggleLoading(false))
			})
		})
	}
}

function editStudent (editedStudent) {
	// sanitize data body
	editedStudent = _.pick(editedStudent, 'email', 'first_name', 'github_username', 'id', 'last_name', 'photo_url')

	let data = {
		data: [editedStudent]
	}

	return (dispatch, getState) => {
		$.ajax({
			url: API.STUDENT,
			type: 'PUT',
			data: JSON.stringify(data),
			contentType: 'application/json',
		})
		.then(res => {
			let studentId = editedStudent.id
			let students = getState().get('students').toJS()

			_.forEach(students, (classObj, i) => {
				if (classObj.id === studentId) students[i] = editedStudent
			})

			dispatch(receiveStudents(students))
			dispatch(renderStudents())
			dispatch(toggleLoading(false))
		})
	}
}

// RECEIVE
function receiveStudent (student) {
	return {
		type: actions.RECEIVE_STUDENT,
		payload: {
			student: Immutable.fromJS(student),
		}
	}
}

function receiveStudents (students) {
	return {
		type: actions.RECEIVE_STUDENTS,
		payload: {
			students: Immutable.fromJS(students),
		}
	}
}
function receiveClasses (classes) {
	return {
		type: actions.RECEIVE_CLASSES,
		payload: {
			classes: Immutable.fromJS(classes)
		}
	}
}

// FETCH
function fetchStudent (id) {
	return dispatch => {
		return $.get(API.STUDENT + id + '?data=class,assignment,attendance')
			.then(res => dispatch(receiveStudent(res.data)))
	}
}

function fetchStudents () {
	return dispatch => {
		return $.get(API.STUDENT + '?data=class')
			.then(res => dispatch(receiveStudents(res.data)))
	}
}

function fetchClasses () {
	return dispatch => {
		return $.get(API.CLASS)
			.then(res => dispatch(receiveClasses(res.data)))
	}
}

// RENDER
function renderStudent () {
	return {
		type: actions.RENDER_STUDENT,
	}
}

function renderStudents () {
	return {
		type: actions.RENDER_STUDENTS,
	}
}

function renderForm () {
	return {
		type: actions.RENDER_FORM,
	}
}
