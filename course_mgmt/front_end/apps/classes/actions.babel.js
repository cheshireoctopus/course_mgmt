var $ = require('jquery')
var Immutable = require('immutable')
var actions = require('classes/constants').ACTIONS
var API = require('constants.js').API
var _ = require('underscore')

module.exports = {
	setup () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchClasses()),
				dispatch(fetchCourses())
			).then(() => dispatch(toggleLoading(false)))
		}
	},

	onEditClass (classId) {
		return (dispatch, getState) => {
			let classes = getState().get('classes').toJS()
			let classObj = _.findWhere(classes, { id: classId })

			dispatch(renderForm(classObj))
		}
	},

	deleteClass (classId) {
		return (dispatch, getState) => {
			dispatch(toggleLoading(true))

			let data = {
				data: [{ id: classId }]
			}
			let classes = getState().get('classes').toJS().filter(classObj => classObj.id !== classId)

			$.ajax({
				url: API.CLASS,
				type: 'DELETE',
				contentType: 'application/json',
				data: JSON.stringify(data),
			}).then(() => {
				dispatch(receiveClasses(classes))
				dispatch(renderClasses())
				dispatch(toggleLoading(false))
			})
		}
	},

	saveClass (classObj) {
		return dispatch => {
			dispatch(toggleLoading(true))

			if (classObj.id) return dispatch(editClass(classObj))
			return dispatch(createClass(classObj))
		}

	},

	showClass (classId) {
		return dispatch => {
			dispatch(toggleLoading(true))

			// fetch class, students, and attendance
			$.when(
				$.get(API.CLASS + classId + '?data=student,homework,lecture'),
				$.get(API.STUDENT + '?class_id=' + classId),
				$.get(API.ATTENDANCE + '?class_id=' + classId)
			)
			.then((classRes, studentRes, attendanceRes) => {
				dispatch(receiveStudents(studentRes[0].data))
				dispatch(receiveClass(classRes[0].data))
				dispatch(receiveAttendance(attendanceRes[0].data))
				dispatch(renderClass())
				dispatch(toggleLoading(false))
			})
		}
	},

	showClasses () {
		return (dispatch, getState) => {
			dispatch(renderClasses())
		}
	},

	onShowForm (classObj) {
		return dispatch => dispatch(renderForm({}))
	},

	updateAttendance (id, value) {
		let data = {
			data: [
				{
					id,
					did_attend: (value === 'true'),
				}
			]
		}

		$.ajax({
			url: API.ATTENDANCE,
			type: 'PUT',
			data: JSON.stringify(data),
			contentType: 'application/json',
		})
	}
}

function createClass (classObj) {
	let data = {
		data: [classObj]
	}

	return (dispatch, getState) => {
		$.ajax({
			url: API.CLASS,
			type: 'POST',
			data: JSON.stringify(data),
			contentType: 'application/json',
		})
		.then(res => {
			let classes = getState().get('classes').toJS()

			classes.push(res.data[0])

			dispatch(receiveClasses(classes))
			dispatch(renderClasses())
			dispatch(toggleLoading(false))
		})
	}
}

function editClass (editedClass) {
	let data = {
		data: [editedClass]
	}

	return (dispatch, getState) => {
		$.ajax({
			url: API.CLASS,
			type: 'PUT',
			data: JSON.stringify(data),
			contentType: 'application/json',
		})
		.then(res => {
			let classId = editedClass.id
			let classes = getState().get('classes').toJS()

			_.forEach(classes, (classObj, i) => {
				if (classObj.id === classId) classes[i] = editedClass
			})

			dispatch(receiveClasses(classes))
			dispatch(renderClasses())
			dispatch(toggleLoading(false))
		})
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

// FETCH
function fetchClass (classId) {
	return dispatch => {
		$.get(API.CLASS + classId)
			.then(res => dispatch(receiveClass(res.data)))
	}
}

function fetchClasses () {
	return dispatch => {
		$.get(API.CLASS)
			.then(res => dispatch(receiveClasses(res.data)))
	}
}

function fetchCourses () {
	return dispatch => {
		$.get(API.COURSE)
			.then(res => dispatch(receiveCourses(res.data)))
	}
}

// RECEIVE
function receiveClass (classObj) {
	return {
		type: actions.RECEIVE_CLASS,
		payload: {
			classObj: Immutable.fromJS(classObj),
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

function receiveCourses (coursesRes) {
	let courses = Immutable.fromJS(coursesRes)

	return {
		type: actions.RECEIVE_COURSES,
		payload: {
			courses,
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

function receiveAttendance (attendance) {
	return {
		type: actions.RECEIVE_ATTENDANCE,
		payload: {
			attendance: Immutable.fromJS(attendance)
		}
	}
}

// RENDER
function renderClass () {
	return {
		type: actions.RENDER_CLASS,
	}
}

function renderClasses () {
	return {
		type: actions.RENDER_CLASSES,
	}
}

function renderForm (classObj) {
	return {
		type: actions.RENDER_FORM,
		payload: {
			classObj: Immutable.fromJS(classObj)
		}
	}
}

